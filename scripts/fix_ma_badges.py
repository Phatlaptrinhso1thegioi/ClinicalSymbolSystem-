import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SYMBOLS_DIR = os.path.join(BASE_DIR, "data", "symbols")

def draw_screen_badge(text, save_path):
    img = Image.new("RGB", (256, 256), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    color = (0, 0, 0)
    
    # Outer monitor frame
    draw.rounded_rectangle([45, 45, 211, 211], radius=24, outline=color, width=12)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 46)
    except:
        font = ImageFont.load_default()
        
    draw.text((70, 78), text, fill=color, font=font)
    # Finger pointing / touch icon at bottom right
    draw.ellipse([145, 145, 165, 165], fill=color)
    draw.rectangle([150, 160, 160, 195], fill=color)
    
    img.save(save_path)
    print(f"Updated {save_path} with text {text}")

draw_screen_badge("MRI", os.path.join(SYMBOLS_DIR, "ma07.png"))
draw_screen_badge("PET", os.path.join(SYMBOLS_DIR, "ma08.png"))
draw_screen_badge("CT", os.path.join(SYMBOLS_DIR, "ma09.png"))
