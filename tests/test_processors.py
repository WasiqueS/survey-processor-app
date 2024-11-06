import unittest
from utils.processors import process_survey_results

class TestProcessors(unittest.TestCase):
    def test_process_survey_results(self):
        payload = {
            "user_id": "test_user",
            "survey_results": [{"question_number": i, "question_value": i % 7 + 1} for i in range(1, 11)]
        }
        result = process_survey_results(payload)
        self.assertIn("overall_analysis", result)
        self.assertIn("cat_dog", result)
        self.assertIn("fur_value", result)
        self.assertIn("tail_value", result)
        self.assertIn("description", result)
        self.assertIn("statistics", result)

if __name__ == '__main__':
    unittest.main()
