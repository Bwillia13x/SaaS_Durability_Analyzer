import unittest
from src.finance.epv_model import GreenwaldEPV

class TestGreenwaldEPV(unittest.TestCase):
    def setUp(self):
        self.model = GreenwaldEPV()
        self.financials = {
            'ticker': 'TEST',
            'revenue': 1000,
            'cogs': 300,
            'ebit': 100,
            'sga': 400,
            'rnd': 200,
            'tax_rate': 0.25,
            'shares_outstanding': 100,
            'cash': 50,
            'debt': 20,
            'accounts_receivable': 30,
            'pp_and_e': 40,
            'other_assets': 10,
            'total_current_liabilities': 20,
            'book_value_equity': 80
        }

    def test_calculate_normalized_earnings(self):
        # 50% maintenance for both
        ai_adjustments = {
            'maintenance_sga_percent': 0.5,
            'maintenance_rnd_percent': 0.5
        }

        # Growth Spend:
        # SGA: 400 * (1 - 0.5) = 200
        # RND: 200 * (1 - 0.5) = 100
        # Total Growth = 300
        # Normalized EBIT = 100 + 300 = 400
        # NOPAT = 400 * (1 - 0.25) = 300

        results = self.model.calculate_normalized_earnings(self.financials, ai_adjustments)

        self.assertEqual(results['normalized_ebit'], 400)
        self.assertEqual(results['nopat'], 300)
        self.assertEqual(results['growth_sga'], 200)
        self.assertEqual(results['growth_rnd'], 100)

    def test_get_epv(self):
        normalized_earnings = 300
        wacc = 0.10
        epv = self.model.get_epv(normalized_earnings, wacc)
        self.assertEqual(epv, 3000)

        # Test zero wacc
        self.assertEqual(self.model.get_epv(300, 0), 0)

    def test_calculate_equity_value(self):
        firm_epv = 3000
        cash = 50
        debt = 20
        # Equity = 3000 + 50 - 20 = 3030
        self.assertEqual(self.model.calculate_equity_value(firm_epv, cash, debt), 3030)

    def test_calculate_rule_of_40(self):
        growth = 20
        margin = 30
        self.assertEqual(self.model.calculate_rule_of_40(growth, margin), 50)

    def test_calculate_reproduction_value(self):
        # Net working capital = (AR 30 + Other 10) - CL 20 = 20
        # Capitalized RND = 200 * 3 = 600
        # PPE = 40
        # Repro Value = 20 + 40 + 600 = 660

        # Book Equity - Cash = 80 - 50 = 30
        # Max(660, 30) = 660

        val = self.model.calculate_reproduction_value(self.financials)
        self.assertEqual(val, 660)

    def test_reproduction_value_book_equity_fallback(self):
        # Case where book equity is higher
        fin = self.financials.copy()
        fin['rnd'] = 0 # No RND
        fin['accounts_receivable'] = 0
        fin['other_assets'] = 0
        fin['total_current_liabilities'] = 0
        fin['pp_and_e'] = 0

        # Calculated Repro = 0
        # Book Equity = 80
        # Cash = 50
        # Floor = 80 - 50 = 30

        val = self.model.calculate_reproduction_value(fin)
        self.assertEqual(val, 30)

if __name__ == '__main__':
    unittest.main()
