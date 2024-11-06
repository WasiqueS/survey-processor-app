from models.database import collection
from sanic import Sanic
from sanic.response import json
from utils.validators import validate_payload
from utils.processors import process_survey_results
import logging

# Configure logging
logger = logging.getLogger('sanic')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', "%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)
logger.addHandler(handler)

app = Sanic("SurveyProcessorApp")

@app.route("/process-survey", methods=["POST"])
async def process_survey(request):
    payload = request.json
    if not payload:
        return json({"error": "Invalid JSON payload."}, status=400)

    errors = validate_payload(payload)
    if errors:
        return json({"errors": errors}, status=400)

    response_data = process_survey_results(payload)

    # Store data asynchronously
    user_id = payload['user_id']
    record = {
        "user_id": user_id,
        **response_data,
        "survey_results": payload['survey_results']
    }
    await collection.insert_one(record)

    return json(response_data, status=200)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
