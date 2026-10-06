# Kiểm tra mô hình và bằng chứng

## Kiểm thử Python

Chạy `python -m unittest discover -s tests -v`.

14 tests gồm: target margin, claim năm 1, bảo toàn từng năm, nối năm, PV identity, một năm tính tay, survival khi lapse=0, lapse=100%, discount=0, nhân số hợp đồng, phí 0 khác ô trống, margin không khả thi, thiếu qₓ, tuổi trùng, input sai và mortality stress.

Đây là kiểm thử hành vi và biên, không chỉ kiểm tra số công thức có trong file. Tests không thay thế actuarial review.

## Đối chiếu hai cách triển khai

Excel tính bằng công thức ô, Python tính theo thuật toán riêng; cùng dữ liệu để so sánh.

- Sáu kịch bản × 20 năm × 26 trường = 3.120 phép đối chiếu từng năm.
- Sáu kịch bản × 9 KPI = 54 phép đối chiếu tổng hợp.
- Tổng: **3.174**.
- Tiền: sai lệch tuyệt đối ≤0,01 VND.
- Xác suất, DF, margin và hệ số: ≤10⁻¹⁰.
- Tuổi và năm: phải khớp chính xác.

Bằng chứng phát hành:

- `results/excel_manifest.json`: phiên bản Excel, SHA-256 workbook và hash input.
- `results/input_manifest.json`: hash input, chế độ giữ phí.
- `results/excel_annual.csv`, `excel_scenarios.csv`: giá trị Excel sau full recalculation.
- `results/python_annual.csv`, `python_scenarios.csv`: kết quả Python.
- `results/reconciliation.csv`: từng phép đối chiếu, chênh lệch, ngưỡng và PASS/FAIL.
- `results/verification.json`: tổng số đạt/không đạt.

Tại cấu hình phát hành, tất cả 3.174 đối chiếu đạt. `reconcile.py` từ chối đối chiếu nếu input hash thay đổi, workbook thay đổi sau lần capture, thiếu/trùng khóa hoặc có sai lệch vượt ngưỡng.

## Kiểm soát trong Excel

Giả định hiển thị cảnh báo input thiếu/sai và thiếu tuổi nguồn; lookup phát hiện tuổi trùng hoặc qₓ trống. AA/AB trong Mô hình kiểm tra theo năm, không chỉ dùng tổng có thể triệt tiêu sai lệch. Tổng quan kiểm tra PV identity và phương trình giải phí.

Một số kiểm tra algebra đọc chính build giúp phát hiện lỗi kết nối nhưng chưa độc lập. Phép tính tay một năm, survival product và đối chiếu triển khai Python là kiểm tra bổ sung. Khớp hai engine chứng minh consistency, không chứng minh giả định là cơ sở định phí thực tế phù hợp.
