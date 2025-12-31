import unittest
from unittest.mock import MagicMock, patch
import json
from src.ai.parser import analyze_growth_spend
from src.ai.prompts import EPV_ANALYSIS_SYSTEM_PROMPT

class TestAIParser(unittest.TestCase):
    def setUp(self):
        self.financials = {
            'revenue': 1000
        }
        self.mda_text = "We invested heavily in growth."

    @patch('src.ai.parser.get_llm_response')
    def test_analyze_growth_spend_success(self, mock_get_llm_response):
        # Mock successful JSON response
        mock_response = json.dumps({
            "maintenance_sga_percent": 0.15,
            "maintenance_rnd_percent": 0.25,
            "reasoning": "Growth focus."
        })
        mock_get_llm_response.return_value = mock_response

        result = analyze_growth_spend(self.mda_text, self.financials)

        self.assertEqual(result['maintenance_sga_percent'], 0.15)
        self.assertEqual(result['maintenance_rnd_percent'], 0.25)
        self.assertEqual(result['reasoning'], "Growth focus.")

    @patch('src.ai.parser.get_llm_response')
    def test_analyze_growth_spend_json_cleanup(self, mock_get_llm_response):
        # Mock response with markdown code blocks
        mock_response = """
        ```json
        {
            "maintenance_sga_percent": 0.1,
            "maintenance_rnd_percent": 0.2,
            "reasoning": "Cleaned up."
        }
        ```
        """
        mock_get_llm_response.return_value = mock_response

        result = analyze_growth_spend(self.mda_text, self.financials)
        self.assertEqual(result['maintenance_sga_percent'], 0.1)

    @patch('src.ai.parser.get_llm_response')
    def test_analyze_growth_spend_fallback(self, mock_get_llm_response):
        # Mock exceptions to trigger retry and finally fallback
        mock_get_llm_response.side_effect = Exception("API Error")

        result = analyze_growth_spend(self.mda_text, self.financials)

        # Check defaults
        self.assertEqual(result['maintenance_sga_percent'], 0.20)
        self.assertEqual(result['maintenance_rnd_percent'], 0.20)
        self.assertIn("AI Unavailable", result['reasoning'])

    @patch('src.ai.parser.get_llm_response')
    def test_analyze_growth_spend_bad_json(self, mock_get_llm_response):
        # Mock bad JSON
        mock_get_llm_response.return_value = "{ bad json "

        result = analyze_growth_spend(self.mda_text, self.financials)

        # Should fallback to defaults
        self.assertIn("AI Unavailable", result['reasoning'])

if __name__ == '__main__':
    unittest.main()
