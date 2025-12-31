import unittest
from src.finance.epv_model import GreenwaldEPV

class TestGreenwaldEPV(unittest.TestCase):
    def setUp(self):
        self.model = GreenwaldEPV()

    def test_calculate_normalized_earnings(self):
        income_stmt = {
            'ebit': 1000,
            'sga': 500,
            'rnd': 200,
            'tax_rate': 0.25
        }
        ai_adjustments = {
            'maintenance_sga_percent': 0.5,
            'maintenance_rnd_percent': 0.5
        }

        # Calculations:
        # Growth SGA = 500 * (1 - 0.5) = 250
        # Growth RND = 200 * (1 - 0.5) = 100
        # Total Growth Capex = 350
        # Normalized EBIT = 1000 + 350 = 1350
        # NOPAT = 1350 * (1 - 0.25) = 1012.5

        result = self.model.calculate_normalized_earnings(income_stmt, ai_adjustments)

        self.assertEqual(result['normalized_ebit'], 1350)
        self.assertEqual(result['nopat'], 1012.5)
        self.assertEqual(result['growth_sga'], 250)
        self.assertEqual(result['growth_rnd'], 100)
        self.assertEqual(result['reported_ebit'], 1000)

    def test_calculate_epv(self):
        normalized_earnings = 1000
        cost_of_capital = 0.10

        # EPV = 1000 / 0.10 = 10000
        epv = self.model.get_epv(normalized_earnings, cost_of_capital)
        self.assertEqual(epv, 10000)

        # Test divide by zero protection
        epv_zero = self.model.get_epv(normalized_earnings, 0)
        self.assertEqual(epv_zero, 0)

    def test_calculate_equity_value(self):
        firm_epv = 10000
        cash = 2000
        debt = 5000

        # Equity Value = 10000 + 2000 - 5000 = 7000
        equity_value = self.model.calculate_equity_value(firm_epv, cash, debt)
        self.assertEqual(equity_value, 7000)

    def test_calculate_reproduction_value(self):
        balance_sheet = {
            'cash': 1000,
            'accounts_receivable': 500,
            'pp_and_e': 2000,
            'other_assets': 100,
            'total_current_liabilities': 300,
            'rnd': 300,
            'book_value_equity': 2500
        }

        # Net Working Capital = (500 + 100) - 300 = 300
        # Capitalized RND = 300 * 3 = 900
        # Reproduction Value (Method 1) = 300 (NWC) + 2000 (PPE) + 900 (Cap RND) = 3200

        # Book Equity Floor Check
        # Book Equity - Cash = 2500 - 1000 = 1500

        # Max(3200, 1500) = 3200

        val = self.model.calculate_reproduction_value(balance_sheet)
        self.assertEqual(val, 3200)

    def test_calculate_reproduction_value_book_equity_floor(self):
        # Case where book equity is higher than calculated repro value
        balance_sheet = {
            'cash': 500,
            'accounts_receivable': 100,
            'pp_and_e': 100,
            'other_assets': 0,
            'total_current_liabilities': 100,
            'rnd': 0,
            'book_value_equity': 5000
        }

        # NWC = (100 + 0) - 100 = 0
        # Cap RND = 0
        # Method 1 = 0 + 100 + 0 = 100

        # Book Equity Floor = 5000 - 500 = 4500

        # Max(100, 4500) = 4500

        val = self.model.calculate_reproduction_value(balance_sheet)
        self.assertEqual(val, 4500)

    def test_calculate_rule_of_40(self):
        growth = 25
        margin = 20
        # 25 + 20 = 45
        score = self.model.calculate_rule_of_40(growth, margin)
        self.assertEqual(score, 45)

if __name__ == '__main__':
    unittest.main()
