"""Tái tạo CSV và báo cáo kết quả Python từ dữ liệu công khai/giả định minh họa."""
import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(ROOT))
from src.model import ANNUAL_FIELDS, load_mortality, project

def csv_write(path, rows, fields=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields or list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

def input_hash():
    digest = hashlib.sha256()
    for name in ("assumptions.json", "mortality.csv", "scenarios.json"):
        digest.update(name.encode())
        digest.update((ROOT/"data"/name).read_bytes())
    return digest.hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixed-premium", type=float, help="Giữ phí do người dùng chỉ định; mặc định giữ phí giải ở cơ sở")
    options = parser.parse_args()
    assumptions = json.loads((ROOT/"data/assumptions.json").read_text(encoding="utf-8"))
    scenarios = json.loads((ROOT/"data/scenarios.json").read_text(encoding="utf-8"))
    if [s["id"] for s in scenarios] != list(range(1, 7)):
        raise ValueError("Kịch bản phải có id 1–6 theo thứ tự; 1 là cơ sở")
    if any(scenarios[0][k] != v for k,v in {
        "mortality_multiplier": 1, "lapse_multiplier": 1, "expense_multiplier": 1, "discount_shift": 0}.items()):
        raise ValueError("Kịch bản 1 phải là cơ sở không stress")
    mortality = load_mortality(ROOT/"data/mortality.csv")
    _, base = project(assumptions, mortality, scenarios[0])
    fixed = base["required_premium"] if options.fixed_premium is None else options.fixed_premium
    annual, summaries = [], []
    for scenario in scenarios:
        rows, summary = project(assumptions, mortality, scenario, fixed)
        summaries.append(summary)
        annual.extend({"scenario_id": scenario["id"], **row} for row in rows)
    csv_write(ROOT/"results/python_scenarios.csv", summaries)
    csv_write(ROOT/"results/python_annual.csv", annual, ["scenario_id", *ANNUAL_FIELDS])
    (ROOT/"results/input_manifest.json").write_text(json.dumps({
        "input_sha256": input_hash(), "fixed_premium": fixed,
        "mode": "base_premium_fixed_for_all_scenarios", "currency": "VND"
    }, indent=2), encoding="utf-8")
    print(f"Phí cơ sở: {base['required_premium']:,.6f} VND/năm")
    for s in summaries:
        margin = "n.a." if s["profit_margin"] is None else f"{s['profit_margin']:.4%}"
        print(f"{s['scenario_id']}. {s['scenario_name']}: PV profit={s['pv_profit']:,.2f}; margin={margin}")

if __name__ == "__main__":
    main()
