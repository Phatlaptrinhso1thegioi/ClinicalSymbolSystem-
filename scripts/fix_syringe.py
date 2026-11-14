import os
from PIL import Image, ImageDraw

SYMBOLS_DIR = "data/symbols"

img = Image.new("RGB", (256, 256), (255, 255, 255))
draw = ImageDraw.Draw(img)
color = (0, 0, 0)

# Solid Syringe
# Needle at top
draw.line([128, 20, 128, 60], fill=color, width=8)
# Needle hub / tip
draw.polygon([(118, 60), (138, 60), (128, 48)], fill=color)
# Syringe barrel (solid with graduations cutout)
draw.rectangle([100, 60, 156, 155], fill=color)
draw.line([115, 80, 140, 80], fill=(255, 255, 255), width=4)
draw.line([115, 105, 140, 105], fill=(255, 255, 255), width=4)
draw.line([115, 130, 140, 130], fill=(255, 255, 255), width=4)
# Finger flange
draw.rectangle([80, 155, 176, 170], fill=color)
# Plunger rod
draw.rectangle([120, 170, 136, 205], fill=color)
# Plunger thumb press
draw.rectangle([100, 205, 156, 220], fill=color)

img.save(os.path.join(SYMBOLS_DIR, "cm09.png"))
print("Updated cm09.png with solid syringe silhouette.")
