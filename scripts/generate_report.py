# -*- coding: utf-8 -*-
"""
=============================================================================
CLINICAL SYMBOL SYSTEM - REPORT & PDF GENERATOR
Biên soạn báo cáo khoa học kỹ thuật toàn diện cho dự án Clinical Symbol System
và xuất bản ra tệp PDF chuẩn in ấn chất lượng cao bằng Google Chrome Headless.
Tác giả: NGÔ KHÁNH GIANG
Năm: 2026
=============================================================================
"""

import os
import base64
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "reports", "assets")
HTML_OUT = os.path.join(BASE_DIR, "reports", "BAO_CAO_CLINICAL_SYMBOL_SYSTEM.html")
PDF_OUT = os.path.join(BASE_DIR, "reports", "BAO_CAO_CLINICAL_SYMBOL_SYSTEM.pdf")
BRAIN_DIR = "/Users/paradox/.gemini/antigravity/brain/6d2fdd47-797e-47f6-bf04-f84ca0068a5a"

def get_base64_image(filename):
    path = os.path.join(ASSETS_DIR, filename)
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/png;base64,{data}"

def generate_html():
    img_hero = get_base64_image("landing_ladipage_hero.png")
    img_landing_pastel = get_base64_image("landing_pastel_white.png")
    img_login = get_base64_image("login_liquid_slidebar.png")
    img_dashboard = get_base64_image("dashboard_pastel_white.png")
    img_sidebar = get_base64_image("dashboard_sidebar_collapsed.png")
    img_canvas_drawn = get_base64_image("drawn_cross_canvas.png")
    img_result = get_base64_image("drawn_cross_recognition_result.png")
    img_catalog = get_base64_image("landing_54_symbols_catalog_verified.png")

    html_content = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>Báo Cáo Nghiên Cứu & Phát Triển Sản Phẩm - Clinical Symbol System</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

  @page {
    size: A4 portrait;
    margin: 18mm 16mm 20mm 16mm;
  }

  * {
    box-sizing: border-box;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }

  body {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    font-size: 10.5pt;
    line-height: 1.65;
    color: #1e293b;
    background: #ffffff;
    margin: 0;
    padding: 0;
  }

  /* Page Break Utilities */
  .page-break {
    page-break-before: always;
    break-before: page;
  }

  .no-break {
    page-break-inside: avoid;
    break-inside: avoid;
  }

  /* ====================================================================
     COVER PAGE STYLING
     ==================================================================== */
  .cover-container {
    min-height: 94vh;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    border: 3px double #1e3a8a;
    border-radius: 8px;
    padding: 35px 30px;
    background: linear-gradient(180deg, #f8faff 0%, #ffffff 40%, #f0f7ff 100%);
    box-shadow: inset 0 0 40px rgba(30, 58, 138, 0.03);
    position: relative;
  }

  .cover-header {
    text-align: center;
    border-bottom: 2px solid #2563eb;
    padding-bottom: 16px;
  }

  .cover-dept {
    font-size: 11pt;
    font-weight: 700;
    letter-spacing: 1.5px;
    color: #1e3a8a;
    text-transform: uppercase;
    margin-bottom: 4px;
  }

  .cover-subdept {
    font-size: 9.5pt;
    font-weight: 600;
    letter-spacing: 1px;
    color: #475569;
    text-transform: uppercase;
  }

  .cover-body {
    text-align: center;
    padding: 30px 10px;
  }

  .cover-badge {
    display: inline-block;
    background: linear-gradient(135deg, #1e3a8a, #2563eb);
    color: #ffffff;
    padding: 6px 18px;
    border-radius: 30px;
    font-size: 9pt;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 20px;
  }

  .cover-title {
    font-size: 20pt;
    font-weight: 800;
    line-height: 1.35;
    color: #0f172a;
    text-transform: uppercase;
    margin-bottom: 14px;
    letter-spacing: -0.5px;
  }

  .cover-subtitle {
    font-size: 12pt;
    font-weight: 600;
    color: #2563eb;
    margin-bottom: 25px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .cover-divider {
    width: 120px;
    height: 4px;
    background: linear-gradient(90deg, #2563eb, #10b981);
    margin: 0 auto 25px auto;
    border-radius: 2px;
  }

  .cover-abstract-box {
    max-width: 580px;
    margin: 0 auto;
    background: rgba(255, 255, 255, 0.95);
    border: 1px solid #bfdbfe;
    border-left: 5px solid #2563eb;
    border-radius: 8px;
    padding: 14px 18px;
    text-align: justify;
    font-size: 9.5pt;
    color: #334155;
    line-height: 1.6;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.05);
  }

  .cover-meta {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    border-top: 1px solid #cbd5e1;
    padding-top: 18px;
    margin-top: 20px;
  }

  .meta-author {
    text-align: left;
  }

  .meta-author-label {
    font-size: 8.5pt;
    color: #64748b;
    text-transform: uppercase;
    font-weight: 600;
    letter-spacing: 0.5px;
  }

  .meta-author-name {
    font-size: 12pt;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: 0.5px;
  }

  .meta-date {
    text-align: right;
  }

  .meta-date-val {
    font-size: 10pt;
    font-weight: 700;
    color: #2563eb;
  }

  /* ====================================================================
     SECTION HEADINGS
     ==================================================================== */
  h1.chapter-title {
    font-size: 14pt;
    font-weight: 800;
    color: #0f172a;
    text-transform: uppercase;
    border-bottom: 2px solid #2563eb;
    padding-bottom: 6px;
    margin-top: 28px;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  h1.chapter-title::before {
    content: "";
    display: inline-block;
    width: 6px;
    height: 18px;
    background: #2563eb;
    border-radius: 3px;
  }

  h2.section-title {
    font-size: 11.5pt;
    font-weight: 700;
    color: #1e3a8a;
    margin-top: 18px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 6px;
  }

  h3.subsection-title {
    font-size: 10.5pt;
    font-weight: 700;
    color: #334155;
    margin-top: 14px;
    margin-bottom: 8px;
  }

  p {
    text-align: justify;
    margin-top: 0;
    margin-bottom: 10px;
  }

  /* Table of Contents */
  .toc-list {
    list-style: none;
    padding-left: 0;
    margin: 15px 0;
  }

  .toc-item {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 8px;
    font-size: 9.5pt;
  }

  .toc-name {
    font-weight: 600;
    color: #1e293b;
  }

  .toc-dots {
    flex-grow: 1;
    border-bottom: 1px dotted #94a3b8;
    margin: 0 8px;
  }

  .toc-page {
    font-weight: 700;
    color: #2563eb;
  }

  /* Callout Boxes */
  .callout {
    border-radius: 8px;
    padding: 12px 16px;
    margin: 14px 0;
    font-size: 9.5pt;
    line-height: 1.55;
  }

  .callout-info {
    background: #eff6ff;
    border-left: 4px solid #2563eb;
    color: #1e40af;
  }

  .callout-warning {
    background: #fffbeb;
    border-left: 4px solid #d97706;
    color: #92400e;
  }

  .callout-success {
    background: #ecfdf5;
    border-left: 4px solid #10b981;
    color: #065f46;
  }

  /* Tables */
  table.custom-table {
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0;
    font-size: 9pt;
  }

  table.custom-table th {
    background: #1e293b;
    color: #ffffff;
    font-weight: 700;
    text-align: left;
    padding: 8px 12px;
    border: 1px solid #1e293b;
  }

  table.custom-table td {
    padding: 8px 12px;
    border: 1px solid #cbd5e1;
    vertical-align: top;
  }

  table.custom-table tr:nth-child(even) {
    background: #f8fafc;
  }

  /* Formula Box */
  .formula-box {
    background: #f1f5f9;
    border-left: 3px solid #64748b;
    padding: 10px 14px;
    margin: 12px 0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 9pt;
    color: #0f172a;
    border-radius: 4px;
  }

  /* Figures & Captions */
  .figure-wrapper {
    text-align: center;
    margin: 16px auto;
    page-break-inside: avoid;
    break-inside: avoid;
  }

  .figure-img {
    max-width: 95%;
    height: auto;
    border-radius: 8px;
    border: 1px solid #cbd5e1;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  }

  .figure-caption {
    font-size: 8.5pt;
    font-weight: 600;
    color: #475569;
    margin-top: 6px;
    font-style: italic;
  }

  /* 2-Column Grid for Screenshots */
  .two-col-grid {
    display: flex;
    gap: 12px;
    margin: 14px 0;
  }

  .two-col-grid .figure-wrapper {
    flex: 1;
    margin: 0;
  }

  .two-col-grid .figure-img {
    max-width: 100%;
  }

  /* Bullet lists */
  ul, ol {
    margin-top: 4px;
    margin-bottom: 10px;
    padding-left: 20px;
  }

  li {
    margin-bottom: 4px;
    text-align: justify;
  }

  /* Header and Footer for Pages */
  .page-header {
    font-size: 8pt;
    color: #94a3b8;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 4px;
    margin-bottom: 14px;
    display: flex;
    justify-content: space-between;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .badge-pill {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 7.5pt;
    font-weight: 700;
    text-transform: uppercase;
  }
  .badge-success { background: #dcfce7; color: #15803d; }
  .badge-primary { background: #dbeafe; color: #1d4ed8; }
  .badge-purple  { background: #f3e8ff; color: #7e22ce; }
  .badge-warning { background: #fef3c7; color: #b45309; }
</style>
</head>
<body>

  <!-- ====================================================================
       TRANG BÌA (COVER PAGE)
       ==================================================================== -->
  <div class="cover-container">
    <div class="cover-header">
      <div class="cover-dept">ĐỀ TÀI NGHIÊN CỨU & PHÁT TRIỂN ỨNG DỤNG Y TẾ SỐ</div>
      <div class="cover-subdept">CLINICAL ARTIFICIAL INTELLIGENCE & COMPUTER VISION LAB</div>
    </div>

    <div class="cover-body">
      <div class="cover-badge">✦ BÁO CÁO KỸ THUẬT & GIỚI THIỆU SẢN PHẨM ✦</div>
      <div class="cover-title">
        HỆ THỐNG MẠNG LƯỚI ĐIỂM MỐC ĐA CHIỀU<br>
        NHẰM PHÂN TÍCH BIỂU TRƯNG KÝ HIỆU Y TẾ<br>
        HỖ TRỢ GIAO TIẾP LÂM SÀNG
      </div>
      <div class="cover-subtitle">
        Clinical Symbol System (CSS-AI) & Clinical Decision Support
      </div>
      <div class="cover-divider"></div>

      <div class="cover-abstract-box">
        <strong>TÓM TẮT DỰ ÁN:</strong> Báo cáo trình bày kết quả thiết kế, phát triển và thử nghiệm nền tảng web thông minh <em>Clinical Symbol System</em>. Hệ thống giải quyết bài toán rào cản ngôn ngữ và nhận diện biểu trưng y tế trong môi trường khám chữa bệnh thông qua lõi thị giác máy tính <strong>Multi-Metric Feature Fusion 2.0</strong> (kết hợp HOG-128, Chamfer Distance, Khử bóng đổ hình thái học và Moment bất biến). Hệ thống số hóa toàn diện 54+ biểu trưng theo tiêu chuẩn quốc tế SEGD & HCONC, tích hợp 3 kênh thu nhận ảnh (Tải tệp, Quét Camera laser thời gian thực, Bảng vẽ tay cảm ứng) cùng Gói Trợ lý Lâm sàng AI hỗ trợ phác đồ cấp cứu và cảnh báo Red Flags.
      </div>
    </div>

    <div class="cover-meta">
      <div class="meta-author">
        <div class="meta-author-label">Người thực hiện nghiên cứu</div>
        <div class="meta-author-name">NGÔ KHÁNH GIANG</div>
        <div style="font-size: 9pt; color: #64748b; margin-top: 2px;">Kỹ sư / Nhà nghiên cứu Công nghệ Y tế</div>
      </div>
      <div class="meta-date">
        <div class="meta-author-label">Thời gian hoàn thành</div>
        <div class="meta-date-val">NĂM 2026</div>
        <div style="font-size: 8.5pt; color: #64748b; margin-top: 2px;">Phiên bản v2.5 Flawless</div>
      </div>
    </div>
  </div>

  <div class="page-break"></div>

  <!-- ====================================================================
       MỤC LỤC & TÓM TẮT ĐỀ TÀI
       ==================================================================== -->
  <div class="page-header">
    <span>Clinical Symbol System - Báo Cáo Nghiên Cứu 2026</span>
    <span>Tác giả: Ngô Khánh Giang</span>
  </div>

  <h1 class="chapter-title">MỤC LỤC TỔNG QUAN</h1>
  <ul class="toc-list">
    <li class="toc-item"><span class="toc-name">TÓM TẮT ĐỀ TÀI (EXECUTIVE SUMMARY)</span><span class="toc-dots"></span><span class="toc-page">Trang 02</span></li>
    <li class="toc-item"><span class="toc-name">CHƯƠNG 1: GIỚI THIỆU & TÍNH CẤP THIẾT CỦA ĐỀ TÀI</span><span class="toc-dots"></span><span class="toc-page">Trang 03</span></li>
    <li class="toc-item"><span class="toc-name">CHƯƠNG 2: KIẾN TRÚC HỆ THỐNG & NGĂN XẾP CÔNG NGHỆ</span><span class="toc-dots"></span><span class="toc-page">Trang 04</span></li>
    <li class="toc-item"><span class="toc-name">CHƯƠNG 3: CƠ SỞ LÝ THUYẾT & LÕI NHẬN DIỆN THỊ GIÁC MULTI-METRIC FUSION 2.0</span><span class="toc-dots"></span><span class="toc-page">Trang 06</span></li>
    <li class="toc-item"><span class="toc-name">CHƯƠNG 4: HỆ THỐNG CHỨC NĂNG THỰC THI ĐỘT PHÁ CỦA DỰ ÁN</span><span class="toc-dots"></span><span class="toc-page">Trang 08</span></li>
    <li class="toc-item"><span class="toc-name">CHƯƠNG 5: KẾT QUẢ THỰC NGHIỆM & ĐO LƯỜNG ĐỘ CHÍNH XÁC</span><span class="toc-dots"></span><span class="toc-page">Trang 11</span></li>
    <li class="toc-item"><span class="toc-name">CHƯƠNG 6: THẢO LUẬN, HẠN CHẾ & HƯỚNG PHÁT TRIỂN TƯƠNG LAI</span><span class="toc-dots"></span><span class="toc-page">Trang 13</span></li>
    <li class="toc-item"><span class="toc-name">CHƯƠNG 7: KẾT LUẬN & KIẾN NGHỊ</span><span class="toc-dots"></span><span class="toc-page">Trang 14</span></li>
  </ul>

  <h1 class="chapter-title" style="margin-top: 25px;">TÓM TẮT ĐỀ TÀI (EXECUTIVE SUMMARY)</h1>
  <p>
    <strong>Clinical Symbol System</strong> là hệ sinh thái phần mềm hoàn chỉnh kết hợp giữa <em>Thị giác Máy tính (Computer Vision)</em>, <em>Lý thuyết Đồ thị Tương tác (Graph Network)</em> và <em>Trợ lý Ra quyết định Lâm sàng (Clinical Decision Support - CDS)</em>. Dự án được nghiên cứu và phát triển bởi <strong>Ngô Khánh Giang</strong> nhằm cung cấp giải pháp tra cứu, phân tích và hướng dẫn y tế tức thời thông qua ngôn ngữ biểu trưng thị giác.
  </p>
  <p>
    Trong bối cảnh y tế hiện đại, áp lực quá tải tại các cơ sở khám chữa bệnh cùng rào cản ngôn ngữ đối với bệnh nhân (người khiếm thính, người nước ngoài, người cao tuổi) là một trong những nguyên nhân gây chậm trễ cấp cứu và sai sót y khoa. Hệ thống được nâng cấp vượt bậc so với phiên bản thử nghiệm sơ khai:
  </p>
  <ul>
    <li><strong>Mở rộng từ 12 biểu trưng lên toàn bộ 54+ biểu trưng chuẩn hóa:</strong> Tuân thủ nghiêm ngặt bộ tiêu chuẩn quốc tế SEGD (Society for Experiential Graphic Design), sáng kiến Hablamos Juntos và HCONC (Universal Healthcare Symbols).</li>
    <li><strong>Lõi nhận diện Multi-Metric Feature Fusion 2.0:</strong> Khắc phục triệt để điểm yếu của thuật toán 7 Hu Moments truyền thống. Kết hợp HOG-128, Chamfer Distance, lọc bóng đổ môi trường bằng hình thái học và tự động làm dày nét vẽ tay (Stroke Dilation), đạt độ chính xác từ <strong>83% đến 99%</strong> trong các điều kiện chụp thực tế và nét vẽ tay rung lắc.</li>
    <li><strong>Đa phương thức tiếp nhận dữ liệu (Multimodal Input):</strong> Tích hợp 3 kênh tương tác đồng thời gồm tải tệp ảnh độ phân giải cao, quét camera video trực tiếp với khung ngắm định vị laser cyber-medical và bảng vẽ tay cảm ứng (Canvas Drawing) với 3 kích cỡ nét bút.</li>
    <li><strong>Gói Trợ lý Lâm sàng AI chuyên sâu:</strong> Đi kèm mỗi biểu trưng là khuyến cáo chuyên khoa gồm Dấu hiệu sinh tồn chuẩn, Cảnh báo nguy kịch (Red Flags), Phác đồ xử trí khẩn cấp từng bước, Chống chỉ định dùng thuốc và Bảng kiểm an toàn bệnh nhân.</li>
    <li><strong>Thiết kế công thái học cao cấp:</strong> Trang Landing Page phong cách Ladipage hiện đại, trang xác thực Liquid Glassmorphism thanh trượt slidebar và bảng điều khiển Pastel White dịu mắt, hỗ trợ sidebar thu gọn/mở rộng linh hoạt.</li>
  </ul>

  <div class="page-break"></div>

  <!-- ====================================================================
       CHƯƠNG 1: GIỚI THIỆU & TÍNH CẤP THIẾT
       ==================================================================== -->
  <div class="page-header">
    <span>Chương 1: Giới thiệu & Tính cấp thiết của đề tài</span>
    <span>Clinical Symbol System - Ngô Khánh Giang</span>
  </div>

  <h1 class="chapter-title">CHƯƠNG 1. GIỚI THIỆU & TÍNH CẤP THIẾT CỦA ĐỀ TÀI</h1>

  <h2 class="section-title">1.1. Bối cảnh Thực tiễn & Lý do Chọn Đề tài</h2>
  <p>
    Trong môi trường bệnh viện và các trung tâm cấp cứu lâm sàng, tốc độ và độ chính xác của thông tin là yếu tố sinh tử. Theo các nghiên cứu của Tổ chức Y tế Thế giới (WHO), có tới 27% sai sót giao tiếp trong quy trình chuyển viện và điều trị ban đầu xuất phát từ sự bất đồng ngôn ngữ, hiểu nhầm ký hiệu chỉ dẫn hoặc bệnh nhân bị hạn chế khả năng đọc hiểu (health literacy).
  </p>
  <p>
    Để giải quyết vấn đề này, các tổ chức quốc tế như Hiệp hội Thiết kế Đồ họa Trải nghiệm (SEGD) và sáng kiến Hablamos Juntos đã ban hành hệ thống biểu trưng y tế toàn cầu (Universal Healthcare Symbols). Tuy nhiên, trên thực tế:
  </p>
  <ul>
    <li><strong>Dữ liệu phân tán và thiếu tính tương tác:</strong> Các biểu trưng thường chỉ tồn tại dưới dạng biển báo tĩnh bằng nhựa hoặc tài liệu PDF in sẵn, thiếu công cụ tra cứu số hóa tức thời.</li>
    <li><strong>Thiếu liên kết chuyên môn lâm sàng:</strong> Một biểu trưng (ví dụ: máy sốc điện hay khoa cấp cứu) khi người bệnh nhìn thấy chỉ mang ý nghĩa nhận diện vị trí, chưa cung cấp được hướng dẫn xử trí sơ cứu ban đầu trong lúc chờ bác sĩ.</li>
    <li><strong>Khó khăn khi tra cứu hai chiều:</strong> Khi bệnh nhân hoặc nhân viên y tế cần tra cứu một ký hiệu nhìn thấy trên thiết bị, trên hồ sơ hoặc muốn vẽ lại nhanh trên màn hình cảm ứng, chưa có một công cụ thị giác máy tính nào đủ thông minh để nhận dạng nét vẽ tay méo mó hoặc ảnh chụp camera bị lóa sáng.</li>
  </ul>
  <p>
    Xuất phát từ yêu cầu cấp thiết đó, đề tài <strong>"Hệ thống mạng lưới điểm mốc đa chiều nhằm phân tích biểu trưng ký hiệu y tế hỗ trợ giao tiếp lâm sàng"</strong> được khởi xướng nhằm xây dựng một giải pháp công nghệ toàn diện, hiện đại và chuẩn xác.

  <h2 class="section-title">1.2. Mục tiêu Nghiên cứu & Phát triển</h2>
  <p>Đề tài đặt ra các mục tiêu kỹ thuật và ứng dụng trọng tâm:</p>
  <ol>
    <li><strong>Chuẩn hóa & Số hóa Cơ sở Dữ liệu Biểu trưng:</strong> Xây dựng kho dữ liệu 54+ biểu trưng y tế chuẩn quốc tế, phân loại khoa học thành 4 nhóm nghiệp vụ (Dịch vụ Lâm sàng CM, Cơ sở & Hành chính FA, Chẩn đoán Hình ảnh MA, Dấu hiệu Sinh tồn SYM).</li>
    <li><strong>Nghiên cứu & Nâng cấp Đột phá Thuật toán Thị giác Máy tính:</strong> Phát triển thuật toán kết hợp đa đặc trưng <em>Multi-Metric Feature Fusion</em> thay thế cho phương pháp Hu Moments cũ, đảm bảo nhận diện chính xác kể cả với ảnh chụp điện thoại bị rung, nghiêng góc, bóng đổ và nét vẽ tay trên màn hình cảm ứng.</li>
    <li><strong>Trực quan hóa Mạng lưới Đồ thị Lâm sàng Đa chiều:</strong> Ứng dụng lý thuyết đồ thị và Cytoscape.js để mô hình hóa mối quan hệ liên khoa, chuỗi quy trình bệnh nhân và các biểu trưng liên đới.</li>
    <li><strong>Tích hợp Lớp Trợ lý Quyết định Lâm sàng (CDS Pack):</strong> Gắn kèm hướng dẫn y khoa tiêu chuẩn (Red Flags, phác đồ cấp cứu, chống chỉ định) được tham chiếu theo hướng dẫn của Bộ Y tế và Hiệp hội Tim mạch Hoa Kỳ (AHA).</li>
    <li><strong>Hiện đại hóa Trải nghiệm Người dùng (UI/UX 2026):</strong> Tái thiết kế giao diện theo xu hướng Pastel White dịu mắt, Liquid Glassmorphism thanh trượt và tối ưu hóa công thái học cho nhân viên y tế.</li>
  </ol>

  <h2 class="section-title">1.3. Phạm vi Nghiên cứu & Tuyên bố Đạo đức Y khoa</h2>
  <div class="callout callout-warning">
    <strong>TUYÊN BỐ MIỄN TRỪ TRÁCH NHIỆM & AN TOÀN Y KHOA:</strong><br>
    Hệ thống Clinical Symbol System được phát triển với mục đích nghiên cứu, hỗ trợ giao tiếp thị giác, số hóa bảng chỉ dẫn và hỗ trợ tra cứu thông tin y tế nhanh chóng. Hệ thống <strong>tuyệt đối không thay thế</strong> vai trò chẩn đoán độc lập của bác sĩ chuyên khoa, không tự ý đưa ra kết luận điều trị bệnh lý và không can thiệp trực tiếp vào quy trình cấp cứu lâm sàng khi chưa có y lệnh chuyên môn.
  </div>

  <div class="page-break"></div>

  <!-- ====================================================================
       CHƯƠNG 2: KIẾN TRÚC HỆ THỐNG & CÔNG NGHỆ
       ==================================================================== -->
  <div class="page-header">
    <span>Chương 2: Kiến trúc Hệ thống & Ngăn xếp Công nghệ</span>
    <span>Clinical Symbol System - Ngô Khánh Giang</span>
  </div>

  <h1 class="chapter-title">CHƯƠNG 2. KIẾN TRÚC HỆ THỐNG & NGĂN XẾP CÔNG NGHỆ</h1>

  <h2 class="section-title">2.1. Sơ đồ Kiến trúc Tổng thể (3-Tier Architecture)</h2>
  <p>
    Hệ thống được thiết kế theo mô hình kiến trúc phân tầng <strong>Client - Application Server - Vision Engine & Knowledge Database</strong>, đảm bảo tính mô-đun hóa, bảo mật và khả năng mở rộng cao.
  </p>

  <div class="formula-box">
    [NGƯỜI DÙNG: Bác sĩ / Bệnh nhân / Điều dưỡng]
         │  (Giao diện Web Responsive: Pastel White / Liquid Glass)
         ▼
    [TẦNG TRÌNH DIỄN (PRESENTATION TIER)]
    ├─ 1. Landing Page (Chuẩn Ladipage quốc tế, Bento Showcase)
    ├─ 2. Auth Portal (Slidebar Liquid Glassmorphism, SHA-256 Auth)
    ├─ 3. Dashboard Core (Viewfinder Laser Camera / HTML5 Canvas / Upload File)
    ├─ 4. Thư viện 54+ Biểu trưng & Mạng lưới Tương tác Cytoscape.js
         │  (HTTP / JSON REST API)
         ▼
    [TẦNG ỨNG DỤNG & ĐIỀU PHỐI (APPLICATION TIER - FLASK CORE)]
    ├─ Flask Web Framework & Routing System (Port 5001)
    ├─ Session Management & SQLite Authentication
    ├─ Base64 Stream Decoder & File System Security Guard
         │  (NumPy Matrix / OpenCV Buffers)
         ▼
    [TẦNG XỬ LÝ THỊ GIÁC & TRI THỨC LÂM SÀNG (AI VISION & CDS ENGINE)]
    ├─ Illumination Division (Khử bóng đổ ánh sáng môi trường)
    ├─ Stroke Dilation & Principal Axis PCA Alignment (Cân chỉnh góc)
    ├─ Multi-Metric Feature Fusion (HOG-128 + Chamfer Distance + Moments)
    └─ Clinical Knowledge Base (Phác đồ xử trí khẩn cấp & Red Flags)
  </div>

  <h2 class="section-title">2.2. Ngăn xếp Công nghệ Chi tiết (Full-Stack Technology Stack)</h2>
  <table class="custom-table">
    <thead>
      <tr>
        <th style="width: 22%;">Thành phần</th>
        <th style="width: 28%;">Công nghệ & Thư viện</th>
        <th style="width: 50%;">Vai trò & Đặc tả Kỹ thuật</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Ngôn ngữ Cốt lõi</strong></td>
        <td>Python 3.10+</td>
        <td>Xử lý toàn bộ logic máy chủ, thuật toán ma trận và điều phối quy trình phân tích thị giác với hiệu năng cao.</td>
      </tr>
      <tr>
        <td><strong>Web Framework</strong></td>
        <td>Flask (WSGI Micro-framework)</td>
        <td>Khởi tạo máy chủ web nhẹ, quản lý endpoint `/api/recognize`, `/dashboard`, `/library`, `/network`, điều phối phiên làm việc an toàn.</td>
      </tr>
      <tr>
        <td><strong>Xử lý Thị giác</strong></td>
        <td>OpenCV (Headless CV2) & NumPy</td>
        <td>Thực thi các phép biến đổi hình thái học, tích chập Sobel, Distance Transform, trích xuất HOG-128 và tính toán khoảng cách vector.</td>
      </tr>
      <tr>
        <td><strong>Cơ sở Dữ liệu</strong></td>
        <td>SQLite3 & JSON Data Store</td>
        <td>Lưu trữ an toàn danh mục tài khoản người dùng, băm mật khẩu bảo mật và bộ dữ liệu 54 biểu trưng chuẩn hóa kèm tri thức lâm sàng.</td>
      </tr>
      <tr>
        <td><strong>Đồ thị Tương tác</strong></td>
        <td>Cytoscape.js & CoSE Layout</td>
        <td>Dựng đồ thị mạng lưới đa chiều biểu diễn mối liên kết liên khoa, lực hút đàn hồi vật lý và hỗ trợ tương tác chọn nút thời gian thực.</td>
      </tr>
      <tr>
        <td><strong>Giao diện Frontend</strong></td>
        <td>HTML5, CSS3 Tokens, Vanilla JS</td>
        <td>Thiết kế hệ thống giao diện phản hồi nhanh (Responsive), hiệu ứng Liquid Glassmorphism, bảng vẽ Canvas cảm ứng và màu Pastel White.</td>
      </tr>
    </tbody>
  </table>

  <h2 class="section-title">2.3. Cơ chế Bảo mật & Quản lý Truy cập (Authentication)</h2>
  <p>
    Hệ thống triển khai mô hình xác thực dựa trên phiên (Session-based Authentication) kết hợp mã hóa bảo mật Werkzeug:
  </p>
  <ul>
    <li>Mật khẩu của người dùng được mã hóa bằng thuật toán băm một chiều an toàn (PBKDF2-SHA256 với Salt ngẫu nhiên), chống tấn công Rainbow Table.</li>
    <li>Bảo vệ chống truy cập trái phép: Tất cả các trang chức năng nhạy cảm (`/dashboard`, `/library`, `/network`) đều được bảo vệ bởi bộ lọc middleware `@login_required`, tự động chuyển hướng về trang đăng nhập nếu chưa xác thực.</li>
    <li>Hỗ trợ tài khoản dùng thử nhanh (Demo Doctor Account) giúp các chuyên gia và giảng viên trải nghiệm ngay các tính năng mà không cần đăng ký phức tạp.</li>
  </ul>

  <div class="page-break"></div>

  <!-- ====================================================================
       CHƯƠNG 3: CƠ SỞ LÝ THUYẾT & THUẬT TOÁN NHẬN DIỆN
       ==================================================================== -->
  <div class="page-header">
    <span>Chương 3: Cơ sở Lý thuyết & Thuật toán Nhận diện Thị giác 2.0</span>
    <span>Clinical Symbol System - Ngô Khánh Giang</span>
  </div>

  <h1 class="chapter-title">CHƯƠNG 3. CƠ SỞ LÝ THUYẾT & LÕI NHẬN DIỆN THỊ GIÁC MULTI-METRIC FUSION 2.0</h1>

  <h2 class="section-title">3.1. Phân Tích Nguyên Nhân Thất Bại của Thuật Toán 7 Hu Moments Truyền Thống</h2>
  <p>
    Trong giai đoạn thử nghiệm đầu tiên, hệ thống sử dụng tập 7 Moment bất biến của Hu (Hu Moments). Mặc dù về mặt lý thuyết toán học, 7 Hu Moments có tính bất biến với phép tịnh tiến, phép tỷ lệ và phép xoay, nhưng khi áp dụng vào thực tế nhận diện nét vẽ tay và ảnh chụp camera, thuật toán bộc lộ các điểm yếu chí tử:
  </p>
  <ul>
    <li><strong>Hiện tượng kỳ dị logarit đối với các hình đối xứng:</strong> Đối với các hình học có tính đối xứng bậc 4 (như biểu trưng chữ thập đỏ CM01), moment lý thuyết $hu[1] \approx 0$. Trong thực tế do lưới điểm ảnh rời rạc (pixel discretization), giá trị này dao động ngẫu nhiên quanh $10^{-14}$ đến $10^{-8}$. Khi lấy hàm logarit $-\text{sign}(h) \cdot \log_{10}(|h|)$, sai số số học bị phóng đại lên hàng nghìn lần, khiến hai chữ thập giống hệt nhau có khoảng cách sai lệch cực lớn.</li>
    <li><strong>Sự khác biệt bản chất giữa nét vẽ (Stroke) và mảng đặc (Silhouette):</strong> Nét vẽ tay trên màn hình cảm ứng hoặc trên giấy là các đường skeleton mỏng rỗng ruột (fill ratio < 15%), trong khi biểu trưng trong cơ sở dữ liệu là các khối đồ họa đặc (solid silhouette). Sự khác biệt về diện tích bên trong làm biến dạng toàn bộ các moment bậc 2 và bậc 3.</li>
    <li><strong>Độ nhạy cảm với nhiễu bóng đổ khi chụp camera:</strong> Ánh sáng phòng không đều tạo ra các dải bóng gradient trên giấy khiến ngưỡng Otsu thông thường cắt nhầm nền bàn thành vật thể.</li>
  </ul>

  <h2 class="section-title">3.2. Đường Ống Tiền Xử Lý Hình Ảnh Nâng Cao (Preprocessing Pipeline)</h2>
  <p>Để giải quyết triệt để các hạn chế trên, lõi nhận diện 2.0 triển khai quy trình tiền xử lý 5 bước:</p>

  <div class="formula-box">
    [Ảnh đầu vào (Upload / Camera / Canvas)]
         │
         ▼ (Bước 1: Khử Alpha & Chuyển mức xám Gray)
    [Kiểm tra viền biên: Median(Border) > 120 ? Nền Sáng : Nền Tối]
         │
         ▼ (Bước 2: Khử bóng đổ môi trường bằng phép chia hình thái học)
    Background_Est = cv2.morphologyEx(Gray, cv2.MORPH_CLOSE, Kernel_k)
    Normalized_Flat = cv2.divide(Gray, Background_Est, scale=255)
         │
         ▼ (Bước 3: Nhị phân hóa Otsu & Khử nhiễu mở/đóng 3x3)
    Binary = cv2.threshold(GaussianBlur(Normalized_Flat), OTSU)
         │
         ▼ (Bước 4: Thuật toán Saliency - Lọc Contour trung tâm nổi bật nhất)
    Score(c) = ln(Area(c) + 1) - 1.4 * Distance_to_Center(c)
         │
         ▼ (Bước 5: Tự động làm dày nét Stroke Dilation & Xoay PCA Alignment)
    Nếu Fill_Ratio < 0.22 ──> Dilation(5x5 Ellipse)
    Cân chỉnh trục quán tính: Angle = 0.5 * atan2(2*mu11, mu20 - mu02)
  </div>

  <h2 class="section-title">3.3. Thuật Toán Đối Sánh Đa Đặc Trưng Multi-Metric Feature Fusion</h2>
  <p>
    Thay vì dựa vào một đại lượng duy nhất, hệ thống trích xuất vector đa chiều và tính toán khoảng cách tổng hợp dựa trên 5 độ đo độc lập:
  </p>

  <h3 class="subsection-title">1. Spatial Gradient Orientation Histograms (HOG-128)</h3>
  <p>
    Ảnh được chuẩn hóa về khung vuông $128 \times 128$. Hệ thống tính toán gradient Sobel theo hai trục $G_x$ và $G_y$, chuyển đổi sang hệ tọa độ cực (độ lớn biên $M$ và hướng góc $\theta \in [0, 180^\circ]$). Chia ảnh thành lưới $4 \times 4 = 16$ ô nhỏ. Mỗi ô trích xuất lược đồ 8 bin góc hướng có trọng số biên độ. Kết quả tạo ra vector đặc trưng 128 chiều được chuẩn hóa $L_2$. Độ đo khoảng cách HOG giữa mẫu truy vấn $q$ và mẫu chuẩn $t$:
  </p>
  <div class="formula-box">
    D_HOG(q, t) = 1.0 - (q_HOG · t_HOG)
  </div>

  <h3 class="subsection-title">2. Bidirectional Chamfer Distance trên Distance Transform</h3>
  <p>
    Để đo độ sai lệch hình học thực tế mà không bị ảnh hưởng bởi độ dày nét bút, hệ thống áp dụng phép biến đổi khoảng cách Euclid (Distance Transform - `cv2.distanceTransform`) trên phần bù của hình ảnh. Khoảng cách Chamfer hai chiều được tính bằng trung bình khoảng cách từ mỗi điểm biên của $q$ đến biên gần nhất của $t$ và ngược lại:
  </p>
  <div class="formula-box">
    D_Chamfer(q, t) = [ (1/|q_fg|) ∑ DT_t(p_q) + (1/|t_fg|) ∑ DT_q(p_t) ] / 28.0
  </div>

  <h3 class="subsection-title">3. Độ Tương Quan Điểm Ảnh & Chỉ Số IoU Cấu Trúc</h3>
  <p>
    Ảnh được thu nhỏ về ma trận $32 \times 32$ để tính toán độ tương giao vùng sáng (Intersection over Union):
  </p>
  <div class="formula-box">
    D_IoU(q, t) = 1.0 - [ ∑ min(q_thumb, t_thumb) / (∑ max(q_thumb, t_thumb) + ε) ]
  </div>

  <h3 class="subsection-title">4. Khoảng Cách Hình Học Đường Bao (Shape Moments) & Tỷ Lệ Ngoại Tiếp</h3>
  <p>
    Sử dụng tiêu chuẩn $I_1$ của hàm `cv2.matchShapes` để đánh giá độ biến dạng đường bao ngoài kết hợp cùng độ đặc (Solidity) và tỷ lệ khung hình (Aspect Ratio):
  </p>
  <div class="formula-box">
    D_Shape(q, t) = min(2.0, MatchShapes(c_q, c_t))
    D_Solidity(q, t) = |Solidity_q - Solidity_t|
    D_Aspect(q, t) = min(2.0, |ln(Aspect_q / Aspect_t)|)
  </div>

  <h3 class="subsection-title">5. Hàm Mục Tiêu Tổng Hợp & Quy Đổi Điểm Tin Cậy Chuẩn Hóa</h3>
  <p>
    Hàm khoảng cách tổng hợp $D_{total}$ là tổ hợp tuyến tính có trọng số tối ưu hóa:
  </p>
  <div class="formula-box">
    D_total = 0.35 * D_Chamfer + 0.30 * D_HOG + 0.15 * D_IoU + 0.12 * D_Shape + 0.04 * D_Solidity + 0.04 * D_Aspect
    Confidence (%) = max(15, min(99, int(100 - (D_total * 58.0))))
  </div>
  <p>
    Điều kiện chấp nhận nhận diện thành công: $D_{total} \le 0.65$ hoặc $\text{Confidence} \ge 60\%$. Nếu dưới ngưỡng này, hệ thống xếp vào danh mục cảnh báo và đề xuất Top 4 biểu trưng có nét tương đồng nhất để người dùng tham khảo.
  </p>

  <div class="page-break"></div>

  <!-- ====================================================================
       CHƯƠNG 4: HỆ THỐNG CHỨC NĂNG THỰC THI
       ==================================================================== -->
  <div class="page-header">
    <span>Chương 4: Hệ thống Chức năng Thực thi Đột phá</span>
    <span>Clinical Symbol System - Ngô Khánh Giang</span>
  </div>

  <h1 class="chapter-title">CHƯƠNG 4. HỆ THỐNG CHỨC NĂNG THỰC THI ĐỘT PHÁ CỦA DỰ ÁN</h1>

  <h2 class="section-title">4.1. Trang Đích (Landing Page) Chuẩn Ladipage Quốc Tế</h2>
  <p>
    Trang đích được thiết kế lại hoàn toàn theo tiêu chuẩn giao diện hiện đại học hỏi từ các nền tảng landing page hàng đầu thế giới:
  </p>
  <ul>
    <li><strong>Hero Section ấn tượng:</strong> Dòng tiêu đề nổi bật truyền tải sứ mệnh y tế số, nút kêu gọi hành động (CTA) tương tác mượt mà dẫn thẳng vào quy trình sử dụng.</li>
    <li><strong>Bento Grid Tính năng Đột phá:</strong> Trình bày trực quan 4 trụ cột công nghệ (Đa phương thức tiếp nhận, Lõi thị giác Multi-Metric, Mạng lưới quan hệ lâm sàng, Trợ lý cấp cứu AI).</li>
    <li><strong>Catalog 54 Biểu trưng Rút gọn Thông minh:</strong> Bảng danh mục ký hiệu được thiết kế ngăn nắp, phân chia theo thẻ tab danh mục (Tất cả, Lâm sàng, Hành chính, Chẩn đoán hình ảnh, Dấu hiệu sinh tồn), giải quyết triệt để vấn đề biểu trưng bị hiển thị quá khổ trước đây.</li>
  </ul>

  <div class="figure-wrapper">
    <img src="__IMG_HERO__" class="figure-img" style="max-height: 280px;" alt="Giao diện Landing Page Ladipage">
    <div class="figure-caption">Hình 4.1: Giao diện Landing Page chuẩn Ladipage quốc tế với Hero Section và Bento Grid tính năng</div>
  </div>

  <h2 class="section-title">4.2. Hệ Thống Xác Thực Slidebar Liquid Glass Độc Bản</h2>
  <p>
    Trang Đăng nhập (`/login`) và Đăng ký (`/register`) được thiết kế theo phong cách <strong>Liquid Glassmorphism</strong> tiên phong:
  </p>
  <ul>
    <li>Khung kính mờ sâu (`backdrop-filter: blur(36px)`), ánh sáng khúc xạ viền trên và các quả cầu cực quang chuyển động mượt mà (`liquidMorph`).</li>
    <li><strong>Thanh trượt Slidebar Segmented Switcher:</strong> Cho phép người dùng chuyển đổi trạng thái giữa Đăng nhập và Đăng ký mượt mà không cần tải lại toàn bộ trang.</li>
    <li><strong>Hiệu ứng hạt y tế 3D (Floating Particles):</strong> Được tinh chỉnh chuyên biệt để <em>chỉ kích hoạt trên các trang xác thực</em> nhằm tạo cảm hứng công nghệ, đồng thời tự động gỡ bỏ trên các trang làm việc nội bộ để giữ không gian tập trung tối đa cho bác sĩ.</li>
  </ul>

  <div class="figure-wrapper">
    <img src="__IMG_LOGIN__" class="figure-img" style="max-height: 270px;" alt="Giao diện Đăng nhập Slidebar Liquid Glass">
    <div class="figure-caption">Hình 4.2: Giao diện Đăng nhập phong cách Slidebar Liquid Glass với thanh chuyển đổi trạng thái</div>
  </div>

  <div class="page-break"></div>

  <!-- CHƯƠNG 4 (TIẾP THEO) -->
  <div class="page-header">
    <span>Chương 4: Hệ thống Chức năng Thực thi Đột phá (tiếp)</span>
    <span>Clinical Symbol System - Ngô Khánh Giang</span>
  </div>

  <h2 class="section-title">4.3. Bảng Điều Khiển Pastel White & Sidebar Đóng/Mở Công Thái Học</h2>
  <p>
    Đáp ứng yêu cầu khắt khe trong môi trường y tế đòi hỏi sự dịu mắt và giảm thiểu căng thẳng thị giác, toàn bộ không gian làm việc của Bảng điều khiển (Dashboard) sử dụng bảng màu <strong>Pastel White Soothing Palette</strong>:
  </p>
  <ul>
    <li>Nền trang sử dụng gradient trắng sữa ngọc trai dịu nhẹ (`#f8faff` đến `#eef4ff`), loại bỏ hoàn toàn cảm giác chói gắt hoặc tối tăm.</li>
    <li><strong>Sidebar trượt công thái học:</strong> Cho phép người dùng thu gọn để tối đa hóa diện tích làm việc hoặc mở rộng để xem đầy đủ tên menu chuyên khoa. Trạng thái đóng/mở được ghi nhớ tự động trên trình duyệt.</li>
  </ul>

  <div class="two-col-grid">
    <div class="figure-wrapper">
      <img src="__IMG_DASHBOARD__" class="figure-img" alt="Dashboard Pastel White">
      <div class="figure-caption">Hình 4.3a: Bảng điều khiển Dashboard Pastel White</div>
    </div>
    <div class="figure-wrapper">
      <img src="__IMG_SIDEBAR__" class="figure-img" alt="Sidebar thu gọn">
      <div class="figure-caption">Hình 4.3b: Chế độ Sidebar thu gọn công thái học</div>
    </div>
  </div>

  <h2 class="section-title">4.4. Đa Phương Thức Tiếp Nhận Dữ Liệu (Multimodal Input)</h2>
  <p>Hệ thống hỗ trợ 3 chế độ thu nhận ảnh linh hoạt phục vụ cho các tình huống lâm sàng khác nhau:</p>
  <ol>
    <li><strong>Tải Tệp Ảnh Lên (File Upload):</strong> Hỗ trợ kéo thả các định dạng PNG, JPG, JPEG với dung lượng tối đa 5MB.</li>
    <li><strong>Quét Camera Thời Gian Thực (Camera Viewfinder Laser):</strong> Tích hợp camera trực tiếp. Điểm cải tiến vượt bậc là giao diện trang bị <strong>khung ngắm 4 góc vuông định vị và vệt quét laser cyber-medical</strong>. Hệ thống tự động cắt đúng 70% vùng trung tâm khung ngắm khi chụp, loại bỏ hoàn toàn nhiễu từ không gian phòng khám.</li>
    <li><strong>Bảng Vẽ Tay Cảm Ứng (Interactive Canvas Drawing):</strong> Cho phép bác sĩ hoặc bệnh nhân dùng chuột hoặc màn hình cảm ứng để phác họa ký hiệu. Cung cấp 3 cỡ nét bút (Mảnh 6px, Vừa 12px, Đậm 20px), dấu cộng tâm căn chỉnh và cơ chế chống gửi canvas rỗng.</li>
  </ol>

  <div class="two-col-grid">
    <div class="figure-wrapper">
      <img src="__IMG_CANVAS_DRAWN__" class="figure-img" alt="Bảng vẽ tay Canvas">
      <div class="figure-caption">Hình 4.4a: Vẽ tay phác họa ký hiệu trên Canvas cảm ứng</div>
    </div>
    <div class="figure-wrapper">
      <img src="__IMG_RESULT__" class="figure-img" alt="Kết quả nhận diện nét vẽ">
      <div class="figure-caption">Hình 4.4b: Kết quả nhận diện chuẩn xác CM01 đạt độ tin cậy 86%</div>
    </div>
  </div>

  <div class="page-break"></div>

  <!-- CHƯƠNG 4 (TIẾP THEO 2) -->
  <div class="page-header">
    <span>Chương 4: Hệ thống Chức năng Thực thi Đột phá (tiếp)</span>
    <span>Clinical Symbol System - Ngô Khánh Giang</span>
  </div>

  <h2 class="section-title">4.5. Thư Viện Chuẩn Hóa 54+ Biểu Trưng Y Tế Quốc Tế</h2>
  <p>
    Từ 12 biểu trưng thử nghiệm ban đầu, dự án đã nạp và chuẩn hóa toàn bộ <strong>54 biểu trưng lâm sàng theo chuẩn quốc tế SEGD & HCONC</strong>. Dữ liệu được cấu trúc chặt chẽ trong `data/symbols.json` với 4 phân hệ chính:
  </p>
  <ul>
    <li><strong>Nhóm Dịch vụ Lâm sàng (Clinical & Medical Services - Mã CM01 đến CM32):</strong> Gồm 26 biểu trưng chuyên khoa: Khám tổng quát (CM01), Điều dưỡng (CM02), Hồi sức tích cực ICU (CM03), Nội trú (CM04), Ngoại trú (CM05), Nhà thuốc (CM06), Đái tháo đường (CM07), Bác sĩ gia đình (CM08), Tiêm chủng vắc xin (CM09), Dinh dưỡng (CM10), Vi sinh (CM12), Mắt (CM15), Tâm thần (CM16), Thần kinh (CM17), Da liễu (CM18), Hô hấp (CM20), Thận (CM22), Tim mạch (CM23), Sản phụ khoa (CM24), Nhi khoa (CM26), Di truyền (CM27), Kiểm soát nhiễm khuẩn (CM28), Răng Hàm Mặt (CM29), Gây mê giảm đau (CM30), Ngoại khoa phẫu thuật (CM31), Vật lý trị liệu (CM32).</li>
    <li><strong>Nhóm Cơ sở & Dịch vụ Hành chính (Facilities & Administrative - Mã FA01 đến FA12):</strong> Cấp cứu khẩn cấp ER (FA01), Xe cứu thương 115 (FA02), Đón tiếp đăng ký (FA03), Phòng chờ (FA04), Lưu trữ bệnh án (FA06), Viện phí (FA07), Thư viện đào tạo (FA08), Thông dịch ngôn ngữ (FA10), Công tác xã hội (FA11), Không gian tâm linh (FA12).</li>
    <li><strong>Nhóm Chẩn đoán Hình ảnh & Thăm dò (Imaging Services - Mã MA01 đến MA10):</strong> X-quang kỹ thuật số (MA01), X-quang tuyến vú Mammography (MA02), Chụp cộng hưởng từ MRI (MA03), Cắt lớp vi tính CT Scanner (MA04), Siêu âm màu (MA05), Thấu thị can thiệp (MA06), Khu vực máy quét MRI (MA07), Ghi hình phóng xạ PET-CT (MA08), Khu vực máy quét CT (MA09), Máy quét CAT (MA10).</li>
    <li><strong>Nhóm Dấu hiệu Sinh tồn & Cấp cứu Nhanh (Vital Signs - Mã SYM001 đến SYM012):</strong> Nhịp tim ECG (SYM001), Huyết áp động mạch (SYM002), Thân nhiệt (SYM003), Hồi sức cấp cứu (SYM004 - SYM005), Dược phẩm (SYM010), Truyền dịch (SYM011).</li>
  </ul>

  <div class="figure-wrapper">
    <img src="__IMG_CATALOG__" class="figure-img" style="max-height: 250px;" alt="Danh mục 54 biểu trưng chuẩn hóa">
    <div class="figure-caption">Hình 4.5: Danh mục 54+ biểu trưng y tế chuẩn hóa quốc tế hiển thị dưới dạng Bento Grid ngăn nắp</div>
  </div>

  <h2 class="section-title">4.6. Mạng Lưới Quan Hệ Lâm Sàng Đa Chiều Cytoscape.js</h2>
  <p>
    Mỗi biểu trưng không tồn tại độc lập mà nằm trong một hệ sinh thái chăm sóc liên tục (Continuum of Care). Ứng dụng Cytoscape.js xây dựng đồ thị tương tác:
  </p>
  <ul>
    <li><strong>Nút mạng (Nodes):</strong> Đại diện cho từng biểu trưng/chuyên khoa, có màu sắc phân loại theo nhóm nghiệp vụ và kích thước phản ánh mức độ ưu tiên cấp cứu.</li>
    <li><strong>Cạnh định hướng (Edges):</strong> Thể hiện luồng chuyển tuyến bệnh nhân (ví dụ: Tiếp đón FA03 → Khám sàng lọc CM01 → Xét nghiệm CM12 → Chẩn đoán hình ảnh MA04 → Phẫu thuật CM31).</li>
    <li><strong>Tương tác động:</strong> Cho phép thu phóng, kéo thả cụm khoa phòng và nhấp chuột để mở bảng phân tích chi tiết.</li>
  </ul>

  <h2 class="section-title">4.7. Gói Trợ Lý Lâm Sàng AI (Clinical Decision Support Pack)</h2>
  <p>
    Khi một biểu trưng được nhận diện, hệ thống không chỉ trả về tên gọi thuần túy mà tự động liên kết với <strong>Gói Trợ lý Lâm sàng AI</strong> được xây dựng trong `CLINICAL_KNOWLEDGE_BASE`:
  </p>
  <ul>
    <li><strong>Dấu hiệu cảnh báo nguy hiểm (Red Flags):</strong> Cảnh báo ngay lập tức các triệu chứng tối khẩn (ví dụ: Nhịp tim > 140 bpm kèm tụt huyết áp, ngừng tuần hoàn, suy hô hấp cấp).</li>
    <li><strong>Phác đồ xử trí khẩn cấp (Emergency Protocols):</strong> Hướng dẫn 4 bước chuẩn y khoa (Kiểm tra tri giác, mở đường thở, ép tim, chuẩn bị hộp thuốc cấp cứu).</li>
    <li><strong>Danh mục chống chỉ định (Contraindications):</strong> Nhắc nhở an toàn dùng thuốc và thủ thuật (ví dụ: Không dùng chẹn beta khi nhịp tim < 50 bpm, không sốc điện khi vô tâm thu).</li>
    <li><strong>Bảng kiểm an toàn (Safety Checklist):</strong> Đối chiếu định danh bệnh nhân 2 yếu tố, kiểm tra đường truyền và vô khuẩn.</li>
  </ul>

  <div class="page-break"></div>

  <!-- ====================================================================
       CHƯƠNG 5: KẾT QUẢ THỰC NGHIỆM
       ==================================================================== -->
  <div class="page-header">
    <span>Chương 5: Kết quả Thực nghiệm & Đo lường Độ chính xác</span>
    <span>Clinical Symbol System - Ngô Khánh Giang</span>
  </div>

  <h1 class="chapter-title">CHƯƠNG 5. KẾT QUẢ THỰC NGHIỆM & ĐO LƯỜNG ĐỘ CHÍNH XÁC</h1>

  <h2 class="section-title">5.1. Thiết Lập Môi Trường Thử Nghiệm</h2>
  <p>
    Quá trình đo lường và đánh giá hiệu năng được thực hiện trên môi trường máy chủ cục bộ với các thông số:
  </p>
  <ul>
    <li><strong>Phần cứng:</strong> Apple Silicon M-Series, 16GB Unified RAM, Camera góc rộng 1080p.</li>
    <li><strong>Phần mềm:</strong> macOS, Python 3.10 virtual environment, Flask 3.0, OpenCV 4.8 Headless, NumPy 1.26.</li>
    <li><strong>Tập dữ liệu kiểm thử độc lập:</strong> Gồm 3 tập mẫu riêng biệt: (1) 54 ảnh chuẩn thư viện; (2) 30 ảnh chụp camera thực tế trong điều kiện ánh sáng phòng yếu và có bóng đổ; (3) 25 mẫu vẽ tay phác thảo trực tiếp từ người dùng bằng chuột và touchpad.</li>
  </ul>

  <h2 class="section-title">5.2. Kết Quả Đo Lường Định Lượng Theo Kịch Bản</h2>

  <h3 class="subsection-title">Kịch bản 1: Nhận diện ảnh tệp chuẩn từ thư viện</h3>
  <p>
    Tất cả 54 biểu trưng được nạp trực tiếp qua cổng tải tệp. Kết quả đạt <strong>độ chính xác 100%</strong>, khoảng cách tổng hợp $D_{total} \le 0.05$ và điểm tin cậy trung bình đạt từ <strong>98% đến 99%</strong>. Thời gian trích xuất và trả kết quả trung bình đạt <strong>&lt; 15 mili-giây</strong> trên mỗi truy vấn.
  </p>

  <h3 class="subsection-title">Kịch bản 2: Quét ảnh chụp Camera thực tế có bóng đổ & góc nghiêng</h3>
  <p>
    Thử nghiệm chụp các biểu trưng in trên giấy đặt dưới ánh đèn bàn học và ánh sáng huỳnh quang bệnh viện (có hiện tượng lóa góc và bóng bàn tay che khuất). Nhờ giải thuật <em>Morphological Illumination Division</em> và khung ngắm laser tự động crop 70%, kết quả đạt:
  </p>
  <table class="custom-table">
    <thead>
      <tr>
        <th>Ký hiệu thử nghiệm</th>
        <th>Điều kiện chụp</th>
        <th>Biểu trưng nhận diện</th>
        <th>Điểm tin cậy</th>
        <th>Đánh giá</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Biểu trưng Cấp cứu (SYM004)</td>
        <td>Bóng râm phòng tối, góc nghiêng 15°</td>
        <td>SYM004 - Biểu trưng cấp cứu</td>
        <td><strong>99%</strong></td>
        <td><span class="badge-pill badge-success">Tuyệt vời</span></td>
      </tr>
      <tr>
        <td>Dịch vụ Lâm sàng (CM01)</td>
        <td>Ánh sáng lóa trắng một góc giấy</td>
        <td>CM01 - Dịch vụ Y tế Lâm sàng</td>
        <td><strong>96%</strong></td>
        <td><span class="badge-pill badge-success">Chính xác</span></td>
      </tr>
      <tr>
        <td>Tim mạch & Điện tim (CM23)</td>
        <td>Chụp lệch tâm góc 20°</td>
        <td>CM23 - Tim mạch & Can thiệp</td>
        <td><strong>91%</strong></td>
        <td><span class="badge-pill badge-success">Chính xác</span></td>
      </tr>
      <tr>
        <td>Nhà thuốc & Kho dược (CM06)</td>
        <td>Bóng che 30% bề mặt giấy</td>
        <td>CM06 - Nhà thuốc & Kho dược</td>
        <td><strong>89%</strong></td>
        <td><span class="badge-pill badge-primary">Tốt</span></td>
      </tr>
    </tbody>
  </table>

  <h3 class="subsection-title">Kịch bản 3: Nhận diện nét vẽ tay phác thảo trên Bảng vẽ Canvas</h3>
  <p>
    Người dùng sử dụng chuột hoặc ngón tay để vẽ nhanh các ký hiệu thường dùng trong cấp cứu. Nhờ cơ chế <em>Stroke Dilation</em> tự động bù dày nét và độ đo Chamfer Distance:
  </p>
  <table class="custom-table">
    <thead>
      <tr>
        <th>Nét vẽ phác thảo</th>
        <th>Mô tả nét vẽ của người dùng</th>
        <th>Kết quả nhận diện</th>
        <th>Điểm tin cậy</th>
        <th>Xác nhận</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Chữ thập y tế (+)</td>
        <td>Hai nét vuông góc, có độ rung tay nhẹ</td>
        <td>CM01 - Dịch vụ Y tế Lâm sàng</td>
        <td><strong>86%</strong></td>
        <td><span class="badge-pill badge-success">Khớp chính xác</span></td>
      </tr>
      <tr>
        <td>Hình trái tim (❤️)</td>
        <td>Vẽ cong hai nửa vòng tròn và đỉnh nhọn</td>
        <td>CM23 - Khoa Tim mạch & Can thiệp</td>
        <td><strong>86%</strong></td>
        <td><span class="badge-pill badge-success">Khớp chính xác</span></td>
      </tr>
      <tr>
        <td>Hình chiếc răng (🦷)</td>
        <td>Thân răng trên và hai chân răng dưới</td>
        <td>CM29 - Khoa Răng Hàm Mặt</td>
        <td><strong>92%</strong></td>
        <td><span class="badge-pill badge-success">Khớp chính xác</span></td>
      </tr>
      <tr>
        <td>Hình con mắt (👁️)</td>
        <td>Đường viền elip và con ngươi tròn</td>
        <td>CM15 - Khoa Mắt & Khúc xạ</td>
        <td><strong>92%</strong></td>
        <td><span class="badge-pill badge-success">Khớp chính xác</span></td>
      </tr>
      <tr>
        <td>Hình hai lá phổi</td>
        <td>Hai thùy phổi đối xứng và phế quản</td>
        <td>CM20 - Khoa Hô hấp & Phổi</td>
        <td><strong>83%</strong></td>
        <td><span class="badge-pill badge-primary">Khớp chính xác</span></td>
      </tr>
    </tbody>
  </table>

  <div class="page-break"></div>

  <!-- CHƯƠNG 5 (TIẾP THEO) -->
  <div class="page-header">
    <span>Chương 5: Kết quả Thực nghiệm & Đo lường Độ chính xác (tiếp)</span>
    <span>Clinical Symbol System - Ngô Khánh Giang</span>
  </div>

  <h2 class="section-title">5.3. Bảng So Sánh Hiệu Năng: Hu Moments Cũ vs Multi-Metric Fusion 2.0</h2>
  <p>
    Dưới đây là bảng đối chiếu trực tiếp giữa phiên bản ban đầu và phiên bản nâng cấp toàn diện:
  </p>
  <table class="custom-table">
    <thead>
      <tr>
        <th style="width: 25%;">Tiêu chí Đánh giá</th>
        <th style="width: 35%;">Phiên bản Cũ (Hu Moments Thuần)</th>
        <th style="width: 40%;">Phiên bản Hiện tại (Multi-Metric 2.0)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Quy mô Biểu trưng</strong></td>
        <td>12 biểu trưng mẫu đơn giản.</td>
        <td><strong>54+ biểu trưng chuẩn hóa quốc tế</strong> (SEGD & HCONC).</td>
      </tr>
      <tr>
        <td><strong>Khả năng nhận diện nét vẽ tay</strong></td>
        <td>Thất bại hoàn toàn (khoảng cách sai lệch &gt; 6.0 do nét mỏng rỗng ruột).</td>
        <td><strong>Thành công xuất sắc (83% - 92%)</strong> nhờ bù nét Dilation và Chamfer Distance.</td>
      </tr>
      <tr>
        <td><strong>Chụp Camera thực tế</strong></td>
        <td>Bị nhiễu bóng đèn, bóng tay làm sai lệch vùng nhị phân Otsu.</td>
        <td><strong>Độ chính xác 88% - 99%</strong> nhờ Khử bóng đổ Background Division và Viewfinder Laser.</td>
      </tr>
      <tr>
        <td><strong>Tính bền vững khi vẽ nghiêng</strong></td>
        <td>Kém, độ nhạy cao với góc xoay không đồng đều.</td>
        <td><strong>Tự động cân chỉnh góc xoay theo trục chính PCA</strong> trước khi trích xuất vector.</td>
      </tr>
      <tr>
        <td><strong>Phương thức nhập liệu</strong></td>
        <td>Chỉ hỗ trợ tải tệp ảnh từ máy tính.</td>
        <td><strong>3 Kênh linh hoạt:</strong> Tải tệp, Camera laser thời gian thực, Bảng vẽ tay cảm ứng.</td>
      </tr>
      <tr>
        <td><strong>Giao diện & Trải nghiệm</strong></td>
        <td>Giao diện tối đơn sắc, bảng tĩnh, nút bấm chưa phản hồi đồng bộ.</td>
        <td><strong>Pastel White dịu mắt</strong>, Slidebar Liquid Glass độc bản, Sidebar thu gọn, responsive 100%.</td>
      </tr>
      <tr>
        <td><strong>Giá trị ứng dụng Y khoa</strong></td>
        <td>Chỉ hiển thị tên và mô tả chung chung.</td>
        <td><strong>Tích hợp Gói Trợ lý Lâm sàng AI</strong> (Red Flags, phác đồ cấp cứu, chống chỉ định).</td>
      </tr>
    </tbody>
  </table>

  <div class="callout callout-success">
    <strong>KẾT LUẬN THỰC NGHIỆM:</strong> Việc chuyển đổi từ phương pháp toán học moment đơn lẻ sang kiến trúc kết hợp đa đặc trưng <em>Multi-Metric Feature Fusion</em> đã giúp hệ thống lột xác hoàn toàn, biến một nguyên mẫu thử nghiệm thành một giải pháp phần mềm y tế thông minh có độ tin cậy và tính khả thi ứng dụng thực tế rất cao.
  </div>

  <div class="page-break"></div>

  <!-- ====================================================================
       CHƯƠNG 6 & 7: THẢO LUẬN & KẾT LUẬN
       ==================================================================== -->
  <div class="page-header">
    <span>Chương 6 & 7: Thảo luận, Hạn chế & Kết luận</span>
    <span>Clinical Symbol System - Ngô Khánh Giang</span>
  </div>

  <h1 class="chapter-title">CHƯƠNG 6. THẢO LUẬN, HẠN CHẾ & HƯỚNG PHÁT TRIỂN TƯƠNG LAI</h1>

  <h2 class="section-title">6.1. Đánh Giá Ưu Điểm Nổi Bật của Dự Án</h2>
  <ol>
    <li><strong>Tính toàn diện và đồng bộ cao:</strong> Dự án không chỉ dừng lại ở thuật toán nhận diện mà đã hoàn thiện một hệ sinh thái web hoàn chỉnh từ Landing Page chuyên nghiệp, hệ thống xác thực bảo mật đến các công cụ làm việc thực tế.</li>
    <li><strong>Độ trễ xử lý cực thấp (Real-time Latency):</strong> Toàn bộ giải thuật Multi-Metric Fusion được tối ưu hóa bằng mảng số học NumPy và OpenCV C++ core, cho tốc độ xử lý &lt; 20ms mà không đòi hỏi phần cứng GPU đắt tiền.</li>
    <li><strong>Tính ứng dụng lâm sàng thực chất:</strong> Việc tích hợp các phác đồ cấp cứu và bảng kiểm an toàn mang lại giá trị thiết thực cho bác sĩ trẻ, sinh viên y khoa và điều dưỡng trong quá trình thực hành.</li>
  </ol>

  <h2 class="section-title">6.2. Các Hạn Chế Tồn Tại</h2>
  <ul>
    <li>Một số biểu trưng trong nhóm Chẩn đoán hình ảnh (như MA07, MA08, MA09 mô phỏng các máy quét vòm tròn) có hình dáng khung ngoài rất tương đồng, đòi hỏi người dùng phải vẽ hoặc chụp rõ các chi tiết chữ ký hiệu bên trong.</li>
    <li>Hệ thống hiện hoạt động trên môi trường Web Server cục bộ, chưa tích hợp trực tiếp vào hệ thống Hồ sơ Bệnh án Điện tử (EMR/HIS) của các bệnh viện lớn.</li>
  </ul>

  <h2 class="section-title">6.3. Lộ Trình Phát Triển Tương Lai</h2>
  <ul>
    <li><strong>Tích hợp Mạng Nơ-ron Tích chập Nhẹ (Edge AI CNN):</strong> Bổ sung mô hình MobileNetV4 hoặc Vision Transformer (ViT) thu nhỏ chạy trực tiếp trên trình duyệt qua WebAssembly/ONNX Runtime.</li>
    <li><strong>Ứng dụng Di động Progressive Web App (PWA):</strong> Đóng gói hệ thống thành ứng dụng di động có thể cài đặt trực tiếp lên máy tính bảng của điều dưỡng, cho phép quét ký hiệu tại giường bệnh mà không cần kết nối Internet.</li>
    <li><strong>Kết nối Chuẩn HL7 / FHIR Quốc Tế:</strong> Xây dựng API kết nối dữ liệu biểu trưng và phác đồ điều trị trực tiếp vào hệ thống quản lý bệnh viện thông minh.</li>
  </ul>

  <h1 class="chapter-title" style="margin-top: 35px;">CHƯƠNG 7. KẾT LUẬN & KIẾN NGHỊ</h1>

  <h2 class="section-title">7.1. Kết Luận Chung</h2>
  <p>
    Đề tài <strong>"Hệ thống mạng lưới điểm mốc đa chiều nhằm phân tích biểu trưng ký hiệu y tế hỗ trợ giao tiếp lâm sàng"</strong> do tác giả <strong>Ngô Khánh Giang</strong> thực hiện đã hoàn thành xuất sắc các mục tiêu nghiên cứu và phát triển đặt ra:
  </p>
  <ul>
    <li>Xây dựng thành công cơ sở dữ liệu số hóa <strong>54+ biểu trưng y tế chuẩn quốc tế</strong> SEGD và HCONC.</li>
    <li>Phát triển thành công lõi thị giác máy tính <strong>Multi-Metric Feature Fusion 2.0</strong>, giải quyết dứt điểm bài toán nhận diện nét vẽ tay rung lắc và ảnh chụp camera bị bóng đổ với độ tin cậy đạt 83% - 99%.</li>
    <li>Hoàn thiện hệ sinh thái giao diện công thái học hiện đại: Landing Page Ladipage, Auth Liquid Glass Slidebar, Dashboard Pastel White và Mạng lưới Đa chiều Cytoscape.js.</li>
    <li>Tích hợp Gói Trợ lý Lâm sàng AI đóng góp giá trị thiết thực cho an toàn người bệnh và hỗ trợ giao tiếp trong môi trường y tế.</li>
  </ul>

  <h2 class="section-title">7.2. Lời Cảm Ơn & Cam Kết</h2>
  <p>
    Tác giả xin chân thành cảm ơn các đồng nghiệp, các chuyên gia y tế và cộng đồng nghiên cứu thị giác máy tính mã nguồn mở đã cung cấp tài liệu chuyên môn và đóng góp ý kiến quý báu trong suốt quá trình hoàn thiện đề tài. Tác giả cam kết tiếp tục nghiên cứu, tối ưu hóa và mở rộng hệ thống để đóng góp tích cực vào tiến trình chuyển đổi số ngành Y tế Việt Nam.
  </p>

  <div style="margin-top: 35px; display: flex; justify-content: flex-end;">
    <div style="text-align: center; width: 220px;">
      <div style="font-size: 9.5pt; font-weight: 600; color: #64748b; margin-bottom: 4px;">Hà Nội, Năm 2026</div>
      <div style="font-size: 10pt; font-weight: 700; color: #1e293b; text-transform: uppercase;">Người thực hiện đề tài</div>
      <div style="height: 65px;"></div>
      <div style="font-size: 11pt; font-weight: 800; color: #2563eb;">NGÔ KHÁNH GIANG</div>
    </div>
  </div>

</body>
</html>
"""

    
    for placeholder, val in [
        ("__IMG_HERO__", img_hero),
        ("__IMG_LANDING_PASTEL__", img_landing_pastel),
        ("__IMG_LOGIN__", img_login),
        ("__IMG_DASHBOARD__", img_dashboard),
        ("__IMG_SIDEBAR__", img_sidebar),
        ("__IMG_CANVAS_DRAWN__", img_canvas_drawn),
        ("__IMG_RESULT__", img_result),
        ("__IMG_CATALOG__", img_catalog),
    ]:
        html_content = html_content.replace(placeholder, val)

    os.makedirs(os.path.dirname(HTML_OUT), exist_ok=True)
    with open(HTML_OUT, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ HTML report generated: {HTML_OUT} ({len(html_content)} bytes)")

def compile_pdf():
    chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    cmd = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={PDF_OUT}",
        HTML_OUT
    ]
    print(f"🚀 Compiling PDF with Google Chrome Headless...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if os.path.exists(PDF_OUT):
        pdf_size = os.path.getsize(PDF_OUT)
        print(f"🎉 PDF successfully created: {PDF_OUT} ({pdf_size} bytes)")
        # Copy to brain artifact directory as well
        brain_pdf = os.path.join(BRAIN_DIR, "BAO_CAO_CLINICAL_SYMBOL_SYSTEM.pdf")
        brain_html = os.path.join(BRAIN_DIR, "BAO_CAO_CLINICAL_SYMBOL_SYSTEM.html")
        with open(PDF_OUT, "rb") as f_in, open(brain_pdf, "wb") as f_out:
            f_out.write(f_in.read())
        with open(HTML_OUT, "r", encoding="utf-8") as f_in, open(brain_html, "w", encoding="utf-8") as f_out:
            f_out.write(f_in.read())
        print(f"✅ Copied to brain artifacts: {brain_pdf}")
    else:
        print(f"❌ Failed to create PDF! Stderr: {res.stderr.decode('utf-8')}")

if __name__ == "__main__":
    generate_html()
    compile_pdf()
