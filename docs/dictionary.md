# Từ điển dữ liệu đầu ra

Mỗi dòng annual là một kịch bản × một năm hợp đồng, trên danh mục ban đầu có kích thước initial_policies.

| Trường | Ý nghĩa | Đơn vị / thời điểm |
| --- | --- | --- |
| scenario_id, scenario_name | Mã/tên kịch bản | 1–6 |
| year, age | Năm hợp đồng, tuổi đầu năm | Số nguyên |
| qx_base, qx | Tử vong nguồn / sau stress | Xác suất năm |
| inforce_boy, inforce_eoy | Hiệu lực đầu/cuối năm | Hợp đồng kỳ vọng |
| deaths, lapses | Tử vong/hủy | Hợp đồng kỳ vọng |
| df_boy, df_eoy | Hệ số chiết khấu đầu/cuối năm | Không có đơn vị |
| pv_exposure | Nₜ × DF đầu năm | Hệ số phí |
| commission_rate | Hoa hồng | Tỷ lệ trên phí |
| pv_commission_factor | Nₜ × cₜ × DF đầu năm | Hệ số hoa hồng |
| claims | Quyền lợi tử vong | VND; cuối năm |
| acquisition_expense | Chi phí phát hành | VND; đầu năm 1 |
| maintenance_expense | Chi phí duy trì | VND; cuối năm |
| annual_premium | Phí năm trên một hợp đồng còn hiệu lực | VND/hợp đồng/năm |
| premium_cashflow | Nₜ × phí năm | VND; đầu năm |
| commission | Phí thu × tỷ lệ hoa hồng | VND; đầu năm |
| net_cashflow | Thu trừ chi gộp theo năm | VND; có nhiều timing |
| pv_claims, pv_acquisition, pv_maintenance | PV các outflow | VND tại t=0 |
| pv_premium, pv_commission | PV phí/hoa hồng | VND tại t=0 |
| pv_profit | Chênh lệch PV thu–chi | VND tại t=0 |
| required_premium | Phí cần theo target của từng kịch bản | VND/hợp đồng/năm |
| pv_expenses | PV acquisition + maintenance | VND tại t=0 |
| profit_margin | PV profit / PV premium | Tỷ lệ; n.a. nếu premium PV=0 |
| closing_inforce | Hiệu lực cuối thời hạn | Hợp đồng kỳ vọng |

Trong `reconciliation.csv`, key là scenario hoặc scenario/year. Difference = Excel − Python. Tolerance là ngưỡng tuyệt đối theo đại lượng; status là PASS/FAIL.
