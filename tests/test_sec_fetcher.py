import unittest
from unittest.mock import MagicMock, patch
import json
from src.data.sec_fetcher import SECFetcher

class TestSECFetcher(unittest.TestCase):
    def setUp(self):
        self.fetcher = SECFetcher()
        self.fetcher._session = MagicMock()

    @patch('src.data.sec_fetcher.os.getenv')
    def test_get_financials_mock_fallback(self, mock_getenv):
        # Mock API keys to be None/Empty
        mock_getenv.return_value = None

        # Mock yfinance Ticker to fail or be empty
        with patch('src.data.sec_fetcher.yf.Ticker') as mock_ticker_cls:
            mock_ticker = MagicMock()
            # Force empty/None data to trigger fallback
            mock_ticker.income_stmt = None
            mock_ticker.financials = None
            mock_ticker.balance_sheet = None
            mock_ticker.info = {}
            mock_ticker_cls.return_value = mock_ticker

            data = self.fetcher.get_financials("FAIL")
            self.assertTrue(data['is_mock'])
            self.assertEqual(data['source'], 'mock')

    @patch('src.data.sec_fetcher.os.getenv')
    def test_get_financials_fmp_success(self, mock_getenv):
        # Mock API key presence
        mock_getenv.return_value = "fake_key"

        # Mock FMP responses
        # Income Statement
        income_resp = MagicMock()
        income_resp.json.return_value = [
            {
                "revenue": 1000,
                "operatingIncome": 200,
                "sellingGeneralAndAdministrativeExpenses": 100,
                "researchAndDevelopmentExpenses": 50,
                "incomeTaxExpense": 20,
                "incomeBeforeTax": 100,
                "weightedAverageShsOutDil": 50
            },
            {
                "revenue": 800 # Previous
            }
        ]

        # Balance Sheet
        bal_resp = MagicMock()
        bal_resp.json.return_value = [{
            "cashAndCashEquivalents": 100,
            "totalDebt": 50,
            "netReceivables": 30,
            "propertyPlantEquipmentNet": 20,
            "otherCurrentAssets": 10,
            "totalCurrentLiabilities": 40,
            "totalStockholdersEquity": 200
        }]

        self.fetcher._session.get.side_effect = [income_resp, bal_resp]

        data = self.fetcher.get_financials("TEST")

        self.assertFalse(data['is_mock'])
        self.assertEqual(data['source'], 'fmp')
        self.assertEqual(data['revenue'], 1000)
        self.assertEqual(data['ebit'], 200)

    def test_extract_mda_section(self):
        # Create a mock HTML with Item 7
        html = """
        <html>
        <body>
        <p>Some random text</p>
        <p><b>Item 7. Management's Discussion and Analysis</b></p>
        <p>This is the MD&A content. We grew a lot.</p>
        <p><b>Item 8. Financial Statements</b></p>
        </body>
        </html>
        """

        extracted = self.fetcher._extract_mda_section(html)
        self.assertIsNotNone(extracted)
        self.assertIn("This is the MD&A content", extracted)

    def test_extract_mda_section_no_match(self):
        html = "<html><body>Nothing here</body></html>"
        extracted = self.fetcher._extract_mda_section(html)
        self.assertIsNone(extracted)

if __name__ == '__main__':
    unittest.main()
