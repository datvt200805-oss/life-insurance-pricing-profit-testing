# Cách trình bày project trong CV và phỏng vấn

## Bullet CV tham khảo

**Life Insurance Pricing & Profit Testing | Python, Excel**

- Ứng dụng mô hình dòng tiền kỳ vọng 20 năm cho bảo hiểm tử kỳ; giải mức phí đạt profit margin 10% và phân tích sáu kịch bản mortality, lapse, expense và discount rate.
- Kiểm tra 14 tình huống Python và đối chiếu 3.174 giá trị Python–Excel; trình bày tác động của stress và các giới hạn giả định trong báo cáo tiếng Việt.

Chỉ ghi các thao tác kiểm tra/tái chạy mà bạn đã thực sự thực hiện và có thể giải thích. Template và mã có hỗ trợ AI; xem CONTRIBUTIONS. Nếu chỉ sử dụng mô hình được cung cấp, dùng “ứng dụng/phân tích/kiểm tra”, không nhận đã tự viết toàn bộ.

## Giới thiệu trong 60–90 giây

“Project của em xét một nam 30 tuổi, bảo hiểm tử kỳ 20 năm. Em sử dụng qₓ công khai từ bảng SOA Ultimate và các giả định minh họa về lapse, chi phí và hoa hồng. Mô hình dự phóng số hợp đồng, dòng tiền thu–chi và chiết khấu theo đúng thời điểm. Phí được giải để đạt margin 10%, sau đó giữ cố định để chạy stress. Khi mortality tăng 10%, margin giảm còn khoảng 4,85%. Em kiểm tra kết quả Excel với triển khai Python và lưu bằng chứng đối chiếu. Em cũng ghi rõ đây là mô hình PV cash-flow đơn giản, chưa có reserve, capital hay tax.”

## Câu hỏi thường gặp

| Câu hỏi | Nội dung cần nói |
| --- | --- |
| Vì sao claim năm 1 là 46.000? | 1 × 0,00046 × 100 triệu; expected cost, claim thực trả 100 triệu khi đủ điều kiện |
| Vì sao lapse sau tử vong? | Quy ước rời rạc, chỉ sống mới hủy; chưa dùng mô hình competing decrements liên tục |
| Vì sao phí đầu năm có DF năm 1 bằng 1? | Thu tại thời điểm 0; claim cuối năm dùng 1/1,05 |
| Vì sao giữ phí khi stress? | Tránh tự repricing đưa margin về target và che tác động rủi ro |
| Vì sao lapse tăng có thể tăng margin? | Loại bớt năm có cash-flow âm; kiểm tra cả absolute PV profit |
| Solver dùng gì? | Nghiệm trực tiếp P=O/[(1−m)A−C], vì tuyến tính theo phí |
| Vì sao năm 1 âm mà cả sản phẩm dương? | Acquisition/commission cao lúc đầu; PV các năm sau bù lại |
| Profit này có phải profit kế toán? | Chưa; không reserve, vốn, thuế hay reinsurance |
| Tại sao dùng SOA Hoa Kỳ? | Nguồn công khai để minh họa; chưa phù hợp định phí thật tại Việt Nam |
| Hạn chế Ultimate từ năm 1? | Không xét selection do underwriting và policy duration |

## Ghi nhớ trước phỏng vấn

Nₜ → Dₜ/Lₜ → claim, premium, expense, commission → PV theo timing → margin → stress → kiểm tra.

Với mỗi công thức, hiểu ý nghĩa và thời điểm sử dụng. Có thể mở Excel/Python chỉ ra một dòng tính nếu được yêu cầu.
