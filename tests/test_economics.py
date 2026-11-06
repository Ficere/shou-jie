import sys
import unittest
from decimal import Decimal as D
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from economics import antidilution, liquidation, number, redemption


class ArithmeticTests(unittest.TestCase):
    def test_simple_redemption(self):
        result = redemption(10000000, "0.08", 730, 500000)
        self.assertEqual(result["simple_interest"], D("1600000"))
        self.assertEqual(result["contract_claim_before_caps"], D("11100000"))

    def test_deduction_floor(self):
        self.assertEqual(redemption(100, 0, 0, 200)["contract_claim_before_caps"], 0)

    def test_explicit_fees(self):
        self.assertEqual(redemption(100, 0, 0, fees=5, penalty=2)
                         ["contract_claim_before_caps"], 107)

    def test_nonparticipating_low_exit(self):
        result = liquidation(100, "0.2", 150)
        self.assertEqual(result["investor_distribution"], 100)
        self.assertEqual(result["other_shareholders_total"], 50)

    def test_nonparticipating_conversion(self):
        self.assertEqual(liquidation(100, "0.2", 1000)["investor_distribution"], 200)

    def test_participating(self):
        result = liquidation(100, "0.2", 150, participating=True)
        self.assertEqual(result["investor_distribution"], 110)
        self.assertEqual(result["other_shareholders_total"], 40)

    def test_insufficient_proceeds_and_zero(self):
        self.assertEqual(liquidation(100, "0.2", 50)["investor_distribution"], 50)
        self.assertEqual(liquidation(100, "0.2", 0)["investor_distribution"], 0)

    def test_weighted_average(self):
        result = antidilution(10, 1000, 1000, 5)
        self.assertEqual(result["c_actual_new_shares"], 200)
        self.assertEqual(result["full_ratchet_price"], 5)
        self.assertAlmostEqual(float(result["weighted_average_price"]), 9.1666666667)

    def test_up_round_not_adjusted(self):
        self.assertEqual(antidilution(10, 1000, 1000, 20)["weighted_average_price"], 10)

    def test_bad_numbers(self):
        for value in ("NaN", "Infinity", "abc"):
            with self.assertRaises(ValueError):
                number(value)

    def test_negative_and_invalid_share(self):
        with self.assertRaises(ValueError):
            redemption(-1, 0, 0)
        for share in ("0", "1.1", "-0.1"):
            with self.assertRaises(ValueError):
                liquidation(100, share, 100)
        with self.assertRaises(ValueError):
            antidilution(10, 0, 100, 5)


if __name__ == "__main__":
    unittest.main()
