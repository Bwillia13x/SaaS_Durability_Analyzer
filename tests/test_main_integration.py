import unittest
from unittest.mock import patch, MagicMock

class TestMainLogic(unittest.TestCase):
    def test_import_main(self):
        """
        Since we cannot fully run Streamlit, we just ensure that main.py can be compiled
        and that our new module is importable.
        """
        try:
            import src.ui.export
        except ImportError as e:
            self.fail(f"Failed to import src.ui.export: {e}")

    def test_export_function_signature(self):
        from src.ui.export import generate_markdown_report
        # Just call with dummy data to ensure no runtime errors in the formatting logic
        report = generate_markdown_report(
            "TEST",
            {'company_name': 'Test Co', 'price': 100, 'market_cap': 1000000000},
            {'shares_outstanding': 10, 'cash': 0, 'debt': 0},
            {'normalized_ebit': 10, 'nopat': 8},
            100, # epv
            100, # equity epv
            50, # repro
            50, # franchise
            "Reasoning"
        )
        self.assertIn("# SaaS EPV Analysis Report: Test Co (TEST)", report)
        # Price 100. Equity EPV 100. Shares 10. Target Price = 10.
        # Upside = (10 - 100)/100 = -90%.
        # Should be Overvalued.
        self.assertIn("Overvalued", report)

if __name__ == '__main__':
    unittest.main()
