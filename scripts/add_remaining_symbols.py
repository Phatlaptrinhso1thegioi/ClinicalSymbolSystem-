# -*- coding: utf-8 -*-
"""
Add remaining symbols from the Universal Healthcare Symbols PDF:
- FA11: Social Services (Công tác Xã hội & Hỗ trợ Gia đình)
- FA12: Chapel (Nhà nguyện / Không gian Tâm linh)
- MA02: Mammography (Chụp X-quang Tuyến vú Kỹ thuật số)
- MA06: Fluoroscopy & Patient Care (Thấu thị & Chăm sóc Điều trị)
- MA10: CAT Scanner (Máy chụp Cắt lớp Vi tính CAT)
"""
import os
import json
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SYMBOLS_DIR = os.path.join(BASE_DIR, "data", "symbols")
JSON_PATH = os.path.join(BASE_DIR, "data", "symbols.json")

ADDITIONAL_SYMBOLS = [
    {
        "id": "FA11",
        "code": "FA11",
        "name": "Công tác Xã hội & Trợ giúp Người bệnh",
        "category": "Cơ sở & Hành chính",
        "description": "Biểu trưng đôi bàn tay nâng đỡ bảo bọc gia đình đại diện cho phòng Công tác Xã hội.",
        "clinical_meaning": "Hỗ trợ người bệnh có hoàn cảnh khó khăn, kết nối nhà hảo tâm, tư vấn tâm lý xã hội và quyền lợi BHYT.",
        "related": ["FA03", "FA10", "FA07"],
        "shape": "social_services"
    },
    {
        "id": "FA12",
        "code": "FA12",
        "name": "Nhà nguyện & Không gian Tâm linh",
        "category": "Cơ sở & Hành chính",
        "description": "Biểu trưng tháp chuông nhà nguyện và chữ thập đại diện không gian tâm linh bệnh viện.",
        "clinical_meaning": "Nơi cầu nguyện, tĩnh tâm và hỗ trợ tinh thần cho thân nhân và bệnh nhân nặng.",
        "related": ["FA04", "CM16", "CM03"],
        "shape": "chapel"
    },
    {
        "id": "MA02",
        "code": "MA02",
        "name": "X-quang Tuyến vú (Mammography)",
        "category": "Chẩn đoán hình ảnh",
        "description": "Biểu trưng máy chụp nhũ ảnh kỹ thuật số tầm soát sớm u xơ và ung thư tuyến vú.",
        "clinical_meaning": "Tầm soát định kỳ u vú, phát hiện vi vôi hóa ác tính giai đoạn sớm ở phụ nữ.",
        "related": ["CM24", "CM14", "MA05"],
        "shape": "mammography"
    },
    {
        "id": "MA06",
        "code": "MA06",
        "name": "Thấu thị & Chăm sóc Điều trị",
        "category": "Chẩn đoán hình ảnh",
        "description": "Biểu trưng màn hình tăng sáng huỳnh quang thấu thị (Fluoroscopy) và chăm sóc bệnh nhân.",
        "clinical_meaning": "Ghi hình động thời gian thực phục vụ can thiệp đường tiêu hóa, đặt catheter và nắn chỉnh xương.",
        "related": ["MA01", "MA03", "CM31"],
        "shape": "fluoroscopy"
    },
    {
        "id": "MA10",
        "code": "MA10",
        "name": "Máy quét CAT Scanner",
        "category": "Chẩn đoán hình ảnh",
        "description": "Huy hiệu định danh phòng chụp cắt lớp điện toán vi tính CAT (Computerized Axial Tomography).",
        "clinical_meaning": "Thực hiện khảo sát mặt cắt ngang trục cơ thể, định vị tổn thương sọ não và ngực bụng cấp cứu.",
        "related": ["MA04", "MA09", "FA01"],
        "shape": "cat_badge"
    }
]

def draw_symbol_image(shape_type, save_path):
    img = Image.new("RGB", (256, 256), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    color = (0, 0, 0)

    if shape_type == "social_services":
        # Two supporting hands cradling 3 family figures
        # Hands curve at bottom
        draw.arc([30, 110, 226, 230], start=10, end=170, fill=color, width=16)
        # Father figure
        draw.ellipse([80, 80, 110, 110], fill=color)
        draw.rectangle([78, 115, 112, 175], fill=color)
        # Mother figure
        draw.ellipse([146, 80, 176, 110], fill=color)
        draw.rectangle([144, 115, 178, 175], fill=color)
        # Child figure in middle
        draw.ellipse([115, 110, 141, 136], fill=color)
        draw.rectangle([115, 140, 141, 185], fill=color)

    elif shape_type == "chapel":
        # Steeple chapel building
        # Triangular roof / steeple
        draw.polygon([(128, 40), (80, 110), (176, 110)], fill=color)
        # Small steeple cross
        draw.rectangle([124, 25, 132, 50], fill=color)
        draw.rectangle([118, 32, 138, 38], fill=color)
        # Main building body
        draw.rectangle([80, 110, 176, 215], fill=color)
        # Arched door (white cutout)
        draw.ellipse([112, 145, 144, 175], fill=(255, 255, 255))
        draw.rectangle([112, 160, 144, 215], fill=(255, 255, 255))

    elif shape_type == "mammography":
        # Machine frame with vertical column and compression paddle
        draw.rectangle([60, 40, 85, 215], fill=color)
        draw.rectangle([85, 70, 165, 88], fill=color)
        draw.rectangle([85, 130, 165, 148], fill=color)
        # Patient torso outline
        draw.ellipse([175, 55, 205, 85], fill=color) # head
        draw.rectangle([170, 90, 200, 215], fill=color) # body
        # Breast curve facing compression plate
        draw.arc([145, 95, 185, 140], start=90, end=270, fill=color, width=12)

    elif shape_type == "fluoroscopy":
        # Upright fluoroscopy stand and patient examination
        draw.rectangle([55, 45, 80, 215], fill=color)
        draw.rectangle([80, 90, 135, 105], fill=color)
        # Patient silhouette standing
        draw.ellipse([145, 50, 175, 80], fill=color)
        draw.rectangle([140, 85, 180, 215], fill=color)
        # Detector screen
        draw.rectangle([185, 75, 205, 170], fill=color)

    elif shape_type == "cat_badge":
        # Large rounded card with text CAT and finger pointing / scanner touch
        draw.rounded_rectangle([45, 45, 211, 211], radius=24, outline=color, width=12)
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 52)
        except:
            font = ImageFont.load_default()
        draw.text((70, 78), "CAT", fill=color, font=font)
        # Finger touching icon at bottom right
        draw.ellipse([145, 150, 165, 170], fill=color)
        draw.rectangle([150, 165, 160, 195], fill=color)

    img.save(save_path)
    print(f"Generated: {save_path}")

# Load existing JSON
with open(JSON_PATH, "r", encoding="utf-8") as f:
    symbols = json.load(f)

existing_ids = {s["id"] for s in symbols}

for item in ADDITIONAL_SYMBOLS:
    sym_id = item["id"]
    filename = f"{sym_id.lower()}.png"
    img_path = os.path.join(SYMBOLS_DIR, filename)
    draw_symbol_image(item["shape"], img_path)

    if sym_id not in existing_ids:
        symbols.append({
            "id": sym_id,
            "code": item["code"],
            "name": item["name"],
            "category": item["category"],
            "description": item["description"],
            "clinical_meaning": item["clinical_meaning"],
            "related": item["related"],
            "image": filename
        })
        existing_ids.add(sym_id)

with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(symbols, f, ensure_ascii=False, indent=2)

print(f"Total symbols now in catalog: {len(symbols)}")
