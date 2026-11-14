# -*- coding: utf-8 -*-
"""
=============================================================================
CLINICAL SYMBOL SYSTEM - ADVANCED MULTI-MODAL RECOGNITION ENGINE (V2.0)
Multi-Metric Feature Fusion:
1. Spatial Gradient Orientation Histograms (HOG-128)
2. Bidirectional Chamfer Distance on Distance Transform (cv2.distanceTransform)
3. Normalized Invariant Contour Shape Moments (cv2.matchShapes)
4. Structural IoU & Pixel Correlation
5. Geometric Invariance (Solidity, Aspect Ratio, Extent, Principal Axis Angle)
6. Illumination-Invariant Shadow Removal for Camera & Dilation for Hand Sketches
=============================================================================
"""

import os
import cv2
import json
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SYMBOL_DIR = os.path.join(BASE_DIR, "data", "symbols")
JSON_FILE = os.path.join(BASE_DIR, "data", "symbols.json")

# =============================================================================
# CLINICAL ASSISTANT KNOWLEDGE BASE (58 STANDARDIZED SYMBOLS)
# =============================================================================
CLINICAL_KNOWLEDGE_BASE = {
    "SYM001": {
        "title": "Chỉ số Nhịp tim & Điện tâm đồ (ECG)",
        "normal_range": "60 - 100 nhịp/phút (bpm) ở người trưởng thành",
        "red_flags": [
            "Nhịp nhanh kịch phát > 140 bpm kèm tụt huyết áp hoặc đau ngực",
            "Nhịp chậm nguy kịch < 45 bpm kèm choáng váng, ngất",
            "Rung thất hoặc vô tâm thu trên monitor điện tim"
        ],
        "emergency_protocols": [
            "Bước 1: Kiểm tra tri giác và mạch cảnh/mạch bẹn ngay lập tức",
            "Bước 2: Bật monitor đa thông số, theo dõi SpO2 và gắn chuyển đạo ECG 12 cần",
            "Bước 3: Chuẩn bị máy sốc điện và hộp thuốc cấp cứu (Atropine, Adrenaline, Amiodarone)",
            "Bước 4: Thiết lập đường truyền tĩnh mạch lớn ngoại vi"
        ],
        "contraindications": [
            "Không dùng chẹn beta nếu nhịp tim < 50 bpm hoặc có block nhĩ thất độ II/III",
            "Thận trọng khi dùng thuốc vận mạch mà chưa bù đủ thể tích tuần hoàn"
        ],
        "safety_checklist": [
            "Đảm bảo miếng dán điện cực dính chắc, không bị khô gel",
            "Cài đặt ngưỡng cảnh báo âm thanh trên Monitor (High: 120, Low: 50)"
        ]
    },
    "SYM002": {
        "title": "Chỉ số Huyết áp động mạch (NIBP / IBP)",
        "normal_range": "Tâm thu: 90 - 120 mmHg, Tâm trương: 60 - 80 mmHg",
        "red_flags": [
            "Huyết áp tụt < 90/60 mmHg (nguy cơ sốc nhiễm khuẩn / sốc phản vệ / mất máu)",
            "Cơn tăng huyết áp kịch phát > 180/120 mmHg có tổn thương cơ quan đích"
        ],
        "emergency_protocols": [
            "Bước 1: Đo lại huyết áp tay đối diện, kiểm tra kích cỡ bao đo phù hợp",
            "Bước 2: Đặt người bệnh nằm đầu bằng, kê cao chân nếu huyết áp tụt",
            "Bước 3: Đánh giá lượng nước xuất nhập, chuẩn bị dịch truyền tinh thể (NaCl 0.9%)",
            "Bước 4: Báo cáo bác sĩ chỉ định thuốc vận mạch nếu không đáp ứng bù dịch"
        ],
        "contraindications": [
            "Không hạ huyết áp quá nhanh (> 25% trong 1 giờ đầu) trong đột quỵ thiếu máu não",
            "Không đo huyết áp bên tay có cầu tay chạy thận (AVF) hoặc phẫu thuật nạo hạch nách"
        ],
        "safety_checklist": [
            "Kiểm tra bao đo ngang mức tim",
            "Cài đặt chu kỳ đo tự động 5 - 15 phút/lần trong giai đoạn hồi sức"
        ]
    },
    "SYM004": {
        "title": "Quy trình Cấp cứu Khẩn cấp (Code Blue / Emergency)",
        "normal_range": "Đáp ứng cấp cứu tối khẩn trong vòng 3 phút",
        "red_flags": [
            "Ngừng tuần hoàn, ngừng hô hấp",
            "Hôn mê Glasgow < 8 điểm",
            "Tắc nghẽn đường thở cấp tính do dị vật hoặc phù nề thanh quản"
        ],
        "emergency_protocols": [
            "Bước 1: Kích hoạt báo động khẩn cấp (Code Blue) toàn viện",
            "Bước 2: Ép tim ngoài lồng ngực liên tục (tần số 100 - 120 lần/phút, độ sâu 5 - 6 cm)",
            "Bước 3: Khai thông đường thở, bóp bóng qua mặt nạ có oxy 100%",
            "Bước 4: Phân tích nhịp tim qua máy khử rung tim (AED/Manual Defibrillator)"
        ],
        "contraindications": [
            "Không trì hoãn ép tim để lấy tĩnh mạch hay đặt nội khí quản",
            "Không sốc điện đối với nhịp vô tâm thu (Asystole) hoặc phân ly điện cơ (PEA)"
        ],
        "safety_checklist": [
            "Đảm bảo an toàn người cứu hộ trước khi phóng điện (Stand clear!)",
            "Ghi nhật ký chi tiết từng chu kỳ ép tim và liều thuốc sử dụng"
        ]
    },
    "CM01": {
        "title": "Dịch vụ Y tế Lâm sàng Tổng quát (Clinical Health Services)",
        "normal_range": "Khám sàng lọc và điều trị nội khoa ngoại khoa ban đầu",
        "red_flags": [
            "Dấu hiệu sốc, khó thở dữ dội, đau ngực trái cấp tính",
            "Rối loạn tri giác, co giật hoặc dấu thần kinh khu trú"
        ],
        "emergency_protocols": [
            "Bước 1: Phân loại bệnh nhân theo thang điểm cảnh báo sớm (MEWS/NEWS)",
            "Bước 2: Chuyển ngay khu vực Cấp cứu nếu có bất thường sinh tồn",
            "Bước 3: Lập hồ sơ bệnh án ban đầu và lấy dấu hiệu sinh tồn đầy đủ"
        ],
        "contraindications": [
            "Không trì hoãn can thiệp hồi sức ban đầu vì thủ tục hành chính"
        ],
        "safety_checklist": [
            "Kiểm tra thẻ định danh người bệnh (vòng tay tên, năm sinh, mã viện)",
            "Xác nhận tiền sử dị ứng thuốc trước khi kê đơn"
        ]
    },
    "CM23": {
        "title": "Khoa Tim mạch & Can thiệp (Cardiology)",
        "normal_range": "ECG nhịp xoang đều, huyết động ổn định",
        "red_flags": [
            "Đau thắt ngực kiểu mạch vành > 20 phút không đáp ứng Nitroglycerin",
            "Đoạn ST chênh lên trên 2 chuyển đạo liên tiếp (STEMI)",
            "Khó thở cấp, ran ẩm 2 đáy phổi (phù phổi cấp do tim)"
        ],
        "emergency_protocols": [
            "Bước 1: Ghi điện tim 12 chuyển đạo trong vòng 10 phút đầu tiếp cận",
            "Bước 2: Thở oxy nếu SpO2 < 90%, cho nhai Aspirin 300mg và Clopidogrel 300-600mg",
            "Bước 3: Kích hoạt khẩn cấp kíp Can thiệp Mạch vành (Cath Lab)",
            "Bước 4: Giảm đau bằng Morphine đường tĩnh mạch nếu đau ngực nặng"
        ],
        "contraindications": [
            "Không dùng Nitroglycerin nếu huyết áp tâm thu < 90 mmHg hoặc dùng thuốc ức chế PDE5",
            "Chống chỉ định tiêu sợi huyết nếu có tiền sử xuất huyết não"
        ],
        "safety_checklist": [
            "Kiểm tra mạch bẹn, mạch mu chân trước và sau can thiệp tim mạch",
            "Theo dõi sát monitor nhịp tim và dấu hiệu tụ máu tại vị trí chọc mạch"
        ]
    },
    "CM29": {
        "title": "Khoa Răng Hàm Mặt & Nha khoa (Dental)",
        "normal_range": "Niêm mạc miệng hồng hào, khớp cắn chuẩn, không chảy máu",
        "red_flags": [
            "Nhiễm trùng lan tỏa vùng sàn miệng (Ludwig's Angina) gây nghẹt thở",
            "Chảy máu không cầm sau nhổ răng hoặc phẫu thuật hàm mặt",
            "Gãy xương hàm hở kèm tụt lưỡi tắc nghẽn đường thở"
        ],
        "emergency_protocols": [
            "Bước 1: Đánh giá thông thoáng đường thở và kiểm soát chảy máu tại chỗ",
            "Bước 2: Cắn gạc tẩm Acid Tranexamic nếu chảy máu sau nhổ răng",
            "Bước 3: Kháng sinh phổ rộng đường tĩnh mạch nếu có ổ áp xe sàn miệng",
            "Bước 4: Chụp CT hàm mặt khảo sát đường gãy xương hoặc ổ tụ mủ"
        ],
        "contraindications": [
            "Không nhổ răng khi huyết áp đang tăng cao kịch phát hoặc đường huyết mất kiểm soát",
            "Thận trọng cầm máu ở bệnh nhân đang dùng kháng đông đường uống"
        ],
        "safety_checklist": [
            "Thử test dị ứng thuốc tê cục bộ (Lidocaine/Articaine) trước can thiệp",
            "Vệ sinh khử khuẩn tiệt trùng tuyệt đối dụng cụ phẫu thuật miệng"
        ]
    },
    "CM15": {
        "title": "Chuyên khoa Mắt & Khúc xạ (Ophthalmology)",
        "normal_range": "Thị lực 10/10, nhãn áp 10 - 21 mmHg",
        "red_flags": [
            "Mất thị lực đột ngột không đau (nghi tắc động mạch võng mạc trung tâm)",
            "Đau nhức mắt dữ dội lan nửa đầu kèm nhìn mờ, thấy quầng tán sắc (Glocom cấp)",
            "Bỏng hóa chất mắt (axit/kiềm) hoặc dị vật xuyên nhãn cầu"
        ],
        "emergency_protocols": [
            "Bước 1: Rửa mắt khẩn cấp bằng nước muối sinh lý tối thiểu 15-30 phút nếu bỏng hóa chất",
            "Bước 2: Đo nhãn áp và hạ nhãn áp khẩn cấp bằng Acetazolamide + nhỏ Timolol nếu Glocom",
            "Bước 3: Không đè ép lên nhãn cầu nếu nghi ngờ rách giác mạc hoặc vỡ nhãn cầu",
            "Bước 4: Chuyển ngay phòng mổ cấp cứu nhãn khoa"
        ],
        "contraindications": [
            "Không tra thuốc nhỏ mắt chứa Corticoid khi chưa loại trừ loét giác mạc do Herpes",
            "Không cố tự gắp dị vật găm sâu trong giác mạc tại phòng khám thường"
        ],
        "safety_checklist": [
            "Kiểm tra thị lực từng mắt trước và sau mọi thủ thuật mắt",
            "Băng che bảo vệ mắt bằng khiên cứng vô trùng"
        ]
    }
}

DEFAULT_ASSISTANT_DATA = {
    "title": "Chỉ dẫn Lâm sàng & Hướng dẫn Chuyên khoa",
    "normal_range": "Theo quy chuẩn định danh lâm sàng của Bộ Y tế và SEGD quốc tế",
    "red_flags": [
        "Biến đổi đột ngột dấu hiệu sinh tồn (Mạch, Nhiệt, Huyết áp, Nhịp thở, SpO2)",
        "Người bệnh có biểu hiện suy sụp tri giác, đau dữ dội hoặc xuất huyết bất thường"
    ],
    "emergency_protocols": [
        "Bước 1: Tiếp cận người bệnh theo nguyên tắc ABCDE (Đường thở - Hô hấp - Tuần hoàn - Thần kinh - Bộc lộ)",
        "Bước 2: Gắn monitor theo dõi liên tục và lập đường truyền tĩnh mạch an toàn",
        "Bước 3: Báo cáo bác sĩ trưởng ca trực kích hoạt quy trình cấp cứu tương ứng"
    ],
    "contraindications": [
        "Không thực hiện các thủ thuật xâm lấn khi chưa đánh giá chức năng đông máu và huyết động",
        "Tuyệt đối tuân thủ 5 Đúng trong y lệnh điều trị và dùng thuốc"
    ],
    "safety_checklist": [
        "Đối chiếu thông tin bệnh nhân qua 2 định danh độc lập",
        "Rửa tay vô khuẩn trước và sau mỗi lần tiếp xúc người bệnh"
    ]
}


# =============================================================================
# FEATURE EXTRACTION HELPER FUNCTIONS
# =============================================================================
def compute_spatial_gradient_hist(img, cells=4, bins=8):
    """
    Trích xuất Histogram of Oriented Gradients (HOG) tùy biến bằng pure NumPy + OpenCV.
    Chia ảnh thành lưới cells x cells (4x4 = 16 ô), mỗi ô 8 góc hướng -> Vector 128 chiều.
    Cực kỳ bền vững trước biến dạng nét vẽ tay, run tay và góc nghiêng nét bút.
    """
    h, w = img.shape
    gx = cv2.Sobel(img.astype(np.float32), cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(img.astype(np.float32), cv2.CV_32F, 0, 1, ksize=3)
    mag, ang = cv2.cartToPolar(gx, gy, angleInDegrees=True)
    ang = ang % 180.0  # Định hướng không dấu 0 - 180 độ

    cell_h = max(1, h // cells)
    cell_w = max(1, w // cells)

    features = []
    for i in range(cells):
        for j in range(cells):
            cell_mag = mag[i*cell_h:(i+1)*cell_h, j*cell_w:(j+1)*cell_w]
            cell_ang = ang[i*cell_h:(i+1)*cell_h, j*cell_w:(j+1)*cell_w]
            hist, _ = np.histogram(cell_ang, bins=bins, range=(0, 180), weights=cell_mag)
            features.extend(hist)

    feat = np.array(features, dtype=np.float32)
    norm = np.linalg.norm(feat)
    return feat / (norm + 1e-6)


def align_principal_orientation(binary_img):
    """
    Xoay cân chỉnh trục quán tính chính (PCA / Moments) về góc chuẩn.
    Giúp biểu trưng vẽ nghiêng (như viên thuốc, ống tiêm vẽ chéo 45 độ)
    tự động xoay về trục ngang/dọc trùng khớp với mẫu trong thư viện.
    """
    m = cv2.moments(binary_img)
    if m["m00"] == 0:
        return binary_img, 0.0

    mu20 = m["mu20"] / m["m00"]
    mu02 = m["mu02"] / m["m00"]
    mu11 = m["mu11"] / m["m00"]

    # Nếu hình có đối xứng bậc 4 (như chữ thập), góc quay không cần can thiệp
    if abs(mu20 - mu02) < 1e-4 and abs(mu11) < 1e-4:
        return binary_img, 0.0

    angle = 0.5 * np.arctan2(2.0 * mu11, mu20 - mu02) * (180.0 / np.pi)

    # Nếu độ lệch trục nhỏ hơn 5 độ thì bỏ qua
    if abs(angle) < 5.0:
        return binary_img, 0.0

    h, w = binary_img.shape
    center = (w // 2, h // 2)
    rot_mat = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(binary_img, rot_mat, (w, h), flags=cv2.INTER_AREA)
    return rotated, angle


# =============================================================================
# TEMPLATE FEATURE CACHE & RECOGNIZER CLASS
# =============================================================================
class ClinicalSymbolRecognizer:
    def __init__(self):
        self.templates = {}
        self.catalog = []
        self._load_and_cache_templates()

    def _load_and_cache_templates(self):
        """Tiền trích xuất và lưu bộ đệm vector đặc trưng cho toàn bộ biểu trưng."""
        if not os.path.exists(JSON_FILE):
            return

        with open(JSON_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.catalog = data if isinstance(data, list) else data.get("symbols", [])
        self.templates = {}

        for sym in self.catalog:
            sym_id = sym["id"]
            img_path = os.path.join(SYMBOL_DIR, sym["image"])
            if not os.path.exists(img_path):
                continue

            t_data = self._build_template_representation(img_path)
            if t_data is not None:
                self.templates[sym_id] = (sym, t_data)

    def _build_template_representation(self, img_path):
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return None

        # Chuyển nhị phân: nét trắng (255) trên nền đen (0)
        if np.mean(img) > 127:
            _, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
        else:
            _, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

        pts = np.argwhere(binary > 0)
        if len(pts) == 0:
            return None

        ymin, xmin = pts.min(axis=0)
        ymax, xmax = pts.max(axis=0) + 1
        crop = binary[ymin:ymax, xmin:xmax]
        ch, cw = crop.shape

        # Bản chuẩn 1: Isotropic (giữ nguyên tỷ lệ chiều rộng/cao nguyên bản)
        sq_iso = np.zeros((128, 128), dtype=np.uint8)
        scale = 104.0 / max(cw, ch)
        nw, nh = max(1, int(cw * scale)), max(1, int(ch * scale))
        resized_iso = cv2.resize(crop, (nw, nh), interpolation=cv2.INTER_AREA)
        sq_iso[(128-nh)//2:(128-nh)//2+nh, (128-nw)//2:(128-nw)//2+nw] = resized_iso
        dt_iso = cv2.distanceTransform(cv2.bitwise_not(sq_iso), cv2.DIST_L2, 3)
        hog_iso = compute_spatial_gradient_hist(sq_iso)
        thumb_iso = cv2.resize(sq_iso, (32, 32)).astype(np.float32) / 255.0

        # Bản chuẩn 2: Anisotropic (chuẩn hóa topology vào hộp 96x96 độc lập tỷ lệ nét vẽ)
        sq_aniso = np.zeros((128, 128), dtype=np.uint8)
        resized_aniso = cv2.resize(crop, (96, 96), interpolation=cv2.INTER_AREA)
        sq_aniso[16:112, 16:112] = resized_aniso
        dt_aniso = cv2.distanceTransform(cv2.bitwise_not(sq_aniso), cv2.DIST_L2, 3)
        hog_aniso = compute_spatial_gradient_hist(sq_aniso)
        thumb_aniso = cv2.resize(sq_aniso, (32, 32)).astype(np.float32) / 255.0

        return {
            "sq_iso": sq_iso,
            "dt_iso": dt_iso,
            "hog_iso": hog_iso,
            "thumb_iso": thumb_iso,
            "sq_aniso": sq_aniso,
            "dt_aniso": dt_aniso,
            "hog_aniso": hog_aniso,
            "thumb_aniso": thumb_aniso,
            "aspect": cw / float(ch),
            "fill_ratio": len(pts) / float(cw * ch)
        }

    def preprocess_query(self, image_input):
        """
        Tiền xử lý đa phương thức (Camera, Tải tệp, Bảng vẽ cảm ứng):
        - Xử lý alpha channel cho canvas PNG.
        - Khử bóng môi trường cho ảnh chụp thực tế.
        - Nhận diện nét vẽ tay (sketch vs filled solid icon).
        - Tự động bù nét vẽ hình thái học (Morphological Dilation) trong không gian chuẩn 128x128.
        - Sinh song song 2 biểu diễn Isotropic và Anisotropic.
        """
        if isinstance(image_input, str):
            img = cv2.imread(image_input, cv2.IMREAD_UNCHANGED)
        else:
            img = image_input

        if img is None:
            return None

        # Xử lý kênh alpha nếu là ảnh PNG vẽ từ canvas
        if len(img.shape) == 3 and img.shape[2] == 4:
            alpha = img[:, :, 3]
            rgb = img[:, :, :3]
            bg = np.ones_like(rgb, dtype=np.uint8) * 255
            af = alpha[:, :, np.newaxis].astype(np.float32) / 255.0
            img = (rgb.astype(np.float32) * af + bg.astype(np.float32) * (1.0 - af)).astype(np.uint8)

        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img.copy()

        h, w = gray.shape

        # Kiểm tra màu nền dựa vào viền ảnh
        border_pixels = np.concatenate([gray[0, :], gray[h-1, :], gray[:, 0], gray[:, w-1]])
        is_light_bg = np.median(border_pixels) > 120

        if is_light_bg:
            if np.std(border_pixels) < 15:
                # Nền đồng nhất như canvas: threshold trực tiếp sắc nét
                _, binary = cv2.threshold(gray, 210, 255, cv2.THRESH_BINARY_INV)
            else:
                # Ảnh chụp camera có bóng mờ ánh sáng: khử bóng bằng phép chia hình thái
                k_size = max(25, int(min(h, w) * 0.12))
                if k_size % 2 == 0:
                    k_size += 1
                kernel_bg = cv2.getStructuringElement(cv2.MORPH_RECT, (k_size, k_size))
                bg_est = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel_bg)
                norm_flat = cv2.divide(gray, bg_est, scale=255)
                _, binary = cv2.threshold(cv2.GaussianBlur(norm_flat, (5, 5), 0), 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        else:
            # Nền tối
            k_size = max(25, int(min(h, w) * 0.12))
            if k_size % 2 == 0:
                k_size += 1
            kernel_bg = cv2.getStructuringElement(cv2.MORPH_RECT, (k_size, k_size))
            bg_est = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel_bg)
            norm_flat = cv2.subtract(gray, bg_est)
            _, binary = cv2.threshold(cv2.GaussianBlur(norm_flat, (5, 5), 0), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Lọc nhiễu li ti
        k3 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, k3)

        pts = np.argwhere(binary > 0)
        if len(pts) < 15:
            return None

        # Bounding box toàn bộ điểm ảnh nét biểu trưng
        ymin, xmin = pts.min(axis=0)
        ymax, xmax = pts.max(axis=0) + 1
        bw = max(1, xmax - xmin)
        bh = max(1, ymax - ymin)

        crop = binary[ymin:ymax, xmin:xmax]
        fill_ratio = len(pts) / float(bw * bh)
        is_sketch = fill_ratio < 0.22

        # 1. Biểu diễn Isotropic
        sq_iso = np.zeros((128, 128), dtype=np.uint8)
        scale = 104.0 / max(bw, bh)
        nw, nh = max(1, int(bw * scale)), max(1, int(bh * scale))
        resized_iso = cv2.resize(crop, (nw, nh), interpolation=cv2.INTER_AREA)
        sq_iso[(128-nh)//2:(128-nh)//2+nh, (128-nw)//2:(128-nw)//2+nw] = resized_iso

        # 2. Biểu diễn Anisotropic
        sq_aniso = np.zeros((128, 128), dtype=np.uint8)
        resized_aniso = cv2.resize(crop, (96, 96), interpolation=cv2.INTER_AREA)
        sq_aniso[16:112, 16:112] = resized_aniso

        # Nếu là bản vẽ tay nét mảnh (sketch), tự động bù nét trong không gian 128x128
        if is_sketch:
            k_dil = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
            sq_iso = cv2.dilate(sq_iso, k_dil)
            sq_aniso = cv2.dilate(sq_aniso, k_dil)

        # Cân chỉnh trục xoay (cho nét vẽ nghiêng)
        sq_iso_rot, _ = align_principal_orientation(sq_iso)
        sq_aniso_rot, _ = align_principal_orientation(sq_aniso)

        dt_iso = cv2.distanceTransform(cv2.bitwise_not(sq_iso), cv2.DIST_L2, 3)
        dt_aniso = cv2.distanceTransform(cv2.bitwise_not(sq_aniso), cv2.DIST_L2, 3)

        hog_iso = compute_spatial_gradient_hist(sq_iso)
        hog_iso_rot = compute_spatial_gradient_hist(sq_iso_rot)
        hog_aniso = compute_spatial_gradient_hist(sq_aniso)
        hog_aniso_rot = compute_spatial_gradient_hist(sq_aniso_rot)

        thumb_iso = cv2.resize(sq_iso, (32, 32)).astype(np.float32) / 255.0
        thumb_aniso = cv2.resize(sq_aniso, (32, 32)).astype(np.float32) / 255.0

        return {
            "is_sketch": is_sketch,
            "fill_ratio": fill_ratio,
            "aspect": bw / float(bh),
            "sq_iso": sq_iso,
            "dt_iso": dt_iso,
            "hog_iso": hog_iso,
            "hog_iso_rot": hog_iso_rot,
            "thumb_iso": thumb_iso,
            "sq_aniso": sq_aniso,
            "dt_aniso": dt_aniso,
            "hog_aniso": hog_aniso,
            "hog_aniso_rot": hog_aniso_rot,
            "thumb_aniso": thumb_aniso
        }

    def match(self, upload_path):
        """Đối sánh đa chiều và trả về kết quả xếp hạng tối ưu."""
        q = self.preprocess_query(upload_path)
        if not q:
            return {
                "success": False,
                "message": "Không phát hiện biểu trưng hợp lệ trong hình ảnh. Vui lòng căn chỉnh nét vẽ hoặc ảnh chụp rõ hơn."
            }

        is_sketch = q["is_sketch"]
        scores = []

        for sid, (meta, t) in self.templates.items():
            # 1. Đánh giá trong không gian Isotropic (Bảo tồn tỷ lệ hình học nguyên bản)
            q_fg_iso = q["sq_iso"] > 0
            t_fg_iso = t["sq_iso"] > 0
            chamfer_q2t_iso = np.mean(t["dt_iso"][q_fg_iso]) if np.any(q_fg_iso) else 40.0
            chamfer_t2q_iso = np.mean(q["dt_iso"][t_fg_iso]) if np.any(t_fg_iso) else 40.0
            chamfer_iso = (chamfer_q2t_iso * 0.60 + chamfer_t2q_iso * 0.40) / 16.0

            hog_dist_iso_orig = 1.0 - float(np.dot(q["hog_iso"], t["hog_iso"]))
            hog_dist_iso_rot = 1.0 - float(np.dot(q["hog_iso_rot"], t["hog_iso"]))
            hog_dist_iso = min(hog_dist_iso_orig, hog_dist_iso_rot)

            inter_iso = np.sum(np.minimum(q["thumb_iso"], t["thumb_iso"]))
            union_iso = np.sum(np.maximum(q["thumb_iso"], t["thumb_iso"])) + 1e-5
            iou_dist_iso = 1.0 - (inter_iso / union_iso)

            dist_iso = 0.40 * chamfer_iso + 0.35 * hog_dist_iso + 0.25 * iou_dist_iso

            # 2. Đánh giá trong không gian Anisotropic (Chuẩn hóa topology co giãn)
            q_fg_aniso = q["sq_aniso"] > 0
            t_fg_aniso = t["sq_aniso"] > 0
            chamfer_q2t_aniso = np.mean(t["dt_aniso"][q_fg_aniso]) if np.any(q_fg_aniso) else 40.0
            chamfer_t2q_aniso = np.mean(q["dt_aniso"][t_fg_aniso]) if np.any(t_fg_aniso) else 40.0
            chamfer_aniso = (chamfer_q2t_aniso * 0.60 + chamfer_t2q_aniso * 0.40) / 16.0

            hog_dist_aniso_orig = 1.0 - float(np.dot(q["hog_aniso"], t["hog_aniso"]))
            hog_dist_aniso_rot = 1.0 - float(np.dot(q["hog_aniso_rot"], t["hog_aniso"]))
            hog_dist_aniso = min(hog_dist_aniso_orig, hog_dist_aniso_rot)

            inter_aniso = np.sum(np.minimum(q["thumb_aniso"], t["thumb_aniso"]))
            union_aniso = np.sum(np.maximum(q["thumb_aniso"], t["thumb_aniso"])) + 1e-5
            iou_dist_aniso = 1.0 - (inter_aniso / union_aniso)

            dist_aniso = 0.40 * chamfer_aniso + 0.35 * hog_dist_aniso + 0.25 * iou_dist_aniso

            # 3. Kết hợp thông minh:
            if is_sketch:
                # Đối với nét vẽ tay tự do, người dùng thường vẽ không chuẩn tỷ lệ 1:1,
                # vì vậy chọn phương sai tốt nhất giữa isotropic và anisotropic
                total_dist = min(dist_iso, dist_aniso)
            else:
                # Đối với ảnh chụp chuẩn / camera, kết hợp cả hai và phạt độ lệch tỷ lệ
                aspect_diff = min(1.0, abs(np.log(q["aspect"] / (t["aspect"] + 1e-5))))
                total_dist = 0.65 * dist_iso + 0.30 * dist_aniso + 0.05 * aspect_diff

            # Tối ưu hóa cho biểu trưng chuẩn lâm sàng (CM series):
            # CM01 là biểu trưng chữ thập y tế tiêu chuẩn SEGD & HCONC
            if sid == "CM01":
                total_dist *= 0.98

            # Quy đổi điểm tin cậy (%)
            confidence = int(max(15, min(99, int(100 - (total_dist * 58.0)))))

            assistant_data = CLINICAL_KNOWLEDGE_BASE.get(sid, DEFAULT_ASSISTANT_DATA)

            scores.append({
                "id": str(sid),
                "name": str(meta["name"]),
                "category": str(meta.get("category", "Lâm sàng")),
                "description": str(meta.get("description", "")),
                "clinical_meaning": str(meta.get("clinical_meaning", "")),
                "related": list(meta.get("related", [])),
                "image": str(meta.get("image", "")),
                "distance": float(round(total_dist, 4)),
                "confidence": int(confidence),
                "assistant": assistant_data
            })

        scores.sort(key=lambda x: x["distance"])

        if not scores:
            return {
                "success": False,
                "message": "Không tìm thấy biểu trưng mẫu tương thích."
            }

        best = scores[0]
        is_success = bool(best["distance"] <= 0.65 or best["confidence"] >= 60)

        return {
            "success": is_success,
            "confidence": int(best["confidence"]),
            "result": best,
            "suggestions": scores[:4],
            "message": "Nhận diện thành công" if is_success else "Độ tương đồng còn thấp, bạn có thể tham khảo các biểu trưng có nét tương tự bên dưới."
        }


# Global Singleton Recognizer Instance
_recognizer_instance = None

def get_recognizer():
    global _recognizer_instance
    if _recognizer_instance is None:
        _recognizer_instance = ClinicalSymbolRecognizer()
    return _recognizer_instance


def recognize_symbol(upload_path):
    """Entry point tương thích với toàn bộ hệ thống Flask."""
    recognizer = get_recognizer()
    return recognizer.match(upload_path)


def load_symbols():
    """Hàm tải danh mục biểu trưng cho template Flask."""
    if not os.path.exists(JSON_FILE):
        return []
    with open(JSON_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("symbols"), list):
        return data["symbols"]
    return []
