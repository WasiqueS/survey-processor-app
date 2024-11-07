import unittest
from unittest.mock import patch, AsyncMock
from app import app

class TestApp(unittest.IsolatedAsyncioTestCase):

    @patch('utils.processors.process_survey_results')
    @patch('models.database.collection.insert_one', new_callable=AsyncMock)
    async def test_process_survey_valid_payload(self, mock_insert, mock_process):
        # Mock the processing function
        mock_process.return_value = {
            "overall_analysis": "certain",
            "cat_dog": "dogs",
            "fur_value": "long",
            "tail_value": "short",
            "description": "Generated description.",
            "statistics": {
                "mean": 5.0,
                "median": 5.0,
                "std_dev": 1.0
            }
        }

        payload = {
            "user_id": "test_user",
            "survey_results": [
                {"question_number": i, "question_value": 5} for i in range(1, 11)
            ]
        }

        async with app.asgi_client as client:
            response = await client.post("/process-survey", json=payload)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(await response.json(), mock_process.return_value)
        mock_process.assert_called_once_with(payload)
        mock_insert.assert_called_once()

    async def test_process_survey_invalid_payload_missing_user_id(self):
        payload = {
            "survey_results": [
                {"question_number": i, "question_value": 5} for i in range(1, 11)
            ]
        }

        async with app.asgi_client as client:
            response = await client.post("/process-survey", json=payload)

        self.assertEqual(response.status_code, 400)
        response_json = await response.json()
        self.assertIn("errors", response_json)
        self.assertIn("user_id is missing.", response_json["errors"])

    async def test_process_survey_invalid_payload_duplicate_question_number(self):
        payload = {
            "user_id": "test_user",
            "survey_results": [
                {"question_number": 1, "question_value": 5},
                {"question_number": 1, "question_value": 5},  # Duplicate
                *[
                    {"question_number": i, "question_value": 5}
                    for i in range(3, 11)
                ]
            ]
        }

        async with app.asgi_client as client:
            response = await client.post("/process-survey", json=payload)

        self.assertEqual(response.status_code, 400)
        response_json = await response.json()
        self.assertIn("errors", response_json)
        self.assertIn("Duplicate question_number 1.", response_json["errors"])

    async def test_process_survey_invalid_payload_incorrect_question_value(self):
        payload = {
            "user_id": "test_user",
            "survey_results": [
                {"question_number": 1, "question_value": 8},  # Invalid
                *[
                    {"question_number": i, "question_value": 5}
                    for i in range(2, 11)
                ]
            ]
        }

        async with app.asgi_client as client:
            response = await client.post("/process-survey", json=payload)

        self.assertEqual(response.status_code, 400)
        response_json = await response.json()
        self.assertIn("errors", response_json)
        self.assertIn("question_value must be between 1 and 7.", response_json["errors"])

    async def test_process_survey_invalid_json_payload(self):
        invalid_json = "This is not a JSON payload"

        async with app.asgi_client as client:
            response = await client.post(
                "/process-survey",
                data=invalid_json,
                headers={"Content-Type": "application/json"}
            )

        self.assertEqual(response.status_code, 400)
        response_json = await response.json()
        self.assertIn("error", response_json)
        self.assertEqual(response_json["error"], "Invalid JSON payload.")

    async def test_process_survey_invalid_method(self):
        async with app.asgi_client as client:
            response = await client.get("/process-survey")

        self.assertEqual(response.status_code, 405)  # Method Not Allowed

if __name__ == '__main__':
    unittest.main()
