import unittest
from unittest.mock import MagicMock

from summarizer_agent import call_ai, INSTRUCTIONS

class TestCallAI(unittest.TestCase):
    
    def test_call_ai_success(self):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.output_text = "- Summary one\n- Summary two"
        mock_client.responses.create.return_value = mock_response
        user_input = "This is a sample text to be summarized."
        model_name = "test-openrouter-model"
        
        result = call_ai(mock_client, user_input, model_name)
        self.assertIn("summarized", result)
        self.assertEqual(result["summarized"], "- Summary one\n- Summary two")
        mock_client.responses.create.assert_called_once_with(
            model=model_name,
            instructions=INSTRUCTIONS,
            input=user_input
        )

    def test_call_ai_failure(self):
        mock_client = MagicMock()
        mock_client.responses.create.side_effect = Exception("Connection timeout error")
        user_input = "This is a sample text."
        model_name = "test-openrouter-model"
        
        result = call_ai(mock_client, user_input, model_name)
        self.assertIn("error", result)
        self.assertIn("An error occurred: Connection timeout error", result["error"])

if __name__ == "__main__":
    unittest.main()