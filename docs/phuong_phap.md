# Phương pháp và công thức

## 1. Quy ước

Ký hiệu Nₜ là số hợp đồng kỳ vọng đầu năm t; x là tuổi tham gia; n là thời hạn; P là phí năm cố định; SA là sum assured; qₜ = qₓ₊ₜ₋₁; lₜ là lapse; i là discount rate.

N₁ = số hợp đồng ban đầu. Phí được thu tại thời điểm t−1 nếu hợp đồng còn hiệu lực đầu năm. Hoa hồng và chi phí phát hành cũng chi tại đầu năm. Quyền lợi tử vong và chi phí duy trì chi tại thời điểm t.

Tử vong được xử lý trước lapse. Lapse chỉ áp dụng cho hợp đồng còn sống sau tử vong; đây là quy ước rời rạc của mô hình, không phải khẳng định mọi công ty dùng cùng cách. Không có tiền hoàn lại và không hoàn một phần phí năm khi tử vong/hủy.

## 2. Dự phóng hợp đồng

| Đại lượng | Công thức | Dùng để |
| --- | --- | --- |
| Xác suất sống | pₓ = 1 − qₓ | Tính survival khi chưa xét lapse |
| Tử vong kỳ vọng | Dₜ = Nₜ × qₜ | Tính claim |
| Hủy kỳ vọng | Lₜ = (Nₜ − Dₜ) × lₜ | Tính số rời hợp đồng |
| Hiệu lực cuối năm | Eₜ = Nₜ − Dₜ − Lₜ | Kiểm tra bảo toàn hợp đồng |
| Hiệu lực năm sau | Nₜ₊₁ = Eₜ | Roll-forward |

Tương đương Eₜ = Nₜ(1−qₜ)(1−lₜ). Với một hợp đồng, kết quả có thể là số thập phân vì là giá trị kỳ vọng. E₂₀≈0,350242 là tỷ lệ còn hiệu lực ngay trước kết thúc hợp đồng, không phải xác suất sống 20 năm thuần; sau đáo hạn không có coverage tiếp.

## 3. Dòng tiền theo năm

Premiumₜ = NₜP.

Claimₜ = DₜSA.

Commissionₜ = NₜP cₜ, trong đó c₁=30%, cₜ=5% từ năm 2.

Acquisition₁ = N₁a; Acquisitionₜ=0 từ năm 2. a là chi phí phát hành trên hợp đồng.

Maintenanceₜ = Nₜe(1+g)^(t−1), e là chi phí duy trì ban đầu, g là inflation. Việc dùng Nₜ dù chi ở cuối năm là quy ước chi phí theo exposure đầu năm, được áp dụng nhất quán ở Excel và Python.

NetCFₜ = Premiumₜ − Claimₜ − Acquisitionₜ − Maintenanceₜ − Commissionₜ.

NetCFₜ chỉ gộp số tiền theo năm để xem thu–chi; không được chiết khấu toàn bộ bằng một DF vì các thành phần có thời điểm khác nhau.

## 4. Discounting

v = 1/(1+i); DF đầu năm = v^(t−1); DF cuối năm = v^t.

PVProfitₜ = (Premiumₜ−Commissionₜ−Acquisitionₜ) v^(t−1) − (Claimₜ+Maintenanceₜ) v^t.

PVProfit = tổng PVProfitₜ. PVPremium = tổng NₜP v^(t−1). Margin = PVProfit/PVPremium. Khi phí bằng 0, margin không xác định, hiển thị n.a.; không tự thay 0 bằng phí solver.

## 5. Giải phí đạt target margin

Đặt A = Σ Nₜv^(t−1), C = Σ Nₜcₜv^(t−1), O = PVClaim + PVAcquisition + PVMaintenance.

Khi đó PVPremium = PA, PVCommission = PC và PVProfit = PA−PC−O.

Với margin mục tiêu m:

PA−PC−O = mPA

P[(1−m)A−C] = O

**P = O / [(1−m)A−C].**

Mẫu số phải dương để có mức phí dương hữu hạn với outflow dương. Đây là nghiệm trực tiếp vì chi phí và claim không phụ thuộc P, hoa hồng tỷ lệ tuyến tính theo P. Nếu phí có bậc, giới hạn, thuế hoặc lựa chọn phụ thuộc phí thì có thể cần solver số.

Phí phát hành chưa làm tròn thương mại. Nếu làm tròn P, kiểm tra margin đạt được có thể khác target. Phí cần thiết mới trong từng stress dùng để xem yêu cầu repricing; profit margin stress phải dùng mức phí cơ sở cố định để quan sát rủi ro.

## 6. Stress

qₜ stress = qₜ × mortality multiplier.

lapse stress = lapse cơ sở × lapse multiplier.

Acquisition và Maintenance cùng nhân expense multiplier.

i stress = i cơ sở + discount shift.

Chạy một yếu tố để xác định hướng tác động. Kịch bản kết hợp không bằng tổng số học của các tác động riêng vì tử vong/lapse làm thay đổi exposure và tất cả dòng tiền tiếp theo.

## 7. Đọc kết quả đúng phạm vi

Lapse tăng có thể làm margin tăng nếu những năm xa có dòng tiền âm và giảm claim nhiều hơn lợi ích phí bị mất; vẫn cần xét PV profit tuyệt đối và chi phí thu hút khách hàng chưa thu hồi.

Năm 1 có dòng tiền âm do acquisition và hoa hồng lớn; các năm sau có thể âm vì qₓ tăng. PV toàn thời hạn dương không có nghĩa mọi năm đều có profit dương.

Lợi nhuận này là **PV economic cash-flow đơn giản**, không phải statutory profit, distributable earnings hay IFRS 17 insurance service result. Chưa có reserve release, vốn, tax, reinsurance, underwriting selection, mortality improvement hay đường cong chiết khấu theo kỳ hạn.
