# -*- coding: utf-8 -*-
"""
=============================================================================
CLINICAL AI CHATBOT ENGINE
Hệ thống Trợ lý Trí tuệ Nhân tạo Lâm sàng & Hướng dẫn Ký hiệu Y tế
=============================================================================
Tính năng:
1. Phân tích ngữ nghĩa câu hỏi y khoa & tra cứu thông minh 58 biểu trưng quốc tế.
2. Cung cấp chỉ dẫn lâm sàng, phác đồ cấp cứu khẩn cấp (Code Blue, CPR, ABCDE).
3. Cảnh báo các dấu hiệu sinh tồn nguy kịch (Red Flags) & thang điểm MEWS.
4. Tích hợp trực tiếp Google Gemini API (khi có GEMINI_API_KEY) và tự động
   dự phòng bằng Hệ tri thức Y khoa chuyên sâu ngoại tuyến.
=============================================================================
"""

import os
import re
import json
import urllib.request
import urllib.error
from recognition import CLINICAL_KNOWLEDGE_BASE, DEFAULT_ASSISTANT_DATA

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SYMBOLS_PATH = os.path.join(BASE_DIR, "data", "symbols.json")


def load_symbols_catalog():
    if not os.path.exists(SYMBOLS_PATH):
        return []
    try:
        with open(SYMBOLS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            if isinstance(data, dict) and isinstance(data.get("symbols"), list):
                return data["symbols"]
    except Exception:
        pass
    return []


SYMBOLS_CATALOG = load_symbols_catalog()
SYMBOLS_MAP = {s["id"].upper(): s for s in SYMBOLS_CATALOG}


# =============================================================================
# GEMINI API INTEGRATION HELPER
# =============================================================================
def query_gemini_api(prompt, api_key, history=None):
    """Gọi trực tiếp Google Gemini API thông qua REST chuẩn (không cần thư viện bên ngoài)."""
    endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

    system_instruction = (
        "Bạn là Trợ lý AI Y tế Lâm sàng của hệ thống 'Clinical Symbol System'. "
        "Nhiệm vụ của bạn là tư vấn chuyên môn y tế, giải mã các biểu tượng ký hiệu y tế chuẩn quốc tế (SEGD & HCONC), "
        "hướng dẫn quy trình cấp cứu, cảnh báo dấu hiệu nguy kịch (Red Flags), thang điểm cảnh báo sớm MEWS "
        "và hỗ trợ định hướng các chuyên khoa bệnh viện. "
        "Trả lời bằng tiếng Việt chuyên nghiệp, ân cần, định dạng Markdown rõ ràng với tiêu đề, danh sách từng bước và lưu ý an toàn. "
        "Luôn kèm theo khuyến cáo: 'Thông tin mang tính chất tham khảo chuyên môn và hỗ trợ giao tiếp lâm sàng, không thay thế chẩn đoán y khoa trực tiếp của bác sĩ.'"
    )

    contents = []
    if history:
        for msg in history[-6:]:
            role = "user" if msg.get("role") in ["user", "human"] else "model"
            contents.append({
                "role": role,
                "parts": [{"text": msg.get("content", "")}]
            })

    contents.append({
        "role": "user",
        "parts": [{"text": prompt}]
    })

    payload = {
        "system_instruction": {
            "parts": [{"text": system_instruction}]
        },
        "contents": contents,
        "generationConfig": {
            "temperature": 0.4,
            "maxOutputTokens": 1024,
            "topP": 0.95
        }
    }

    req = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=10) as resp:
        res_data = json.loads(resp.read().decode("utf-8"))
        text = res_data["candidates"][0]["content"]["parts"][0]["text"]
        return text.strip()


# =============================================================================
# LOCAL CLINICAL REASONING ENGINE (HỆ TRI THỨC Y KHOA NỘI TẠI)
# =============================================================================
def search_matching_symbols(query_text):
    """Tìm kiếm các biểu trưng liên quan trong catalog 58 ký hiệu."""
    matches = []
    q_norm = query_text.lower().strip()

    # 1. Tìm theo ID chính xác (CM01, FA02, MA03, SYM004...)
    ids_found = re.findall(r"\b(CM\d{2}|FA\d{2}|MA\d{2}|SYM\d{3})\b", query_text, re.IGNORECASE)
    for sid in ids_found:
        sid_up = sid.upper()
        if sid_up in SYMBOLS_MAP and SYMBOLS_MAP[sid_up] not in matches:
            matches.append(SYMBOLS_MAP[sid_up])

    # 2. Tìm theo từ khóa chuyên môn
    keyword_map = {
        "chữ thập": ["CM01", "SYM004", "FA01"],
        "cấp cứu": ["SYM004", "FA01", "FA02", "SYM005"],
        "tim mạch": ["CM23", "SYM001"],
        "ecg": ["SYM001", "CM23"],
        "điện tim": ["SYM001", "CM23"],
        "huyết áp": ["SYM002"],
        "nhiệt độ": ["SYM003"],
        "sốt": ["SYM003"],
        "nha khoa": ["CM29"],
        "răng": ["CM29"],
        "mắt": ["CM15"],
        "khúc xạ": ["CM15"],
        "thần kinh": ["CM17", "CM16"],
        "não": ["CM17", "MA03"],
        "x quang": ["MA01"],
        "mri": ["MA03", "MA07"],
        "ct": ["MA09", "MA10"],
        "siêu âm": ["MA05"],
        "nhà thuốc": ["CM06"],
        "thuốc": ["CM06"],
        "viên thuốc": ["CM06"],
        "tiêm": ["CM09"],
        "vắc xin": ["CM09"],
        "xét nghiệm": ["CM12", "CM13"],
        "hô hấp": ["CM20"],
        "phổi": ["CM21"],
        "thận": ["CM22"],
        "tiêu hóa": ["CM07"],
        "da liễu": ["CM18"],
        "tai mũi họng": ["CM19"],
        "thu ngân": ["FA07"],
        "viện phí": ["FA07"],
        "tiếp đón": ["FA03"],
        "hồ sơ": ["FA06"],
        "thư viện": ["FA08"]
    }

    for kw, sym_ids in keyword_map.items():
        if kw in q_norm:
            for sid in sym_ids:
                if sid in SYMBOLS_MAP and SYMBOLS_MAP[sid] not in matches:
                    matches.append(SYMBOLS_MAP[sid])

    # Nếu không tìm thấy bằng keyword_map, duyệt tên và mô tả
    if not matches:
        for s in SYMBOLS_CATALOG:
            name = s.get("name", "").lower()
            desc = s.get("description", "").lower()
            meaning = s.get("clinical_meaning", "").lower()
            if any(term in name or term in desc or term in meaning for term in q_norm.split() if len(term) >= 3):
                matches.append(s)
                if len(matches) >= 4:
                    break

    return matches[:4]


def generate_local_clinical_response(user_message):
    """Sinh câu trả lời thông minh dựa trên Hệ tri thức Y tế Lâm sàng."""
    q_norm = user_message.lower().strip()
    symbols = search_matching_symbols(user_message)
    suggested = [
        "Quy trình cấp cứu khẩn cấp Code Blue?",
        "Ý nghĩa biểu trưng y tế CM01?",
        "Chỉ số sinh tồn huyết áp nguy kịch?",
        "Cách vẽ nét biểu trưng để AI nhận diện đúng?"
    ]

    # --- CHỦ ĐỀ 1: HƯỚNG DẪN BIỂU TƯỢNG CỤ THỂ ---
    if symbols and any(code in q_norm for code in ["cm", "fa", "ma", "sym", "ký hiệu", "biểu tượng", "mã"]):
        primary = symbols[0]
        sid = primary["id"]
        know = CLINICAL_KNOWLEDGE_BASE.get(sid, DEFAULT_ASSISTANT_DATA)
        
        reply = f"### 🩺 Thông tin Chuyên môn: {primary['name']} (`{sid}`)\n\n"
        reply += f"**Phân loại:** {primary.get('category', 'Lâm sàng')} | **Quy chuẩn:** SEGD & HCONC International Healthcare Standard\n\n"
        reply += f"**Mô tả:** {primary.get('description', '')}\n\n"
        reply += f"**Ý nghĩa lâm sàng:** {primary.get('clinical_meaning', know.get('normal_range', ''))}\n\n"

        if "normal_range" in know and know["normal_range"]:
            reply += f"**📊 Giá trị tham chiếu / Tiêu chuẩn:** {know['normal_range']}\n\n"

        if "red_flags" in know and know["red_flags"]:
            reply += "🚨 **Dấu hiệu cảnh báo nguy kịch (Red Flags):**\n"
            for rf in know["red_flags"]:
                reply += f"- {rf}\n"
            reply += "\n"

        if "emergency_protocols" in know and know["emergency_protocols"]:
            reply += "📋 **Phác đồ xử trí khuyến nghị:**\n"
            for p in know["emergency_protocols"]:
                reply += f"- {p}\n"
            reply += "\n"

        if "safety_checklist" in know and know["safety_checklist"]:
            reply += "✅ **Checklist an toàn người bệnh:**\n"
            for sc in know["safety_checklist"]:
                reply += f"- {sc}\n"
            reply += "\n"

        reply += "> *Lưu ý: Thông tin trên hỗ trợ định hướng và hướng dẫn ca trực, luôn phối hợp hội chẩn bác sĩ chuyên khoa.*"
        
        suggested = [
            f"Phác đồ xử trí cấp cứu của {primary['name']}?",
            f"Các biểu trưng liên quan đến {primary.get('category')}?",
            "Quy trình cấp cứu ngừng tuần hoàn CPR?",
            "Hướng dẫn quét camera nhận diện biểu trưng"
        ]
        return reply, symbols, suggested

    # --- CHỦ ĐỀ 2: CẤP CỨU NGỪNG TIM, CPR, CODE BLUE ---
    if any(k in q_norm for k in ["cpr", "ngừng tim", "ép tim", "code blue", "sốc điện", "hồi sinh", "cấp cứu"]):
        reply = """### 🚨 Phác đồ Cấp cứu Ngừng Tuần hoàn Hô hấp (Code Blue Protocol)

Theo khuyến cáo quốc tế **AHA / ERC Guidelines**:

1. **Bước 1: Tiếp cận & Đánh giá an toàn**
   - Kiểm tra hiện trường an toàn.
   - Lay gọi người bệnh, kiểm tra mạch cảnh / mạch bẹn trong vòng **không quá 10 giây**.
   - Nếu không thở hoặc thở ngáp cá: **KÍCH HOẠT CODE BLUE NGAY LẬP TỨC**.

2. **Bước 2: Ép tim chất lượng cao (High-Quality CPR)**
   - Vị trí: $1/2$ dưới xương ức.
   - Tần số: **$100 - 120$ lần/phút**.
   - Độ sâu: **$5 - 6$ cm** ở người lớn, để ngực nở lại hoàn toàn sau mỗi lần ép.
   - Tỷ lệ ép tim / thổi ngạt: **$30 : 2$** (nếu chưa đặt nội khí quản).
   - Hạn chế tối đa gián đoạn ép tim ($< 10$ giây).

3. **Bước 3: Khử rung tim sớm (Early Defibrillation)**
   - Gắn máy AED hoặc máy sốc điện 2 pha (Biphasic).
   - Nhịp sốc điện được: **Rung thất (VF)** và **Nhịp nhanh thất mất mạch (pVT)** (Liều khởi đầu: $150 - 200\\text{ J}$).
   - Nhịp không sốc: **Vô tâm thu (Asystole)** và **Phân ly điện cơ (PEA)** $\\to$ Tiếp tục ép tim ngay và tiêm Adrenaline $1\\text{mg}$ TM mỗi $3 - 5$ phút.

4. **Bước 4: Thiết lập đường thở & Đường truyền**
   - Đặt canun, bóp bóng Ambu qua mặt nạ oxy $100\\%$.
   - Lập $2$ đường truyền tĩnh mạch lớn ngoại vi hoặc đường truyền trong xương.
"""
        suggested = [
            "Biểu trưng cấp cứu SYM004 và CM01?",
            "Dấu hiệu cảnh báo nhồi máu cơ tim?",
            "Thang điểm cảnh báo sớm MEWS?",
            "Quy tắc FAST nhận biết đột quỵ?"
        ]
        return reply, symbols or [SYMBOLS_MAP["SYM004"], SYMBOLS_MAP["CM01"], SYMBOLS_MAP["FA01"]], suggested

    # --- CHỦ ĐỀ 3: HUYẾT ÁP & DẤU HIỆU SINH TỒN ---
    if any(k in q_norm for k in ["huyết áp", "tụt huyết áp", "cao huyết áp", "mạch", "sinh tồn", "nhiệt độ", "spo2"]):
        reply = """### 📊 Chỉ dẫn Lâm sàng: Dấu hiệu Sinh tồn & Huyết áp Động mạch (NIBP)

*Biểu trưng tương ứng: `SYM001` (Nhịp tim) & `SYM002` (Huyết áp)*

#### 1. Các giá trị tiêu chuẩn ở người trưởng thành:
- **Huyết áp tối ưu:** Tâm thu $90 - 120\\text{ mmHg}$, Tâm trương $60 - 80\\text{ mmHg}$.
- **Nhịp tim:** $60 - 100$ nhịp/phút (bpm), nhịp xoang đều.
- **SpO2 khí trời:** $95\\% - 100\\%$.
- **Thân nhiệt:** $36.5^\\circ\\text{C} - 37.2^\\circ\\text{C}$.

#### 2. Ngưỡng báo động đỏ (Red Flags):
- **Huyết áp tụt kịch phát:** Huyết áp tâm thu $< 90\\text{ mmHg}$ hoặc huyết áp trung bình (MAP) $< 65\\text{ mmHg}$ $\\to$ Nguy cơ sốc (nhiễm khuẩn, mất máu, phản vệ, tim).
- **Cơn tăng huyết áp khẩn cấp:** Huyết áp $> 180/120\\text{ mmHg}$ kèm tổn thương cơ quan đích (đau ngực, nhìn mờ, co giật, khó thở).

#### 3. Xử trí bước đầu khi tụt huyết áp:
- Đặt người bệnh nằm đầu bằng, kê cao chân $30^\\circ$ (tư thế Trendelenburg cải tiến).
- Bắt đầu bù dịch tinh thể đẳng trương (NaCl $0.9\\%$ hoặc Ringer Lactate $500\\text{ml}$ truyền nhanh) nếu không có dấu hiệu suy tim/phù phổi.
- Đánh giá tri giác, gọi hỗ trợ kíp Hồi sức cấp cứu.
"""
        suggested = [
            "Ý nghĩa biểu trưng SYM002 Huyết áp?",
            "Phác đồ xử trí cơn đau ngực cấp?",
            "Thang điểm cảnh báo sớm MEWS?",
            "Cách quét camera nhận diện biểu trưng sinh tồn"
        ]
        return reply, symbols or [SYMBOLS_MAP["SYM002"], SYMBOLS_MAP["SYM001"]], suggested

    # --- CHỦ ĐỀ 4: ĐAU NGỰC, NHỒI MÁU CƠ TIM, TIM MẠCH ---
    if any(k in q_norm for k in ["đau ngực", "nhồi máu", "tim mạch", "stemi", "mạch vành"]):
        reply = """### ❤️ Chỉ dẫn Xử trí Cơn Đau thắt ngực Cấp tính & Hội chứng Vành cấp

*Biểu trưng tương ứng: `CM23` (Khoa Tim mạch & Can thiệp)*

#### 1. Dấu hiệu nhận biết điển hình:
- Đau thắt, đè nặng sau xương ức, kéo dài $> 20$ phút, lan lên cằm, vai trái hoặc dọc cánh tay trái.
- Kèm vã mồ hôi lạnh, khó thở dữ dội, hồi hộp, hoa mắt chóng mặt.

#### 2. Phác đồ tiếp cận ban đầu (MONAC):
- **O (Oxygen):** Thở oxy gọng kính $2 - 4\\text{ L/phút}$ nếu $\\text{SpO}_2 < 90\\%$.
- **A (Aspirin):** Cho nhai ngậm ngay $162 - 325\\text{mg}$ Aspirin không bao.
- **N (Nitroglycerin):** Xịt dưới lưỡi $0.4\\text{mg}$ mỗi 5 phút (tối đa 3 lần) nếu $\\text{HA tâm thu} > 90\\text{ mmHg}$.
- **M (Morphine):** Giảm đau bằng Morphine sulfate $2 - 4\\text{mg}$ tiêm TM chậm nếu đau ngực dữ dội không giảm.
- **C (Clopidogrel / Ticagrelor):** Liều nạp theo chỉ định trước can thiệp.

#### 3. Hành động khẩn cấp:
- Ghi điện tâm đồ 12 chuyển đạo trong vòng **10 phút đầu** tiếp cận.
- Kích hoạt phòng can thiệp tim mạch (Cath Lab) nếu có đoạn ST chênh lên (STEMI).
"""
        suggested = [
            "Xem chi tiết biểu trưng CM23 Tim mạch?",
            "Quy trình cấp cứu Code Blue?",
            "Chỉ số huyết áp nguy kịch?",
            "Tra cứu biểu trưng Khoa Chẩn đoán hình ảnh"
        ]
        return reply, symbols or [SYMBOLS_MAP["CM23"], SYMBOLS_MAP["SYM001"]], suggested

    # --- CHỦ ĐỀ 5: ĐỘT QUỴ, TAI BIẾN, THẦN KINH ---
    if any(k in q_norm for k in ["đột quỵ", "tai biến", "liệt", "méo miệng", "fast", "não"]):
        reply = """### 🧠 Quy tắc FAST & Nhận diện Cấp cứu Đột quỵ Não (Stroke)

*Biểu trưng tương ứng: `CM17` (Khoa Thần kinh) & `MA03` (Chụp MRI Não)*

#### 1. Quy tắc FAST nhận biết sớm:
- **F (Face - Mặt):** Miệng bị méo, nụ cười lệch một bên.
- **A (Arms - Tay):** Yếu hoặc liệt một bên tay chân, không thể nhấc đều 2 tay.
- **S (Speech - Lời nói):** Nói đớ, nói ngọng, không diễn đạt được hoặc không hiểu lời nói.
- **T (Time - Thời gian):** Kích hoạt hệ thống Cấp cứu đột quỵ ngay. **Khung giờ vàng là $< 4.5$ giờ** để dùng thuốc tiêu sợi huyết (rTPA) hoặc $< 6 - 24$ giờ để lấy huyết khối cơ học.

#### 2. Lưu ý sống còn:
- **KHÔNG** tự ý cho người bệnh uống thuốc hạ huyết áp tại nhà.
- **KHÔNG** chích máu đầu ngón tay hay cạo gió.
- Đặt bệnh nhân nằm nghiêng an toàn nếu có nôn ói để tránh sặc đường thở.
- Chuyển thẳng cơ sở y tế có máy chụp CT/MRI và đơn vị Đột quỵ.
"""
        suggested = [
            "Xem biểu trưng CM17 Thần kinh?",
            "Biểu trưng MA03 Chụp MRI Não?",
            "Thang điểm MEWS phân loại bệnh nhân?",
            "Quy trình cấp cứu Code Blue?"
        ]
        return reply, symbols or [SYMBOLS_MAP["CM17"], SYMBOLS_MAP["MA03"]], suggested

    # --- CHỦ ĐỀ 6: HƯỚNG DẪN DÙNG HỆ THỐNG (VẼ TAY, CAMERA, THƯ VIỆN) ---
    if any(k in q_norm for k in ["vẽ", "bảng vẽ", "camera", "quét", "chụp", "tải ảnh", "sử dụng", "hướng dẫn"]):
        reply = """### 💡 Hướng dẫn Tối ưu Hóa Nhận diện AI trên Hệ thống

Hệ thống hỗ trợ 3 phương thức đầu vào được tối ưu bằng **Động cơ Thị giác AI Đa Phương thức (HOG-128 + Chamfer Fusion)**:

1. **✏️ Bảng vẽ tay cảm ứng (Hand-drawn Canvas):**
   - **Vị trí:** Nhấn tab *'Bảng vẽ tay'* trên Dashboard.
   - **Mẹo nhận diện chính xác:**
     - Nên chọn **Nét vừa (12px)** hoặc **Nét đậm (20px)** để đường nét rõ ràng.
     - Vẽ biểu trưng căn vào giữa tâm dấu cộng (+) của khung vẽ.
     - Vẽ đầy đủ các nét chính (ví dụ: chữ thập thì vẽ 2 nét cắt nhau; trái tim thì vẽ vòng khép kín).
   - Nhấn nút **'⚡ Nhận diện nét vẽ'** để AI tự động bão hòa nét và so khớp.

2. **📸 Quét Camera trực tiếp (Live Camera Scanner):**
   - Bấm *'Bật Camera'* và cấp quyền truy cập trình duyệt.
   - Đặt bảng ký hiệu y tế lọt trọn vào khung ngắm laser hình vuông ở giữa.
   - Giữ camera thẳng góc, tránh lóa sáng và bấm *'📸 Chụp & Quét Biểu trưng'*.

3. **📁 Tải ảnh tệp:**
   - Hỗ trợ định dạng PNG, JPG, JPEG dung lượng tối đa 5MB.
"""
        suggested = [
            "Thử vẽ chữ thập y tế CM01?",
            "Hệ thống có bao nhiêu biểu trưng?",
            "Quy trình cấp cứu Code Blue?",
            "Tra cứu biểu trưng cấp cứu SYM004"
        ]
        return reply, symbols or [SYMBOLS_MAP["CM01"], SYMBOLS_MAP["SYM004"]], suggested

    # --- CHỦ ĐỀ MẶC ĐỊNH / CHÀO HỎI ---
    reply = f"""### 👋 Chào bạn! Tôi là Trợ lý AI Y tế Lâm sàng

Tôi được huấn luyện với **Cơ sở tri thức 58 Biểu trưng Y tế Chuẩn Quốc tế (SEGD & HCONC)** cùng các hướng dẫn chuyên môn cấp cứu lâm sàng.

Bạn có thể đặt bất kỳ câu hỏi nào về:
1. **Tra cứu ý nghĩa biểu trưng y tế:** Chữ thập (`CM01`), cấp cứu (`SYM004`), tim mạch (`CM23`), nha khoa (`CM29`), mắt (`CM15`), X-quang (`MA01`), v.v.
2. **Quy trình & Phác đồ cấp cứu:** Hồi sức tim phổi CPR, Code Blue, tiếp cận người bệnh theo nguyên tắc ABCDE.
3. **Cảnh báo dấu hiệu sinh tồn:** Ngưỡng nguy kịch của huyết áp, nhịp tim, nhịp thở, SpO2.
4. **Hướng dẫn sử dụng:** Mẹo vẽ tay, quét camera nhận diện chính xác.

*Bạn muốn tìm hiểu biểu trưng hoặc quy trình lâm sàng nào?*
"""
    return reply, symbols or [SYMBOLS_MAP["CM01"], SYMBOLS_MAP["SYM004"], SYMBOLS_MAP["CM23"]], suggested


# =============================================================================
# MAIN ENTRY POINT CHO API CHATBOT
# =============================================================================
def answer_clinical_chat(user_message, history=None):
    """
    Hàm xử lý chính cho endpoint /api/chat.
    Tự động thử Google Gemini API nếu có cấu hình key;
    Nếu không có key hoặc xảy ra lỗi kết nối, chuyển mượt mà sang Hệ tri thức Y tế Nội tại.
    """
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    symbols = search_matching_symbols(user_message)
    source = "Hệ tri thức Lâm sàng SEGD & HCONC (AI Vision Core)"

    if api_key:
        try:
            gemini_reply = query_gemini_api(user_message, api_key, history)
            if gemini_reply:
                suggested = [
                    "Quy trình cấp cứu Code Blue?",
                    "Ý nghĩa biểu trưng y tế CM01?",
                    "Dấu hiệu cảnh báo nguy kịch Red Flags?",
                    "Hướng dẫn vẽ biểu trưng nhận diện đúng"
                ]
                return {
                    "success": True,
                    "reply": gemini_reply,
                    "symbols": format_symbol_cards(symbols),
                    "suggested_questions": suggested,
                    "source": "Google Gemini 1.5 Flash (AI Medical Specialist)"
                }
        except Exception:
            # Fallback to local clinical reasoning engine
            pass

    reply_text, res_symbols, suggested_qs = generate_local_clinical_response(user_message)
    return {
        "success": True,
        "reply": reply_text,
        "symbols": format_symbol_cards(res_symbols),
        "suggested_questions": suggested_qs,
        "source": source
    }


def format_symbol_cards(symbols_list):
    """Format danh sách biểu trưng thành card JSON thân thiện với UI."""
    cards = []
    for s in symbols_list[:4]:
        cards.append({
            "id": s.get("id"),
            "name": s.get("name"),
            "category": s.get("category", "Lâm sàng"),
            "image": f"/symbol-image/{s.get('image')}",
            "description": s.get("description", "")
        })
    return cards
