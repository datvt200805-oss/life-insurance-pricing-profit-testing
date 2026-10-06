"""Dự phóng giá trị kỳ vọng; không sử dụng thư viện Excel để tính kết quả."""
import csv
import math
from pathlib import Path

CORE_FIELDS = (
    "issue_age", "term", "sum_assured", "initial_policies", "target_margin",
    "lapse_rate", "discount_rate", "acquisition_expense", "maintenance_expense",
    "expense_inflation", "first_commission", "renewal_commission",
)
ANNUAL_FIELDS = (
    "year", "age", "qx_base", "qx", "inforce_boy", "deaths", "lapses",
    "inforce_eoy", "df_boy", "df_eoy", "pv_exposure", "commission_rate",
    "pv_commission_factor", "claims", "acquisition_expense", "maintenance_expense",
    "pv_claims", "pv_acquisition", "pv_maintenance", "annual_premium",
    "premium_cashflow", "commission", "net_cashflow", "pv_premium",
    "pv_commission", "pv_profit",
)

def load_mortality(path):
    """Kiểm tra tuổi duy nhất, tỷ lệ hữu hạn và nằm trong [0,1]."""
    result = {}
    with Path(path).open(encoding="utf-8-sig", newline="") as file:
        for row in csv.DictReader(file):
            age = int(row["age"])
            qx = float(row["qx"])
            if age in result:
                raise ValueError(f"Tuổi trùng trong bảng tử vong: {age}")
            if not math.isfinite(qx) or not 0 <= qx <= 1:
                raise ValueError(f"q_x không hợp lệ tại tuổi {age}")
            result[age] = qx
    if not result:
        raise ValueError("Bảng tử vong trống")
    return result

def validate(assumptions, mortality, scenario):
    for field in CORE_FIELDS:
        value = assumptions.get(field)
        if isinstance(value, bool) or not isinstance(value, (float, int)) or not math.isfinite(value):
            raise ValueError(f"Thiếu hoặc sai dữ liệu: {field}")
    for field in ("issue_age", "term"):
        if int(assumptions[field]) != assumptions[field]:
            raise ValueError(f"{field} phải là số nguyên")
    if not 1 <= assumptions["term"] <= 20:
        raise ValueError("Thời hạn hỗ trợ: 1–20 năm")
    for field in ("sum_assured", "initial_policies"):
        if assumptions[field] <= 0:
            raise ValueError(f"{field} phải dương")
    for field in ("acquisition_expense", "maintenance_expense"):
        if assumptions[field] < 0:
            raise ValueError(f"{field} không thể âm")
    for field in ("lapse_rate", "first_commission", "renewal_commission"):
        if not 0 <= assumptions[field] <= 1:
            raise ValueError(f"{field} phải trong [0,1]")
    if not 0 <= assumptions["target_margin"] < 1:
        raise ValueError("Target margin phải trong [0,1)")
    if assumptions["expense_inflation"] <= -1:
        raise ValueError("Lạm phát chi phí phải lớn hơn -100%")
    for field in ("mortality_multiplier", "lapse_multiplier", "expense_multiplier", "discount_shift"):
        value = scenario.get(field)
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError(f"Thiếu hoặc sai giả định kịch bản: {field}")
    for field in ("mortality_multiplier", "lapse_multiplier", "expense_multiplier"):
        if scenario[field] < 0:
            raise ValueError(f"{field} không thể âm")
    if not 0 <= assumptions["lapse_rate"] * scenario["lapse_multiplier"] <= 1:
        raise ValueError("Lapse sau stress vượt [0,1]")
    if assumptions["discount_rate"] + scenario["discount_shift"] <= -1:
        raise ValueError("Lãi suất chiết khấu phải lớn hơn -100%")
    for age in range(int(assumptions["issue_age"]), int(assumptions["issue_age"] + assumptions["term"])):
        if age not in mortality:
            raise ValueError(f"Thiếu q_x cho tuổi {age}")
        if not math.isfinite(mortality[age]) or not 0 <= mortality[age] <= 1 or not 0 <= mortality[age] * scenario["mortality_multiplier"] <= 1:
            raise ValueError(f"q_x sau stress không hợp lệ tại tuổi {age}")

def project(assumptions, mortality, scenario, fixed_premium=None):
    """Giải phí trực tiếp rồi dự phóng; phí cố định=0 được giữ đúng là 0."""
    validate(assumptions, mortality, scenario)
    if fixed_premium is not None and (isinstance(fixed_premium, bool) or not isinstance(fixed_premium, (int, float)) or
            not math.isfinite(fixed_premium) or fixed_premium < 0):
        raise ValueError("Phí cố định phải hữu hạn và không âm")
    a = assumptions
    lapse = a["lapse_rate"] * scenario["lapse_multiplier"]
    rate = a["discount_rate"] + scenario["discount_shift"]
    n = a["initial_policies"]
    rows = []
    for t in range(1, int(a["term"]) + 1):
        age = int(a["issue_age"]) + t - 1
        qx = mortality[age] * scenario["mortality_multiplier"]
        deaths = n * qx
        lapses = (n - deaths) * lapse
        df_boy, df_eoy = (1 + rate) ** (1 - t), (1 + rate) ** (-t)
        commission_rate = a["first_commission"] if t == 1 else a["renewal_commission"]
        claims = deaths * a["sum_assured"]
        acquisition = n * a["acquisition_expense"] * scenario["expense_multiplier"] if t == 1 else 0
        maintenance = n * a["maintenance_expense"] * (1 + a["expense_inflation"]) ** (t - 1) * scenario["expense_multiplier"]
        row = dict(zip(ANNUAL_FIELDS[:19], (
            t, age, mortality[age], qx, n, deaths, lapses, n - deaths - lapses,
            df_boy, df_eoy, n * df_boy, commission_rate, n * commission_rate * df_boy,
            claims, acquisition, maintenance, claims * df_eoy, acquisition * df_boy, maintenance * df_eoy,
        )))
        rows.append(row)
        n = row["inforce_eoy"]
    exposure = math.fsum(r["pv_exposure"] for r in rows)
    commission_factor = math.fsum(r["pv_commission_factor"] for r in rows)
    costs = math.fsum(r["pv_claims"] + r["pv_acquisition"] + r["pv_maintenance"] for r in rows)
    denominator = (1 - a["target_margin"]) * exposure - commission_factor
    if denominator <= 0:
        raise ValueError("Không có phí dương hữu hạn đạt target margin: mẫu số <= 0")
    required = costs / denominator
    premium = required if fixed_premium is None else fixed_premium
    for r in rows:
        premium_cf = r["inforce_boy"] * premium
        commission = premium_cf * r["commission_rate"]
        r.update(annual_premium=premium, premium_cashflow=premium_cf, commission=commission,
                 net_cashflow=premium_cf-r["claims"]-r["acquisition_expense"]-r["maintenance_expense"]-commission,
                 pv_premium=premium_cf*r["df_boy"], pv_commission=commission*r["df_boy"])
        r["pv_profit"] = r["pv_premium"]-r["pv_claims"]-r["pv_acquisition"]-r["pv_maintenance"]-r["pv_commission"]
    totals = {key: math.fsum(r[key] for r in rows) for key in ("pv_premium", "pv_claims", "pv_acquisition", "pv_maintenance", "pv_commission", "pv_profit")}
    totals["pv_expenses"] = totals["pv_acquisition"] + totals["pv_maintenance"]
    summary = {
        "scenario_id": scenario["id"], "scenario_name": scenario["name"],
        "required_premium": required, "annual_premium": premium, **totals,
        "profit_margin": totals["pv_profit"]/totals["pv_premium"] if totals["pv_premium"] > 0 else None,
        "closing_inforce": rows[-1]["inforce_eoy"],
    }
    return rows, summary
