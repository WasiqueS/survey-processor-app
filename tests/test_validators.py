import unittest
from utils.validators import validate_payload

class TestValidators(unittest.TestCase):
    def test_valid_payload(self):
        payload = {
            "user_id": "test_user",
            "survey_results": [{"question_number": i, "question_value": 4} for i in range(1, 11)]
        }
        errors = validate_payload(payload)
        self.assertEqual(errors, [])

    def test_invalid_user_id(self):
        payload = {
            "user_id": "usr",
            "survey_results": [{"question_number": i, "question_value": 4} for i in range(1, 11)]
        }
        errors = validate_payload(payload)
        self.assertIn("user_id must be at least 5 characters long.", errors)

if __name__ == '__main__':
    unittest.main()
