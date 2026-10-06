# Nguồn dữ liệu và giả định

## Mortality

- Nguồn: American Academy of Actuaries / Society of Actuaries, 2015 VBT.
- Trang: https://mort.soa.org/ViewTable.aspx?TableIdentity=3269
- Tên bảng: 2015 VBT Smoker Distinct Male Non-Smoker ALB.
- Phần sử dụng: **Ultimate**, tuổi đạt được (attained age) 30–49; **không dùng phần Select theo duration**.
- ALB: Age Last Birthday, tuổi theo sinh nhật gần nhất đã qua.
- Địa lý: Hoa Kỳ. Xác minh ngày 2026-10-05.
- Tệp trích: `data/mortality.csv`; tỷ lệ được lưu dạng thập phân, không phải số trên 1.000 người.
- Ví dụ: q₃₀ = 0,00046 = 0,046%.

Bảng công khai không đồng nghĩa với giả định kinh nghiệm của công ty hay Việt Nam. Dùng Ultimate ngay từ năm 1 là đơn giản hóa để học; không mô hình hóa hiệu ứng chọn lọc do underwriting. Quyền đối với nguồn bên thứ ba thuộc nhà cung cấp; project không áp dụng một giấy phép riêng cho dữ liệu SOA.

## Giả định minh họa

| Input | Giá trị | Bản chất |
| --- | ---: | --- |
| Tuổi tham gia / thời hạn | 30 / 20 năm | Thiết kế minh họa |
| Sum Assured | 100.000.000 VND | Thiết kế minh họa |
| Số hợp đồng ban đầu | 1 | Đơn vị chuẩn hóa |
| Lapse | 5% mỗi năm | Không ước lượng từ dữ liệu hợp đồng |
| Discount rate | 5% mỗi năm | Không suy ra từ yield curve |
| Acquisition expense | 150.000 VND | Tại đầu năm 1 |
| Maintenance expense | 30.000 VND | Trên hợp đồng còn hiệu lực đầu năm, chi cuối năm |
| Expense inflation | 3% | Tăng từ năm 2 |
| First / renewal commission | 30% / 5% phí | Chi đầu năm |
| Target margin | 10% | PV profit / PV premium |

Stress được định nghĩa trong `data/scenarios.json`. Lapse +25% là tăng tương đối từ 5% lên 6,25%; discount -1 điểm phần trăm là từ 5% xuống 4%. Kịch bản kết hợp gộp bốn thay đổi, không đại diện một mức confidence hoặc xác suất xảy ra đã được hiệu chỉnh.

## Dữ liệu đầu ra

`results/python_*.csv` là kết quả thuật toán Python. `results/excel_*.csv` được trích từ Microsoft Excel thực sự tính lại, không phải chép kết quả Python sang Excel. Hai cách triển khai dùng cùng đầu vào để kiểm tra tính nhất quán về tính toán.
