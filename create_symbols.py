
from PIL import Image, ImageDraw
import os

OUTPUT_DIR = "data/symbols"
SIZE = 256

os.makedirs(OUTPUT_DIR, exist_ok=True)

def new_icon():
    img = Image.new("RGB", (SIZE, SIZE), "white")
    draw = ImageDraw.Draw(img)
    return img, draw

def save(img, name):
    img.save(os.path.join(OUTPUT_DIR, name + ".png"))

# SYM001 - Nhịp tim
img, d = new_icon()
d.line([(35,130),(75,130),(95,80),(125,180),(150,105),(170,130),(220,130)],
       fill="black", width=9)
save(img, "SYM001")

# SYM002 - Huyết áp
img, d = new_icon()
d.arc((55,55,200,200), 180, 360, fill="black", width=10)
d.line((128,130,170,90), fill="black", width=8)
d.ellipse((116,118,140,142), fill="black")
d.line((55,130,55,175), fill="black", width=8)
d.line((200,130,200,175), fill="black", width=8)
save(img, "SYM002")

# SYM003 - Thân nhiệt
img, d = new_icon()
d.rounded_rectangle((108,40,148,175), radius=18, outline="black", width=9)
d.ellipse((90,150,166,226), outline="black", width=9)
d.line((128,90,128,185), fill="black", width=12)
save(img, "SYM003")

# SYM004 - Cấp cứu
img, d = new_icon()
d.rectangle((105,35,151,221), fill="black")
d.rectangle((35,105,221,151), fill="black")
save(img, "SYM004")

# SYM005 - Hồi sức
img, d = new_icon()
d.ellipse((95,45,160,110), outline="black", width=9)
d.arc((65,85,190,220), 180, 360, fill="black", width=10)
d.line((128,110,128,205), fill="black", width=10)
d.line((75,145,180,145), fill="black", width=10)
save(img, "SYM005")

# SYM006 - Cảnh báo
img, d = new_icon()
d.polygon([(128,30),(225,210),(31,210)], outline="black", fill="white")
d.line((128,90,128,150), fill="black", width=12)
d.ellipse((119,168,137,186), fill="black")
save(img, "SYM006")

# SYM007 - Xét nghiệm máu
img, d = new_icon()
d.polygon([(128,35),(65,145),(65,175)], outline="black", fill="white")
d.line((65,175,65,195,190,195,190,175), fill="black", width=9)
d.line((190,175,190,145,128,35), fill="black", width=9)
d.line((78,150,177,150), fill="black", width=8)
save(img, "SYM007")

# SYM008 - Mẫu bệnh phẩm
img, d = new_icon()
d.rounded_rectangle((75,65,180,215), radius=15, outline="black", width=9)
d.rectangle((95,35,160,70), outline="black", width=8)
d.line((85,155,170,155), fill="black", width=8)
save(img, "SYM008")

# SYM009 - Xét nghiệm
img, d = new_icon()
d.line((95,35,160,35), fill="black", width=10)
d.line((110,35,110,110,65,190), fill="black", width=9)
d.line((145,35,145,110,195,190), fill="black", width=9)
d.line((65,190,195,190), fill="black", width=9)
d.line((85,155,175,155), fill="black", width=8)
save(img, "SYM009")

# SYM010 - Thuốc
img, d = new_icon()
d.rounded_rectangle((45,85,211,170), radius=42, outline="black", width=9)
d.line((128,87,128,168), fill="black", width=9)
save(img, "SYM010")

# SYM011 - Truyền dịch
img, d = new_icon()
d.rectangle((75,55,180,190), outline="black", width=9)
d.line((128,25,128,55), fill="black", width=8)
d.line((128,190,128,220), fill="black", width=8)
d.line((80,130,175,130), fill="black", width=8)
save(img, "SYM011")

# SYM012 - Theo dõi bệnh nhân
img, d = new_icon()
d.rounded_rectangle((35,45,220,205), radius=15, outline="black", width=9)
d.line([(50,130),(80,130),(100,90),(125,165),(150,110),(175,130),(205,130)],
       fill="black", width=8)
save(img, "SYM012")

print("Da tao thanh cong 12 hinh bieu trung!")
