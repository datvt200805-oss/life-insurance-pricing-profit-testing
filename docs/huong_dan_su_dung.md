# Sử dụng mô hình có sẵn

## Excel

1. Mở `excel/mo_hinh_dinh_phi.xlsx`.
2. Xem `Tổng quan`: phí và margin cơ sở. Mức phí cố định đã được nhập bằng nghiệm cơ sở để stress có ý nghĩa.
3. Trong `Giả định`, thay B5 từ 1 đến 6. KPI chính tự tính lại.
4. B21 là phí cố định. Để trống để giải phí theo kịch bản đang chọn; nhập 0 nghĩa là không thu phí, margin n.a.
5. Muốn định phí lại sản phẩm: chọn cơ sở, sửa input, xóa B21, ghi mức phí giải mới từ Tổng quan!B6 rồi dán giá trị vào B21.
6. `Mô hình` hiển thị từng năm; AA và AB là sai lệch bảo toàn và nối đầu–cuối. `Công thức` có công thức mẫu.
7. Bảng sáu kịch bản và `Đối chiếu` là bản chụp cấu hình phát hành, không tự cập nhật khi sửa input. Xem kết quả mới bằng script tái chạy.

| Ô input | Đại lượng |
| --- | --- |
| B5 | Số kịch bản |
| B8:B11 | Tuổi, thời hạn, SA, số hợp đồng |
| B13:B15 | Target margin, lapse, discount rate |
| B16:B18 | Acquisition, maintenance, inflation |
| B19:B20 | First / renewal commission |
| B21 | Phí cố định; trống để solver tính lại |
| G15:J20 | Mức stress |
| B31:B50 | qₓ theo tuổi |

Tuổi cuối = tuổi tham gia + thời hạn − 1 phải ≤49 và tuổi đầu ≥30 với nguồn hiện tại. Không đổi giới tính/hút thuốc mà giữ nguyên bảng nguồn. Excel là mô hình một profile; chưa phải công cụ pricing mọi tuổi/sản phẩm.

## Python và cập nhật kết quả

1. Sửa `data/assumptions.json` và/hoặc `data/scenarios.json`.
2. Chạy tests rồi `python scripts/run_project.py`.
3. Chạy `python scripts/create_figures.py` nếu đã cài matplotlib.
4. Trên Windows có Excel, chạy `scripts/verify_excel.ps1` rồi `python scripts/reconcile.py`.
5. Cập nhật báo cáo và các nhận xét theo CSV mới trước khi công bố.

Input Excel và JSON là hai bản độc lập để tiện học. Thay Excel không tự sửa JSON. Script verify nạp JSON/CSV vào một bản workbook chỉ đọc để đảm bảo cùng input khi đối chiếu; không ghi đè file Excel người dùng đang chỉnh.

## Những việc nên tự làm để hiểu project

- Chạy mortality +20%, expense +15% và giảm discount 0,5 điểm phần trăm; trước khi chạy, dự đoán hướng thay đổi.
- So sánh margin và PV profit tuyệt đối khi lapse đổi; giải thích vì sao chúng có thể di chuyển khác nhau.
- Làm tròn phí và kiểm tra margin sau làm tròn.
- Chọn một năm, tính claim và PV claim bằng tay để đối chiếu.
- Viết 5–7 câu giải thích kết quả cho người không chuyên.

Bạn có thể dùng template sẵn. Giá trị học tập nằm ở việc hiểu giả định, kiểm tra và giải thích các lựa chọn.
