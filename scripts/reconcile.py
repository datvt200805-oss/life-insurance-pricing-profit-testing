"""Đối chiếu kết quả tính lại bởi Microsoft Excel với Python theo năm/kịch bản."""
import csv
import hashlib
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.run_project import csv_write, input_hash
from src.model import ANNUAL_FIELDS

def read(name, keys):
    with (ROOT/"results"/name).open(encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))
    result = {}
    for row in rows:
        key = tuple(int(float(row[k])) for k in keys)
        if key in result:
            raise ValueError(f"Khóa trùng: {name}, {key}")
        result[key] = row
    return result

def main():
    current = input_hash()
    for name in ("input_manifest.json", "excel_manifest.json"):
        manifest = json.loads((ROOT/"results"/name).read_text(encoding="utf-8-sig"))
        if manifest["input_sha256"] != current:
            raise ValueError(f"{name}: kết quả cũ, hãy chạy lại từ dữ liệu hiện tại")
    workbook_hash = hashlib.sha256((ROOT/"excel/mo_hinh_dinh_phi.xlsx").read_bytes()).hexdigest()
    if manifest["workbook_sha256"] != workbook_hash:
        raise ValueError("Workbook đã đổi sau lần đối chiếu; chạy lại verify_excel.ps1")
    checks = []
    for suffix, keys, fields in (
        ("scenarios", ("scenario_id",), (
            "required_premium", "annual_premium", "pv_premium", "pv_claims",
            "pv_expenses", "pv_commission", "pv_profit", "profit_margin", "closing_inforce")),
        ("annual", ("scenario_id", "year"), ANNUAL_FIELDS),
    ):
        py, excel = read(f"python_{suffix}.csv", keys), read(f"excel_{suffix}.csv", keys)
        if set(py) != set(excel):
            raise ValueError(f"Khóa không khớp: {suffix}")
        for key in sorted(py):
            for field in fields:
                p, e = float(py[key][field]), float(excel[key][field])
                tolerance = 1e-10 if field in {
                    "profit_margin","closing_inforce","qx_base","qx","inforce_boy","inforce_eoy",
                    "deaths","lapses","df_boy","df_eoy","pv_exposure","commission_rate","pv_commission_factor"} else 0.01
                if field in ("year", "age"):
                    tolerance = 0
                delta = e - p
                checks.append({
                    "scope": suffix, "key": "/".join(map(str,key)), "metric": field,
                    "python": p, "excel": e, "difference": delta, "tolerance": tolerance,
                    "status": "PASS" if abs(delta) <= tolerance else "FAIL",
                })
    csv_write(ROOT/"results/reconciliation.csv", checks)
    failed = [row for row in checks if row["status"] == "FAIL"]
    status = {"checks": len(checks), "passed": len(checks)-len(failed), "failed": len(failed),
              "input_sha256": current, "max_absolute_difference": max(abs(r["difference"]) for r in checks)}
    (ROOT/"results/verification.json").write_text(json.dumps(status,indent=2),encoding="utf-8")
    print(json.dumps(status,indent=2))
    if failed:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
