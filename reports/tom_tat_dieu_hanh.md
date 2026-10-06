# Tóm tắt định phí và khả năng sinh lời

Ngày phát hành: 2026-10-05. Đơn vị: VND trên một hợp đồng ban đầu; phí năm giữ nguyên ở các stress.

**Kết luận:** mức phí giải để đạt target margin 10% là **168.227 VND/năm** trước làm tròn thương mại. Tử vong là yếu tố gây giảm margin lớn nhất trong các stress đơn lẻ đã chọn. Kịch bản kết hợp còn margin dương **1,28%**, thấp đáng kể so với target.

## Phạm vi và giả định

Bảo hiểm tử kỳ 20 năm, nam 30 tuổi không hút thuốc, sum assured 100 triệu. qₓ lấy từ SOA 2015 VBT Ultimate; lapse 5%, discount 5%, acquisition 150.000, maintenance 30.000 tăng 3%/năm, commission 30% năm 1 và 5% tái tục. Phí/hoa hồng đầu năm, claim/duy trì cuối năm.

## Kết quả

| Kịch bản | Phí mới cần để đạt 10% | PV quyền lợi | PV chi phí | PV dòng tiền thuần | Margin giữ phí | Δ margin (điểm %) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Cơ sở | 168.227 | 784.666 | 465.320 | 152.005 | 10,00% | 0,00 |
| Tử vong +10% | 178.768 | 862.487 | 465.133 | 73.644 | 4,85% | −5,15 |
| Hủy +25% | 166.674 | 700.605 | 437.394 | 150.685 | 10,76% | +0,76 |
| Chi phí +10% | 174.489 | 784.666 | 511.851 | 105.473 | 6,94% | −3,06 |
| Discount −1 điểm % | 170.941 | 862.616 | 491.525 | 140.230 | 8,67% | −1,33 |
| Kết hợp | 186.088 | 843.390 | 505.915 | 18.947 | 1,28% | −8,72 |

Các mức tiền làm tròn đến đồng để trình bày; tính toán dùng độ chính xác đầy đủ. Phí dùng trong toàn bộ stress = 168.227,000069; “phí mới cần” chỉ là kết quả repricing tham khảo của mô hình.

## Diễn giải

Mortality +10% làm tăng PV claim khoảng 77.822 VND và giảm PV dòng tiền thuần khoảng 78.361 VND. Chi phí +10% làm PV chi phí tăng khoảng 46.532 VND. Trong discount stress, PV phí cũng tăng nhưng mức tăng outflow và commission lớn hơn, nên margin giảm.

Lapse +25% làm margin tăng nhưng PV dòng tiền thuần tuyệt đối **giảm** từ 152.005 xuống 150.685. Exposure phí nhỏ hơn và một phần cash-flow âm các năm xa bị loại bỏ. Do đó không diễn giải đây là bằng chứng “lapse cao tốt cho kinh doanh”.

Năm đầu có cash-flow âm do chi phí phát hành và hoa hồng; sau đó qₓ tăng làm các năm xa có thể âm. Đây là lý do phải xem toàn bộ PV và timing.

## Kiểm tra và đề xuất

14 tests Python và 3.174 đối chiếu với Microsoft Excel đạt. Bằng chứng chi tiết nằm trong `results/`.

Nếu mở rộng, ưu tiên hiệu chỉnh mortality/lapse theo kinh nghiệm phù hợp, rồi bổ sung reserve, capital, tax và reinsurance trước khi đánh giá shareholder profit. Kết quả hiện tại là mô hình học tập PV cash-flow; chưa phải pricing basis Việt Nam hoặc lợi nhuận kế toán đầy đủ.
