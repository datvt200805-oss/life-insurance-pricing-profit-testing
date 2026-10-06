import csv
import json
import math
import tempfile
import unittest
from pathlib import Path
from src.model import load_mortality, project
ROOT = Path(__file__).resolve().parents[1]

class ModelTests(unittest.TestCase):
    def setUp(self):
        self.a = json.loads((ROOT/"data/assumptions.json").read_text(encoding="utf-8"))
        self.s = json.loads((ROOT/"data/scenarios.json").read_text(encoding="utf-8"))[0]
        self.q = load_mortality(ROOT/"data/mortality.csv")
    def run_model(self, **changes):
        return project({**self.a, **changes}, self.q, self.s)
    def test_base_target_and_first_year(self):
        rows,s = self.run_model()
        self.assertAlmostEqual(s["profit_margin"], .10, places=12)
        self.assertAlmostEqual(rows[0]["inforce_eoy"], .949563, places=12)
        self.assertEqual(rows[0]["claims"], 46000)
        _, decimal_integers = self.run_model(issue_age=30.0, term=20.0)
        self.assertEqual(s["required_premium"], decimal_integers["required_premium"])
    def test_every_year_conservation_and_pv_identity(self):
        rows,s = self.run_model()
        for i,r in enumerate(rows):
            self.assertAlmostEqual(r["inforce_boy"]-r["deaths"]-r["lapses"],r["inforce_eoy"],places=12)
            if i:
                self.assertEqual(r["inforce_boy"],rows[i-1]["inforce_eoy"])
        self.assertAlmostEqual(s["pv_profit"],s["pv_premium"]-s["pv_claims"]-s["pv_expenses"]-s["pv_commission"],places=8)
    def test_one_year_hand_calculation(self):
        _,s = self.run_model(term=1)
        # Quyền lợi 46k, chi phí cuối năm 30k, chi phí đầu năm 150k.
        expected = (46000/1.05+30000/1.05+150000)/(.9-.3)
        self.assertAlmostEqual(s["required_premium"], expected, places=8)
    def test_no_lapse_survival_product(self):
        rows,_ = self.run_model(lapse_rate=0)
        self.assertAlmostEqual(rows[-1]["inforce_eoy"], math.prod(1-v for v in self.q.values()),places=12)
    def test_full_lapse_after_first_year(self):
        rows,_ = self.run_model(lapse_rate=1)
        self.assertEqual(rows[0]["inforce_eoy"],0)
        self.assertTrue(all(r["premium_cashflow"] == 0 for r in rows[1:]))
    def test_zero_discount(self):
        rows,_ = self.run_model(discount_rate=0)
        self.assertTrue(all(r["df_boy"] == r["df_eoy"] == 1 for r in rows))
    def test_scale_number_of_policies(self):
        _,one = self.run_model()
        _,many = self.run_model(initial_policies=10000)
        self.assertAlmostEqual(one["required_premium"],many["required_premium"],places=8)
        self.assertAlmostEqual(one["pv_profit"]*10000,many["pv_profit"],places=5)
    def test_fixed_zero_is_not_blank(self):
        rows,s = project(self.a,self.q,self.s,0)
        self.assertEqual(s["pv_premium"],0)
        self.assertIsNone(s["profit_margin"])
        self.assertTrue(all(r["annual_premium"] == 0 for r in rows))
    def test_infeasible_margin(self):
        with self.assertRaises(ValueError):
            self.run_model(target_margin=.99)
    def test_missing_qx(self):
        with self.assertRaises(ValueError):
            project(self.a,{30:self.q[30]},self.s)
    def test_invalid_inputs(self):
        for change in ({"term":0},{"term":1.5},{"lapse_rate":1.01},{"discount_rate":-1},
                       {"maintenance_expense":-1},{"sum_assured":None},{"sum_assured":float("nan")}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.run_model(**change)
    def test_qx_above_one_after_stress(self):
        with self.assertRaises(ValueError):
            project(self.a,self.q,{**self.s,"mortality_multiplier":10000})
        with self.assertRaises(ValueError):
            project(self.a,{**self.q,30:2},{**self.s,"mortality_multiplier":0})
    def test_duplicate_source_age(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/"duplicate.csv"
            p.write_text("age,qx\n30,0.01\n30,0.02\n")
            with self.assertRaises(ValueError):
                load_mortality(p)
    def test_stress_fixed_premium(self):
        _,base=self.run_model()
        _,stress=project(self.a,self.q,{**self.s,"mortality_multiplier":1.1},base["required_premium"])
        self.assertGreater(stress["pv_claims"],base["pv_claims"])
        self.assertLess(stress["profit_margin"],base["profit_margin"])

if __name__ == "__main__":
    unittest.main()
