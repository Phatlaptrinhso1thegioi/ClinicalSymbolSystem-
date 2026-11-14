import os
import sys

# Thêm thư mục gốc vào sys.path để Flask import được recognition.py, chatbot.py và dữ liệu data/
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from app import app

# Vercel sẽ tự động phát hiện đối tượng WSGI `app`
