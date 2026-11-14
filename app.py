
import os
import sqlite3
import uuid
import json
import hashlib
from functools import wraps

# Polyfill for hashlib.scrypt if running on macOS LibreSSL
if not hasattr(hashlib, "scrypt"):
    try:
        from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

        def _scrypt_polyfill(password, *, salt, n=16384, r=8, p=1, maxmem=0, dklen=64):
            kdf = Scrypt(salt=salt, length=dklen, n=n, r=r, p=p)
            return kdf.derive(password)

        hashlib.scrypt = _scrypt_polyfill
    except ImportError:
        pass

import base64
from flask import (
    Flask, render_template, request,
    redirect, url_for, session, flash, jsonify
)
from werkzeug.security import generate_password_hash, check_password_hash
from PIL import Image

from recognition import recognize_symbol
from chatbot import answer_clinical_chat


app = Flask(__name__)
app.secret_key = "clinical-symbol-dev-key-change-before-deployment"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IS_VERCEL = bool(os.environ.get("VERCEL"))

if IS_VERCEL:
    UPLOAD_FOLDER = "/tmp/uploads"
    DB_PATH = "/tmp/clinical.db"
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    initial_db = os.path.join(BASE_DIR, "data", "clinical.db")
    if os.path.exists(initial_db) and not os.path.exists(DB_PATH):
        try:
            import shutil
            shutil.copyfile(initial_db, DB_PATH)
        except Exception:
            pass
else:
    DB_PATH = os.path.join(BASE_DIR, "data", "clinical.db")
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

SYMBOLS_PATH = os.path.join(BASE_DIR, "data", "symbols.json")
SYMBOLS_FOLDER = os.path.join(BASE_DIR, "data", "symbols")

app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


def get_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        # Đảm bảo tài khoản demo doctor_test luôn tồn tại kể cả trên môi trường serverless Vercel
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE username = ?", ("doctor_test",))
        if not cur.fetchone():
            demo_pass = generate_password_hash("password123")
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                ("doctor_test", demo_pass)
            )


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return wrapper


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def load_symbols():
    """Đọc danh sách biểu trưng từ file JSON."""
    if not os.path.exists(SYMBOLS_PATH):
        return []

    with open(SYMBOLS_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)

    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        if isinstance(data.get("symbols"), list):
            return data["symbols"]

    return []


@app.route("/symbol-image/<filename>")
def symbol_image(filename):
    from flask import send_from_directory

    filename = os.path.basename(filename)

    return send_from_directory(
        SYMBOLS_FOLDER,
        filename
    )


@app.route("/static/uploads/<path:filename>")
def serve_uploads(filename):
    from flask import send_from_directory

    filename = os.path.basename(filename)

    return send_from_directory(
        UPLOAD_FOLDER,
        filename
    )


@app.errorhandler(413)
def file_too_large(error):
    flash("Ảnh quá lớn. Vui lòng chọn ảnh nhỏ hơn 5 MB.")
    return redirect(url_for("dashboard"))


@app.route("/")
def index():
    symbols = load_symbols()
    return render_template(
        "landing.html",
        symbols=symbols,
        user=session.get("username")
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if len(username) < 3:
            flash("Tên đăng nhập phải có ít nhất 3 ký tự.")
            return redirect(url_for("register"))

        if len(password) < 8:
            flash("Mật khẩu phải có ít nhất 8 ký tự.")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)

        try:
            with get_db() as conn:
                conn.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, hashed_password)
                )
            flash("Đăng ký thành công! Bạn có thể đăng nhập ngay.")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Tên đăng nhập đã tồn tại. Vui lòng chọn tên khác.")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        with get_db() as conn:
            user = conn.execute(
                "SELECT * FROM users WHERE username = ?",
                (username,)
            ).fetchone()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("dashboard"))

        flash("Tên đăng nhập hoặc mật khẩu không đúng.")

    return render_template("login.html")


@app.route("/dashboard")
@login_required
def dashboard():
    symbols = load_symbols()
    return render_template(
        "dashboard.html",
        symbols=symbols,
        result=None,
        uploaded_image=None
    )


@app.route("/recognize", methods=["POST"])
@login_required
def recognize():
    image_base64 = request.form.get("image_base64", "").strip()
    file = request.files.get("symbol_image")

    filename = f"{uuid.uuid4()}.png"
    save_path = os.path.join(UPLOAD_FOLDER, filename)

    try:
        if image_base64:
            # Xử lý ảnh gửi từ Camera hoặc Canvas dạng base64
            if "," in image_base64:
                image_base64 = image_base64.split(",", 1)[1]
            image_data = base64.b64decode(image_base64)
            with open(save_path, "wb") as f:
                f.write(image_data)
        elif file and file.filename != "":
            if not allowed_file(file.filename):
                flash("Chỉ hỗ trợ ảnh PNG, JPG hoặc JPEG.")
                return redirect(url_for("dashboard"))
            ext = file.filename.rsplit(".", 1)[1].lower()
            filename = f"{uuid.uuid4()}.{ext}"
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(save_path)
        else:
            flash("Vui lòng tải lên ảnh, chụp từ camera hoặc vẽ biểu trưng.")
            return redirect(url_for("dashboard"))

        with Image.open(save_path) as img:
            img.verify()

        result = recognize_symbol(save_path)
        symbols = load_symbols()

        return render_template(
            "dashboard.html",
            symbols=symbols,
            result=result,
            uploaded_image=url_for("static", filename="uploads/" + filename)
        )

    except Exception as e:
        if os.path.exists(save_path):
            os.remove(save_path)
        flash(f"Không thể xử lý ảnh ({str(e)}). Vui lòng thử lại.")
        return redirect(url_for("dashboard"))


@app.route("/api/recognize", methods=["POST"])
@login_required
def api_recognize():
    """API thời gian thực cho Camera và Bảng vẽ Canvas."""
    data = request.get_json(silent=True) or {}
    image_base64 = data.get("image_base64", "").strip()

    if not image_base64:
        return jsonify({"success": False, "message": "Không nhận được dữ liệu hình ảnh."}), 400

    if "," in image_base64:
        image_base64 = image_base64.split(",", 1)[1]

    filename = f"{uuid.uuid4()}.png"
    save_path = os.path.join(UPLOAD_FOLDER, filename)

    try:
        image_data = base64.b64decode(image_base64)
        with open(save_path, "wb") as f:
            f.write(image_data)

        with Image.open(save_path) as img:
            img.verify()

        result = recognize_symbol(save_path)
        result["uploaded_image"] = url_for("static", filename="uploads/" + filename)
        return jsonify(result)

    except Exception as e:
        if os.path.exists(save_path):
            os.remove(save_path)
        return jsonify({"success": False, "message": f"Lỗi xử lý: {str(e)}"}), 500


@app.route("/api/chat", methods=["POST"])
def api_chat():
    """API Trợ lý AI Y tế Lâm sàng phục vụ hỏi đáp trực tuyến."""
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()
    history = data.get("history", [])

    if not message:
        return jsonify({
            "success": False,
            "reply": "Vui lòng nhập câu hỏi y tế hoặc tên biểu trưng bạn cần tìm hiểu."
        }), 400

    result = answer_clinical_chat(message, history)
    return jsonify(result)


@app.route("/symbols/add", methods=["POST"])
@login_required
def add_symbol():
    """Thêm biểu trưng mới vào thư viện (Feature 5 - Admin CRUD)."""
    name = request.form.get("name", "").strip()
    category = request.form.get("category", "Chăm sóc lâm sàng").strip()
    description = request.form.get("description", "").strip()
    clinical_meaning = request.form.get("clinical_meaning", "").strip()
    related_input = request.form.get("related", "").strip()
    file = request.files.get("symbol_file")

    if not name or not file or file.filename == "":
        flash("Vui lòng nhập tên biểu trưng và chọn file ảnh ký hiệu.")
        return redirect(url_for("library"))

    if not allowed_file(file.filename):
        flash("File ảnh phải có định dạng PNG hoặc JPG.")
        return redirect(url_for("library"))

    try:
        symbols = load_symbols()
        # Tìm ID tiếp theo (ví dụ SYM013)
        max_num = 0
        for s in symbols:
            s_id = s.get("id", "")
            if s_id.startswith("SYM"):
                try:
                    num = int(s_id.replace("SYM", ""))
                    if num > max_num:
                        max_num = num
                except ValueError:
                    pass
        new_id = f"SYM{str(max_num + 1).zfill(3)}"
        image_filename = f"{new_id}.png"
        image_save_path = os.path.join(SYMBOLS_FOLDER, image_filename)

        # Lưu ảnh và chuyển thành ảnh vuông chuẩn hóa
        file.save(image_save_path)

        related_list = [r.strip() for r in related_input.split(",") if r.strip()]
        if not related_list:
            related_list = ["SYM001", "SYM002"]

        new_symbol = {
            "id": new_id,
            "name": name,
            "category": category,
            "description": description or f"Biểu trưng minh họa {name}.",
            "clinical_meaning": clinical_meaning or f"Liên quan đến {name} trong quy trình khám chữa bệnh lâm sàng.",
            "related": related_list,
            "image": image_filename
        }

        symbols.append(new_symbol)
        with open(SYMBOLS_PATH, "w", encoding="utf-8") as f:
            json.dump(symbols, f, ensure_ascii=False, indent=2)

        flash(f"Đã thêm thành công biểu trưng '{name}' (Mã: {new_id}) vào thư viện!")
    except Exception as e:
        flash(f"Lỗi khi thêm biểu trưng: {str(e)}")

    return redirect(url_for("library"))


@app.route("/symbols/delete/<symbol_id>", methods=["POST"])
@login_required
def delete_symbol(symbol_id):
    """Xóa biểu trưng tùy biến khỏi thư viện (Feature 5)."""
    try:
        symbols = load_symbols()
        filtered = [s for s in symbols if s["id"] != symbol_id]
        if len(filtered) == len(symbols):
            flash("Không tìm thấy biểu trưng cần xóa.")
        else:
            with open(SYMBOLS_PATH, "w", encoding="utf-8") as f:
                json.dump(filtered, f, ensure_ascii=False, indent=2)
            flash(f"Đã xóa biểu trưng {symbol_id} khỏi thư viện!")
    except Exception as e:
        flash(f"Lỗi khi xóa biểu trưng: {str(e)}")

    return redirect(url_for("library"))


@app.route("/network")
@login_required
def network():
    try:
        symbols = load_symbols()
    except (json.JSONDecodeError, OSError):
        symbols = []
        flash("Không thể đọc dữ liệu biểu trưng.")

    return render_template(
        "network.html",
        symbols=symbols
    )


@app.route("/library")
@login_required
def library():
    try:
        symbols = load_symbols()
    except (json.JSONDecodeError, OSError):
        symbols = []
        flash("Không thể đọc dữ liệu biểu trưng.")

    return render_template(
        "library.html",
        symbols=symbols
    )


@app.route("/logout")
def logout():
    session.clear()
    flash("Bạn đã đăng xuất an toàn.")
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5001))
    app.run(debug=True, port=port)
