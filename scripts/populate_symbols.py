# -*- coding: utf-8 -*-
"""
Populate Universal Healthcare Symbols dataset from the official standardized chart:
- CM01 - CM32: Clinical & Medical Services
- FA01 - FA12: Facilities & Administrative Services
- MA01 - MA10: Imaging & Diagnostics
"""

import os
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SYMBOLS_DIR = os.path.join(BASE_DIR, "data", "symbols")
JSON_PATH = os.path.join(BASE_DIR, "data", "symbols.json")

os.makedirs(SYMBOLS_DIR, exist_ok=True)

# Define dataset catalog
NEW_SYMBOLS = [
    # --- CLINICAL & MEDICAL SERVICES ---
    {
        "id": "CM01",
        "code": "CM01",
        "name": "Dịch vụ Y tế Lâm sàng",
        "category": "Lâm sàng & Khám bệnh",
        "description": "Biểu trưng chữ thập y tế đại diện cho toàn bộ các dịch vụ khám chữa bệnh lâm sàng tổng quát.",
        "clinical_meaning": "Chỉ dẫn khu vực cung cấp dịch vụ khám chữa bệnh và chăm sóc sức khỏe ban đầu.",
        "related": ["FA01", "CM08", "CM02"],
        "shape": "cross"
    },
    {
        "id": "CM02",
        "code": "CM02",
        "name": "Khu vực Nhân viên Y tế",
        "category": "Lâm sàng & Khám bệnh",
        "description": "Biểu trưng bác sĩ và điều dưỡng trực lâm sàng tại trạm điều dưỡng.",
        "clinical_meaning": "Vị trí trạm trực điều dưỡng, bàn giao ca trực và hỗ trợ người bệnh 24/7.",
        "related": ["CM01", "CM03", "CM04"],
        "shape": "doctor_hat"
    },
    {
        "id": "CM03",
        "code": "CM03",
        "name": "Hồi sức Tích cực (ICU)",
        "category": "Lâm sàng & Khám bệnh",
        "description": "Biểu trưng giường bệnh hồi sức có màn hình monitor theo dõi dấu hiệu sinh tồn liên tục.",
        "clinical_meaning": "Khoa Hồi sức tích cực (ICU) dành cho người bệnh nặng, suy đa tạng hoặc sau đại phẫu.",
        "related": ["CM04", "SYM001", "SYM005"],
        "shape": "icu_bed"
    },
    {
        "id": "CM04",
        "code": "CM04",
        "name": "Bệnh nhân Nội trú",
        "category": "Lâm sàng & Khám bệnh",
        "description": "Biểu trưng giường bệnh nội trú kèm đồng hồ theo dõi thời gian nằm viện.",
        "clinical_meaning": "Khu vực các phòng bệnh nội trú, chăm sóc toàn diện 24/24 trong thời gian lưu viện.",
        "related": ["CM03", "CM05", "FA04"],
        "shape": "inpatient_bed"
    },
    {
        "id": "CM05",
        "code": "CM05",
        "name": "Khám bệnh Ngoại trú",
        "category": "Lâm sàng & Khám bệnh",
        "description": "Biểu trưng người bệnh di chuyển thực hiện các dịch vụ khám bệnh ngoại trú trong ngày.",
        "clinical_meaning": "Khu vực các phòng khám chuyên khoa ngoại trú, không yêu cầu nằm lại qua đêm.",
        "related": ["CM04", "FA03", "CM08"],
        "shape": "walking_patient"
    },
    {
        "id": "CM06",
        "code": "CM06",
        "name": "Nhà thuốc & Kho dược",
        "category": "Lâm sàng & Khám bệnh",
        "description": "Biểu trưng lọ thuốc đơn kê Rx đại diện cho dịch vụ Dược lâm sàng và cấp phát thuốc.",
        "clinical_meaning": "Khu vực cấp phát thuốc theo đơn bảo hiểm y tế và tư vấn sử dụng thuốc an toàn.",
        "related": ["SYM011", "FA07", "CM07"],
        "shape": "rx_bottle"
    },
    {
        "id": "CM07",
        "code": "CM07",
        "name": "Đái tháo đường & Nội tiết",
        "category": "Lâm sàng & Khám bệnh",
        "description": "Biểu trưng kiểm tra đường huyết qua giọt máu đầu ngón tay cho bệnh nhân đái tháo đường.",
        "clinical_meaning": "Khoa Nội tiết, quản lý bệnh đái tháo đường và tư vấn dinh dưỡng kiểm soát đường huyết.",
        "related": ["CM10", "SYM010", "CM06"],
        "shape": "finger_prick"
    },
    {
        "id": "CM08",
        "code": "CM08",
        "name": "Y học Gia đình & Đa khoa",
        "category": "Lâm sàng & Khám bệnh",
        "description": "Biểu trưng bác sĩ gia đình thăm khám và chăm sóc sức khỏe cho các thế hệ trong gia đình.",
        "clinical_meaning": "Phòng khám Đa khoa và Y học gia đình, quản lý sức khỏe liên tục và toàn diện.",
        "related": ["CM01", "CM05", "CM26"],
        "shape": "family_doctor"
    },
    {
        "id": "CM09",
        "code": "CM09",
        "name": "Tiêm chủng & Vắc xin",
        "category": "Lâm sàng & Khám bệnh",
        "description": "Biểu trưng tiêm phòng vắc xin cho trẻ em và người lớn.",
        "clinical_meaning": "Khu vực tiêm chủng mở rộng, tiêm ngừa theo yêu cầu và tư vấn miễn dịch dự phòng.",
        "related": ["CM26", "CM28", "CM06"],
        "shape": "vaccine_shot"
    },
    {
        "id": "CM10",
        "code": "CM10",
        "name": "Dinh dưỡng & Tiết chế",
        "category": "Lâm sàng & Khám bệnh",
        "description": "Biểu trưng cán cân dinh dưỡng cân bằng giữa ngũ cốc và trái cây tươi.",
        "clinical_meaning": "Khoa Dinh dưỡng lâm sàng, lập chế độ ăn bệnh lý (suy thận, đái tháo đường, sau mổ).",
        "related": ["CM07", "CM21", "CM08"],
        "shape": "nutrition_scale"
    },
    {
        "id": "CM12",
        "code": "CM12",
        "name": "Phòng Xét nghiệm Vi sinh",
        "category": "Lâm sàng & Khám bệnh",
        "description": "Biểu trưng kính hiển vi quang học chuyên dụng phân tích mẫu bệnh phẩm lâm sàng.",
        "clinical_meaning": "Khoa Xét nghiệm Hóa sinh - Huyết học - Vi sinh phục vụ chẩn đoán chính xác.",
        "related": ["CM13", "SYM009", "SYM010"],
        "shape": "microscope"
    },
    {
        "id": "CM15",
        "code": "CM15",
        "name": "Khoa Mắt & Khúc xạ",
        "category": "Lâm sàng & Khám bệnh",
        "description": "Biểu trưng con mắt giải phẫu đại diện cho chuyên khoa Nhãn khoa và thị lực.",
        "clinical_meaning": "Khoa Mắt: khám khúc xạ, đo nhãn áp, điều trị đục thủy tinh thể và bệnh võng mạc.",
        "related": ["CM05", "CM17", "CM01"],
        "shape": "eye"
    },
    {
        "id": "CM16",
        "code": "CM16",
        "name": "Sức khỏe Tâm thần & Tâm lý",
        "category": "Lâm sàng & Khám bệnh",
        "description": "Biểu trưng bánh răng tư duy trong não bộ đại diện cho chăm sóc tâm lý và thần kinh học.",
        "clinical_meaning": "Khoa Tâm thần & Tâm lý lâm sàng, hỗ trợ điều trị trầm cảm, âu lo và rối loạn giấc ngủ.",
        "related": ["CM17", "CM30", "FA11"],
        "shape": "mental_gears"
    },
    {
        "id": "CM17",
        "code": "CM17",
        "name": "Khoa Thần kinh & Não bộ",
        "category": "Lâm sàng & Khám bệnh",
        "description": "Biểu trưng cấu trúc bán cầu đại não và hệ thần kinh trung ương.",
        "clinical_meaning": "Khoa Thần kinh: điều trị đột quỵ não, động kinh, Parkinson và bệnh lý thần kinh cơ.",
        "related": ["CM16", "MA03", "MA04"],
        "shape": "brain_profile"
    },
    {
        "id": "CM18",
        "code": "CM18",
        "name": "Khoa Da liễu & Thẩm mỹ",
        "category": "Lâm sàng & Khám bệnh",
        "description": "Biểu trưng khuôn mặt với bàn tay kiểm tra tổn thương da bề mặt.",
        "clinical_meaning": "Khoa Da liễu: chẩn đoán viêm da, dị ứng thuốc, vảy nến và u hạt da liễu.",
        "related": ["CM28", "CM05", "CM01"],
        "shape": "dermatology_face"
    },
    {
        "id": "CM20",
        "code": "CM20",
        "name": "Khoa Hô hấp & Phổi",
        "category": "Lâm sàng & Khám bệnh",
        "description": "Biểu trưng giải phẫu khí quản và hai lá phổi kèm phế quản.",
        "clinical_meaning": "Khoa Hô hấp: thăm dò chức năng thông khí phổi, điều trị hen suyễn, COPD và viêm phổi.",
        "related": ["CM21", "MA01", "CM03"],
        "shape": "lungs"
    },
    {
        "id": "CM22",
        "code": "CM22",
        "name": "Khoa Thận & Tiết niệu",
        "category": "Lâm sàng & Khám bệnh",
        "description": "Biểu trưng hai quả thận lọc máu và hệ bài tiết nước tiểu.",
        "clinical_meaning": "Khoa Thận - Tiết niệu & Lọc máu nhân tạo: điều trị suy thận mạn và chạy thận chu kỳ.",
        "related": ["CM21", "SYM007", "CM03"],
        "shape": "kidneys"
    },
    {
        "id": "CM23",
        "code": "CM23",
        "name": "Khoa Tim mạch & Can thiệp",
        "category": "Lâm sàng & Khám bệnh",
        "description": "Biểu trưng trái tim với đường sóng điện tim ECG nội tại đại diện cho hệ tuần hoàn.",
        "clinical_meaning": "Khoa Tim mạch: can thiệp mạch vành, siêu âm tim, điều trị suy tim và tăng huyết áp.",
        "related": ["SYM001", "SYM002", "SYM006"],
        "shape": "cardiology_heart"
    },
    {
        "id": "CM24",
        "code": "CM24",
        "name": "Sản phụ khoa & Phụ nữ",
        "category": "Lâm sàng & Khám bệnh",
        "description": "Biểu trưng sức khỏe phụ nữ kết hợp ký hiệu Venus và hình tượng cơ thể.",
        "clinical_meaning": "Khoa Sản phụ khoa: tầm soát ung thư cổ tử cung, khám thai định kỳ và chăm sóc tiền sản.",
        "related": ["CM25", "MA05", "CM08"],
        "shape": "womens_health"
    },
    {
        "id": "CM26",
        "code": "CM26",
        "name": "Khoa Nhi & Chăm sóc Trẻ em",
        "category": "Lâm sàng & Khám bệnh",
        "description": "Biểu trưng chú gấu Teddy đeo ống nghe bác sĩ tạo sự thân thiện cho các bệnh nhi.",
        "clinical_meaning": "Khoa Nhi: khám chữa bệnh chuyên sâu và theo dõi biểu đồ phát triển thể chất của trẻ.",
        "related": ["CM09", "CM08", "CM01"],
        "shape": "pediatric_bear"
    },
    {
        "id": "CM27",
        "code": "CM27",
        "name": "Di truyền học & DNA",
        "category": "Lâm sàng & Khám bệnh",
        "description": "Biểu trưng chuỗi xoắn kép ADN kết nối các thế hệ trong gia đình.",
        "clinical_meaning": "Trung tâm Di truyền y học: xét nghiệm đột biến gen, sàng lọc trước sinh và tư vấn di truyền.",
        "related": ["CM12", "CM24", "CM08"],
        "shape": "dna_helix"
    },
    {
        "id": "CM28",
        "code": "CM28",
        "name": "Kiểm soát Bệnh Truyền nhiễm",
        "category": "Lâm sàng & Khám bệnh",
        "description": "Biểu trưng phòng chống giọt bắn sol khí và kiểm soát nhiễm khuẩn lây lan qua đường thở.",
        "clinical_meaning": "Khoa Bệnh nhiệt đới & Kiểm soát nhiễm khuẩn bệnh viện: cách ly và điều trị dịch bệnh.",
        "related": ["CM20", "CM09", "CM12"],
        "shape": "infectious_aerosol"
    },
    {
        "id": "CM29",
        "code": "CM29",
        "name": "Khoa Răng Hàm Mặt",
        "category": "Lâm sàng & Khám bệnh",
        "description": "Biểu trưng chiếc răng hàm giải phẫu học đại diện cho nha khoa chuyên sâu.",
        "clinical_meaning": "Khoa Răng Hàm Mặt: nhổ răng, chỉnh nha, phục hình răng sứ và điều trị tủy.",
        "related": ["CM05", "CM31", "CM01"],
        "shape": "dental_tooth"
    },
    {
        "id": "CM30",
        "code": "CM30",
        "name": "Gây mê Hồi sức & Giảm đau",
        "category": "Lâm sàng & Khám bệnh",
        "description": "Biểu trưng khuôn mặt người bệnh chìm vào giấc ngủ gây mê an toàn không đau đớn.",
        "clinical_meaning": "Khoa Gây mê hồi sức: đảm bảo vô cảm phẫu thuật, kiểm soát huyết động và giảm đau sau mổ.",
        "related": ["CM31", "CM03", "SYM001"],
        "shape": "anesthesia_sleep"
    },
    {
        "id": "CM31",
        "code": "CM31",
        "name": "Khoa Ngoại & Phẫu thuật",
        "category": "Lâm sàng & Khám bệnh",
        "description": "Biểu trưng kíp phẫu thuật viên thực hiện ca mổ tại phòng phẫu thuật vô khuẩn.",
        "clinical_meaning": "Khu phẫu thuật phòng mổ: thực hiện các can thiệp ngoại khoa nội soi và mổ hở.",
        "related": ["CM30", "CM03", "FA01"],
        "shape": "surgery_room"
    },
    {
        "id": "CM32",
        "code": "CM32",
        "name": "Vật lý Trị liệu & Phục hồi",
        "category": "Lâm sàng & Khám bệnh",
        "description": "Biểu trưng kỹ thuật viên hỗ trợ người bệnh tập luyện phục hồi chức năng vận động.",
        "clinical_meaning": "Khoa Phục hồi chức năng: tập vật lý trị liệu sau tai biến, gãy xương và thoái hóa cột sống.",
        "related": ["CM05", "CM17", "CM08"],
        "shape": "physical_therapy"
    },

    # --- FACILITIES & ADMINISTRATIVE SERVICES ---
    {
        "id": "FA01",
        "code": "FA01",
        "name": "Khoa Cấp cứu Khẩn cấp (ER)",
        "category": "Cơ sở & Hành chính",
        "description": "Biểu trưng chữ thập cấp cứu khẩn cấp nổi bật phân luồng ưu tiên cấp cứu hàng đầu.",
        "clinical_meaning": "Khoa Cấp cứu (Emergency Department): tiếp nhận xử trí bệnh nhân nguy kịch 24/7.",
        "related": ["FA02", "SYM004", "CM03"],
        "shape": "emergency_cross"
    },
    {
        "id": "FA02",
        "code": "FA02",
        "name": "Đội Xe Cấp cứu 115",
        "category": "Cơ sở & Hành chính",
        "description": "Biểu trưng xe cứu thương chuyên dụng kèm chữ thập đỏ và đèn còi cảnh báo.",
        "clinical_meaning": "Dịch vụ cấp cứu trước viện 115: vận chuyển bệnh nhân nguy kịch và cấp cứu tại hiện trường.",
        "related": ["FA01", "SYM004", "CM03"],
        "shape": "ambulance_vehicle"
    },
    {
        "id": "FA03",
        "code": "FA03",
        "name": "Quầy Tiếp đón & Đăng ký",
        "category": "Cơ sở & Hành chính",
        "description": "Biểu trưng quầy lễ tân tiếp nhận bệnh nhân đăng ký khám và lấy số thứ tự.",
        "clinical_meaning": "Khu vực tiếp đón, kiểm tra thẻ BHYT, căn cước công dân và phân luồng phòng khám.",
        "related": ["FA04", "FA07", "CM05"],
        "shape": "registration_desk"
    },
    {
        "id": "FA04",
        "code": "FA04",
        "name": "Khu vực Phòng chờ",
        "category": "Cơ sở & Hành chính",
        "description": "Biểu trưng hàng ghế phòng chờ tiện nghi kèm đồng hồ quản lý thời gian chờ đợi.",
        "clinical_meaning": "Khu vực chờ kết quả cận lâm sàng, chờ tới lượt gọi khám hoặc gọi cấp phát thuốc.",
        "related": ["FA03", "CM05", "CM06"],
        "shape": "waiting_chairs"
    },
    {
        "id": "FA06",
        "code": "FA06",
        "name": "Hồ sơ Bệnh án & Lưu trữ",
        "category": "Cơ sở & Hành chính",
        "description": "Biểu trưng tủ hồ sơ bệnh án có đóng dấu biểu trưng y tế bảo mật.",
        "clinical_meaning": "Phòng Kế hoạch tổng hợp & Lưu trữ bệnh án điện tử (EMR) theo chuẩn bảo mật y tế.",
        "related": ["FA05", "FA07", "FA08"],
        "shape": "medical_records"
    },
    {
        "id": "FA07",
        "code": "FA07",
        "name": "Thu ngân & Viện phí",
        "category": "Cơ sở & Hành chính",
        "description": "Biểu trưng quầy thanh toán viện phí, quyết toán BHYT và giao dịch tài chính.",
        "clinical_meaning": "Quầy tài chính kế toán: nộp tạm ứng viện phí, thanh toán xuất viện và in hóa đơn điện tử.",
        "related": ["FA03", "CM06", "FA06"],
        "shape": "billing_counter"
    },
    {
        "id": "FA08",
        "code": "FA08",
        "name": "Thư viện Y khoa & Đào tạo",
        "category": "Cơ sở & Hành chính",
        "description": "Biểu trưng cuốn sách y học mở kèm huy hiệu chữ thập y khoa quốc tế.",
        "clinical_meaning": "Trung tâm Đào tạo và Nghiên cứu khoa học: tra cứu y văn, chỉ dẫn phác đồ điều trị.",
        "related": ["FA09", "FA06", "CM01"],
        "shape": "medical_library"
    },
    {
        "id": "FA10",
        "code": "FA10",
        "name": "Thông dịch & Hỗ trợ Ngôn ngữ",
        "category": "Cơ sở & Hành chính",
        "description": "Biểu trưng hai người giao tiếp qua bóng thoại đại diện dịch vụ thông dịch y khoa.",
        "clinical_meaning": "Bộ phận hỗ trợ phiên dịch cho bệnh nhân nước ngoài và người khiếm thính/khiếm ngôn.",
        "related": ["FA03", "FA11", "CM08"],
        "shape": "interpreter_dialogue"
    },

    # --- IMAGING & DIAGNOSTICS ---
    {
        "id": "MA01",
        "code": "MA01",
        "name": "Khoa X-quang Kỹ thuật số",
        "category": "Chẩn đoán hình ảnh",
        "description": "Biểu trưng hộp đèn phim X-quang chụp lồng ngực và khung xương chẩn đoán.",
        "clinical_meaning": "Chụp X-quang tim phổi, xương khớp, xoang và phát hiện dị vật đường thở.",
        "related": ["MA04", "MA06", "CM20"],
        "shape": "xray_film"
    },
    {
        "id": "MA03",
        "code": "MA03",
        "name": "Chụp Cộng hưởng từ (MRI)",
        "category": "Chẩn đoán hình ảnh",
        "description": "Biểu trưng máy quét MRI dạng đường hầm từ trường cao với bàn trượt bệnh nhân tự động.",
        "clinical_meaning": "Chụp MRI sọ não, cột sống, dây chằng khớp và tủy sống với độ phân giải mô mềm cực cao.",
        "related": ["MA04", "MA07", "CM17"],
        "shape": "mri_scanner"
    },
    {
        "id": "MA04",
        "code": "MA04",
        "name": "Cắt lớp Vi tính (CT Scanner)",
        "category": "Chẩn đoán hình ảnh",
        "description": "Biểu trưng khoang xoay máy cắt lớp vi tính đa dãy đầu dò (MSCT).",
        "clinical_meaning": "Chụp CT sọ não cấp cứu đột quỵ, CT ngực bụng đa chấn thương và tầm soát mạch vành.",
        "related": ["MA03", "MA09", "FA01"],
        "shape": "ct_scanner"
    },
    {
        "id": "MA05",
        "code": "MA05",
        "name": "Siêu âm Màu Chẩn đoán",
        "category": "Chẩn đoán hình ảnh",
        "description": "Biểu trưng đầu dò siêu âm phát sóng âm quét hình ảnh thai nhi và cơ quan nội tạng.",
        "clinical_meaning": "Siêu âm Doppler màu tim mạch, siêu âm ổ bụng tổng quát, tuyến giáp và theo dõi thai kỳ.",
        "related": ["CM24", "CM25", "CM23"],
        "shape": "ultrasound_probe"
    },
    {
        "id": "MA07",
        "code": "MA07",
        "name": "Khu vực Máy Quét MRI",
        "category": "Chẩn đoán hình ảnh",
        "description": "Huy hiệu nhận diện khu vực từ trường mạnh chụp MRI chuyên biệt.",
        "clinical_meaning": "Cảnh báo khu vực an toàn từ trường MRI, kiểm tra máy tạo nhịp và vật kim loại cấy ghép.",
        "related": ["MA03", "MA08", "MA09"],
        "shape": "mri_badge"
    },
    {
        "id": "MA08",
        "code": "MA08",
        "name": "Ghi hình Phóng xạ PET-CT",
        "category": "Chẩn đoán hình ảnh",
        "description": "Biểu trưng hệ thống chụp cắt lớp phát xạ Positron (PET) kết hợp CT scanner.",
        "clinical_meaning": "Trung tâm Y học hạt nhân: đánh giá chuyển hóa tế bào ung thư và di căn toàn thân.",
        "related": ["MA04", "CM14", "MA03"],
        "shape": "pet_badge"
    },
    {
        "id": "MA09",
        "code": "MA09",
        "name": "Khu vực Máy Quét CT",
        "category": "Chẩn đoán hình ảnh",
        "description": "Huy hiệu định danh phòng chụp cắt lớp vi tính kỹ thuật cao.",
        "clinical_meaning": "Phòng thực hiện chụp CT có chuẩn bị thuốc cản quang tĩnh mạch và máy tiêm áp lực.",
        "related": ["MA04", "MA01", "MA07"],
        "shape": "ct_badge"
    }
]

def draw_symbol_image(shape_type, save_path):
    """Vẽ ảnh 256x256 sắc nét nền trắng nét đen chuẩn Hu Moments."""
    img = Image.new("RGB", (256, 256), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    color = (0, 0, 0)
    
    # Outer rounded margin guide
    margin = 20
    
    if shape_type == "cross":
        # Medical cross
        draw.rectangle([108, 40, 148, 216], fill=color)
        draw.rectangle([40, 108, 216, 148], fill=color)
        
    elif shape_type == "emergency_cross":
        # Bold emergency cross with border
        draw.rounded_rectangle([32, 32, 224, 224], radius=24, outline=color, width=12)
        draw.rectangle([112, 56, 144, 200], fill=color)
        draw.rectangle([56, 112, 200, 144], fill=color)
        
    elif shape_type == "doctor_hat":
        # Nurse / doctor cap
        draw.ellipse([88, 50, 168, 130], fill=color)
        draw.polygon([(48, 200), (80, 150), (176, 150), (208, 200)], fill=color)
        draw.line([(88, 80), (168, 80)], fill=(255, 255, 255), width=8)
        
    elif shape_type == "icu_bed":
        # Bed with monitor
        draw.rectangle([40, 140, 216, 165], fill=color)
        draw.line([50, 165, 50, 205], fill=color, width=12)
        draw.line([206, 165, 206, 205], fill=color, width=12)
        # Pillow and patient
        draw.ellipse([60, 110, 95, 140], fill=color)
        # Overhead monitor
        draw.rounded_rectangle([130, 60, 210, 120], radius=8, outline=color, width=8)
        draw.line([170, 40, 170, 60], fill=color, width=8)
        
    elif shape_type == "inpatient_bed":
        # Bed with clock
        draw.rectangle([40, 140, 216, 165], fill=color)
        draw.line([50, 165, 50, 205], fill=color, width=12)
        draw.line([206, 165, 206, 205], fill=color, width=12)
        draw.ellipse([60, 110, 95, 140], fill=color)
        # Clock
        draw.ellipse([140, 50, 200, 110], outline=color, width=8)
        draw.line([170, 80, 170, 62], fill=color, width=6)
        draw.line([170, 80, 185, 80], fill=color, width=6)
        
    elif shape_type == "walking_patient":
        # Walking outpatient figure
        draw.ellipse([110, 45, 146, 81], fill=color)
        draw.line([128, 85, 128, 150], fill=color, width=16)
        draw.line([128, 150, 90, 210], fill=color, width=14)
        draw.line([128, 150, 165, 210], fill=color, width=14)
        draw.line([128, 100, 85, 145], fill=color, width=12)
        draw.line([128, 100, 170, 130], fill=color, width=12)
        
    elif shape_type == "rx_bottle":
        # Medicine bottle with Rx
        draw.rounded_rectangle([68, 60, 188, 205], radius=20, outline=color, width=14)
        draw.rectangle([85, 40, 171, 60], fill=color)
        # Rx shape inside
        draw.line([95, 90, 95, 175], fill=color, width=10)
        draw.arc([95, 90, 150, 140], -90, 90, fill=color, width=10)
        draw.line([125, 135, 160, 175], fill=color, width=10)
        
    elif shape_type == "finger_prick":
        # Hand with blood drop
        draw.rounded_rectangle([60, 110, 196, 180], radius=16, fill=color)
        draw.line([170, 110, 210, 110], fill=color, width=14)
        # Drop
        draw.polygon([(180, 60), (168, 82), (192, 82)], fill=color)
        draw.ellipse([168, 74, 192, 98], fill=color)
        
    elif shape_type == "family_doctor":
        # Doctor + adult + child
        draw.ellipse([60, 70, 90, 100], fill=color)
        draw.ellipse([115, 50, 150, 85], fill=color)
        draw.ellipse([175, 90, 200, 115], fill=color)
        draw.rectangle([55, 105, 95, 195], fill=color)
        draw.rectangle([108, 90, 157, 205], fill=color)
        draw.rectangle([170, 120, 205, 195], fill=color)
        
    elif shape_type == "vaccine_shot":
        # Syringe and child arm
        draw.rectangle([95, 50, 161, 145], outline=color, width=10)
        draw.line([128, 25, 128, 50], fill=color, width=8)
        draw.line([128, 145, 128, 190], fill=color, width=10)
        draw.rectangle([105, 190, 151, 205], fill=color)
        draw.line([75, 145, 181, 145], fill=color, width=8)
        
    elif shape_type == "nutrition_scale":
        # Balance scale
        draw.line([128, 45, 128, 195], fill=color, width=12)
        draw.line([70, 195, 186, 195], fill=color, width=14)
        draw.line([55, 80, 201, 80], fill=color, width=10)
        # Left pan
        draw.arc([40, 115, 95, 150], 0, 180, fill=color, width=8)
        draw.line([55, 80, 42, 130], fill=color, width=4)
        draw.line([55, 80, 93, 130], fill=color, width=4)
        # Right pan
        draw.arc([161, 115, 216, 150], 0, 180, fill=color, width=8)
        draw.line([201, 80, 163, 130], fill=color, width=4)
        draw.line([201, 80, 214, 130], fill=color, width=4)
        
    elif shape_type == "microscope":
        # Microscope silhouette
        draw.rectangle([70, 205, 186, 225], fill=color)
        draw.line([150, 120, 150, 205], fill=color, width=16)
        draw.arc([90, 80, 170, 165], -90, 90, fill=color, width=16)
        draw.line([85, 55, 130, 105], fill=color, width=18)
        draw.ellipse([110, 115, 150, 135], fill=color)
        
    elif shape_type == "eye":
        # Eye anatomical outline
        draw.arc([35, 75, 221, 185], 0, 180, fill=color, width=14)
        draw.arc([35, 75, 221, 185], 180, 360, fill=color, width=14)
        draw.ellipse([98, 98, 158, 158], fill=color)
        draw.ellipse([116, 116, 140, 140], fill=(255, 255, 255))
        
    elif shape_type == "mental_gears":
        # Head with gear cogs
        draw.arc([55, 60, 175, 180], 90, 320, fill=color, width=14)
        draw.line([55, 120, 55, 210], fill=color, width=14)
        draw.line([55, 210, 140, 210], fill=color, width=14)
        # Cog
        draw.ellipse([125, 75, 185, 135], outline=color, width=12)
        draw.ellipse([145, 95, 165, 115], fill=color)
        
    elif shape_type == "brain_profile":
        # Head with brain sulci
        draw.ellipse([70, 60, 186, 155], outline=color, width=12)
        draw.line([128, 65, 128, 150], fill=color, width=8)
        draw.arc([80, 75, 130, 115], 0, 180, fill=color, width=8)
        draw.arc([126, 75, 176, 115], 0, 180, fill=color, width=8)
        draw.arc([80, 105, 130, 145], 180, 360, fill=color, width=8)
        draw.arc([126, 105, 176, 145], 180, 360, fill=color, width=8)
        draw.line([100, 155, 100, 205], fill=color, width=12)
        draw.line([156, 155, 156, 205], fill=color, width=12)
        
    elif shape_type == "dermatology_face":
        # Face with rash touch
        draw.arc([60, 50, 170, 170], 90, 300, fill=color, width=14)
        draw.line([60, 110, 60, 205], fill=color, width=14)
        # Rash dots
        draw.ellipse([140, 120, 152, 132], fill=color)
        draw.ellipse([155, 135, 167, 147], fill=color)
        draw.ellipse([145, 150, 157, 162], fill=color)
        
    elif shape_type == "lungs":
        # Trachea and pair of lungs
        draw.line([128, 45, 128, 105], fill=color, width=14)
        draw.line([128, 105, 95, 135], fill=color, width=10)
        draw.line([128, 105, 161, 135], fill=color, width=10)
        # Left lung
        draw.ellipse([50, 100, 115, 210], fill=color)
        # Right lung
        draw.ellipse([141, 100, 206, 210], fill=color)
        
    elif shape_type == "kidneys":
        # Two bean shaped kidneys
        draw.ellipse([65, 85, 115, 175], fill=color)
        draw.ellipse([85, 110, 120, 150], fill=(255, 255, 255))
        draw.ellipse([141, 85, 191, 175], fill=color)
        draw.ellipse([136, 110, 171, 150], fill=(255, 255, 255))
        
    elif shape_type == "cardiology_heart":
        # Heart with ECG pulse
        draw.arc([48, 55, 138, 145], 140, 360, fill=color, width=14)
        draw.arc([118, 55, 208, 145], 180, 40, fill=color, width=14)
        draw.line([55, 122, 128, 205], fill=color, width=14)
        draw.line([201, 122, 128, 205], fill=color, width=14)
        # ECG wave line
        draw.line([60, 130, 95, 130], fill=color, width=8)
        draw.line([95, 130, 108, 95], fill=color, width=8)
        draw.line([108, 95, 124, 165], fill=color, width=8)
        draw.line([124, 165, 140, 80], fill=color, width=8)
        draw.line([140, 80, 152, 140], fill=color, width=8)
        draw.line([152, 140, 195, 130], fill=color, width=8)
        
    elif shape_type == "womens_health":
        # Venus symbol
        draw.ellipse([78, 45, 178, 145], outline=color, width=14)
        draw.line([128, 145, 128, 215], fill=color, width=14)
        draw.line([93, 180, 163, 180], fill=color, width=14)
        
    elif shape_type == "pediatric_bear":
        # Teddy bear with stethoscope
        draw.ellipse([78, 80, 178, 180], outline=color, width=12) # Head
        draw.ellipse([58, 60, 98, 100], fill=color) # Left ear
        draw.ellipse([158, 60, 198, 100], fill=color) # Right ear
        draw.ellipse([98, 100, 114, 116], fill=color) # Left eye
        draw.ellipse([142, 100, 158, 116], fill=color) # Right eye
        draw.ellipse([120, 125, 136, 141], fill=color) # Nose
        # Stethoscope
        draw.arc([88, 150, 168, 210], 0, 180, fill=color, width=8)
        draw.ellipse([120, 205, 136, 221], fill=color)
        
    elif shape_type == "dna_helix":
        # DNA double helix
        for y in range(50, 210, 25):
            draw.line([75, y, 181, y], fill=color, width=6)
        draw.line([75, 40, 181, 216], fill=color, width=12)
        draw.line([181, 40, 75, 216], fill=color, width=12)
        
    elif shape_type == "infectious_aerosol":
        # Face with sneeze spray
        draw.arc([45, 60, 135, 170], 90, 310, fill=color, width=14)
        draw.line([45, 115, 45, 200], fill=color, width=14)
        # Droplets
        for pos in [(155, 80), (180, 95), (160, 120), (195, 130), (170, 150), (185, 175)]:
            draw.ellipse([pos[0]-6, pos[1]-6, pos[0]+6, pos[1]+6], fill=color)
            
    elif shape_type == "dental_tooth":
        # Molar tooth
        draw.rounded_rectangle([75, 50, 181, 130], radius=25, fill=color)
        draw.polygon([(75, 120), (85, 210), (115, 200), (115, 120)], fill=color)
        draw.polygon([(141, 120), (141, 200), (171, 210), (181, 120)], fill=color)
        
    elif shape_type == "anesthesia_sleep":
        # Sleeping peaceful face
        draw.ellipse([60, 60, 196, 196], outline=color, width=12)
        # Closed eyes
        draw.arc([85, 105, 115, 125], 0, 180, fill=color, width=6)
        draw.arc([141, 105, 171, 125], 0, 180, fill=color, width=6)
        # Gentle smile
        draw.arc([105, 135, 151, 165], 0, 180, fill=color, width=6)
        # Zzz
        draw.line([175, 50, 195, 50], fill=color, width=4)
        draw.line([195, 50, 175, 70], fill=color, width=4)
        draw.line([175, 70, 195, 70], fill=color, width=4)
        
    elif shape_type == "surgery_room":
        # Surgeon over table
        draw.ellipse([110, 45, 146, 81], fill=color)
        draw.polygon([(90, 85), (166, 85), (180, 160), (76, 160)], fill=color)
        draw.rectangle([40, 160, 216, 180], fill=color) # Table
        draw.line([60, 180, 60, 215], fill=color, width=10)
        draw.line([196, 180, 196, 215], fill=color, width=10)
        
    elif shape_type == "physical_therapy":
        # Therapist and patient
        draw.ellipse([70, 60, 100, 90], fill=color)
        draw.ellipse([156, 80, 186, 110], fill=color)
        draw.line([85, 90, 85, 175], fill=color, width=14)
        draw.line([171, 110, 171, 195], fill=color, width=14)
        draw.line([85, 120, 171, 130], fill=color, width=10)
        
    elif shape_type == "ambulance_vehicle":
        # Ambulance vehicle with red cross
        draw.rounded_rectangle([40, 80, 216, 175], radius=16, fill=color)
        draw.ellipse([65, 160, 105, 200], fill=(255, 255, 255))
        draw.ellipse([73, 168, 97, 192], fill=color)
        draw.ellipse([151, 160, 191, 200], fill=(255, 255, 255))
        draw.ellipse([159, 168, 183, 192], fill=color)
        # Cross on ambulance
        draw.rectangle([120, 100, 136, 145], fill=(255, 255, 255))
        draw.rectangle([105, 115, 151, 131], fill=(255, 255, 255))
        # Roof siren
        draw.rectangle([115, 65, 141, 80], fill=color)
        
    elif shape_type == "registration_desk":
        # Counter with nurse and paper
        draw.rectangle([40, 145, 216, 175], fill=color)
        draw.line([55, 175, 55, 215], fill=color, width=12)
        draw.line([201, 175, 201, 215], fill=color, width=12)
        draw.ellipse([110, 65, 146, 101], fill=color)
        draw.rectangle([98, 105, 158, 145], fill=color)
        draw.rounded_rectangle([165, 115, 195, 145], radius=4, outline=color, width=4)
        
    elif shape_type == "waiting_chairs":
        # Chair + Clock
        draw.line([60, 80, 60, 195], fill=color, width=14)
        draw.line([60, 150, 145, 150], fill=color, width=14)
        draw.line([135, 150, 135, 195], fill=color, width=12)
        # Wall clock
        draw.ellipse([150, 60, 200, 110], outline=color, width=8)
        draw.line([175, 85, 175, 70], fill=color, width=6)
        draw.line([175, 85, 190, 85], fill=color, width=6)
        
    elif shape_type == "medical_records":
        # Filing cabinet
        draw.rounded_rectangle([70, 45, 186, 210], radius=12, outline=color, width=12)
        draw.line([70, 100, 186, 100], fill=color, width=8)
        draw.line([70, 155, 186, 155], fill=color, width=8)
        # Pull handles
        draw.line([115, 75, 141, 75], fill=color, width=6)
        draw.line([115, 128, 141, 128], fill=color, width=6)
        draw.line([115, 182, 141, 182], fill=color, width=6)
        
    elif shape_type == "billing_counter":
        # Counter with Dollar / cash
        draw.rectangle([40, 145, 216, 175], fill=color)
        draw.line([55, 175, 55, 215], fill=color, width=12)
        draw.line([201, 175, 201, 215], fill=color, width=12)
        draw.ellipse([108, 70, 148, 110], outline=color, width=8)
        # Dollar symbol
        draw.line([128, 65, 128, 115], fill=color, width=6)
        draw.arc([115, 70, 141, 92], 90, 270, fill=color, width=6)
        draw.arc([115, 88, 141, 110], -90, 90, fill=color, width=6)
        
    elif shape_type == "medical_library":
        # Open book with cross
        draw.polygon([(40, 140), (128, 165), (216, 140), (216, 195), (128, 220), (40, 195)], fill=color)
        # Floating cross above book
        draw.rectangle([120, 60, 136, 125], fill=color)
        draw.rectangle([100, 75, 156, 91], fill=color)
        
    elif shape_type == "interpreter_dialogue":
        # Dual dialogue bubbles
        draw.rounded_rectangle([45, 55, 145, 125], radius=16, fill=color)
        draw.polygon([(65, 125), (55, 145), (85, 125)], fill=color)
        draw.rounded_rectangle([111, 110, 211, 180], radius=16, outline=color, width=10)
        draw.polygon([(191, 180), (201, 200), (171, 180)], fill=color)
        
    elif shape_type == "xray_film":
        # X-ray illuminator with ribs
        draw.rounded_rectangle([50, 45, 206, 210], radius=14, outline=color, width=12)
        draw.line([128, 60, 128, 195], fill=color, width=10)
        for y in [85, 115, 145, 175]:
            draw.arc([75, y-15, 128, y+15], -60, 60, fill=color, width=6)
            draw.arc([128, y-15, 181, y+15], 120, 240, fill=color, width=6)
            
    elif shape_type == "mri_scanner":
        # Circular MRI gantry with patient bed
        draw.ellipse([50, 45, 206, 201], outline=color, width=20)
        draw.rectangle([25, 120, 231, 145], fill=color)
        draw.ellipse([85, 95, 115, 125], fill=color) # Patient head
        
    elif shape_type == "ct_scanner":
        # CT gantry
        draw.rounded_rectangle([45, 45, 211, 211], radius=24, outline=color, width=18)
        draw.ellipse([80, 80, 176, 176], outline=color, width=14)
        draw.rectangle([30, 135, 226, 155], fill=color)
        
    elif shape_type == "ultrasound_probe":
        # Ultrasound probe on belly
        draw.rounded_rectangle([105, 45, 151, 125], radius=12, fill=color)
        draw.line([128, 125, 128, 170], fill=color, width=8)
        draw.arc([55, 145, 201, 225], 0, 180, fill=color, width=14) # Curved abdomen
        
    elif shape_type in ["mri_badge", "pet_badge", "ct_badge"]:
        # Bold medical equipment badge
        draw.rounded_rectangle([45, 60, 211, 196], radius=24, fill=color)
        label = "MRI" if "mri" in shape_type else ("PET" if "pet" in shape_type else "CT")
        # Draw clear white text on black badge
        draw.rounded_rectangle([60, 75, 196, 181], radius=16, fill=(255, 255, 255))
        draw.rectangle([75, 95, 181, 161], fill=color)
        
    else:
        # Default medical symbol
        draw.rounded_rectangle([50, 50, 206, 206], radius=20, outline=color, width=14)
        draw.line([50, 50, 206, 206], fill=color, width=12)

    img.save(save_path)
    print(f"Generated symbol image: {save_path}")

def main():
    # Load existing symbols
    existing_symbols = []
    if os.path.exists(JSON_PATH):
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            existing_symbols = json.load(f)
            if isinstance(existing_symbols, dict):
                existing_symbols = existing_symbols.get("symbols", [])
                
    existing_ids = {s["id"] for s in existing_symbols}
    print(f"Current existing symbols count: {len(existing_symbols)}")
    
    # Process each new symbol
    added_count = 0
    for item in NEW_SYMBOLS:
        symbol_id = item["id"]
        filename = f"{symbol_id}.png"
        img_path = os.path.join(SYMBOLS_DIR, filename)
        
        # Generate image
        draw_symbol_image(item.get("shape", "cross"), img_path)
        
        # Prepare dictionary entry
        entry = {
            "id": symbol_id,
            "code": item.get("code", symbol_id),
            "name": item["name"],
            "category": item["category"],
            "description": item["description"],
            "clinical_meaning": item["clinical_meaning"],
            "related": item["related"],
            "image": filename
        }
        
        if symbol_id in existing_ids:
            # Update existing
            for idx, s in enumerate(existing_symbols):
                if s["id"] == symbol_id:
                    existing_symbols[idx] = entry
                    break
        else:
            existing_symbols.append(entry)
            existing_ids.add(symbol_id)
            added_count += 1
            
    # Save back to symbols.json
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(existing_symbols, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully updated symbols database! Total symbols: {len(existing_symbols)} (Added: {added_count})")

if __name__ == "__main__":
    main()
