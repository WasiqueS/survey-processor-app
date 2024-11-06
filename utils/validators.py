import re

def validate_payload(payload):
    errors = []

    # Validate user_id
    user_id = payload.get('user_id')
    if not user_id:
        errors.append("user_id is missing.")
    elif not isinstance(user_id, str):
        errors.append("user_id must be a string.")
    elif len(user_id) < 5:
        errors.append("user_id must be at least 5 characters long.")
    elif not re.match(r'^\w+$', user_id):
        errors.append("user_id must be alphanumeric and underscores only.")

    # Validate survey_results
    survey_results = payload.get('survey_results')
    if not survey_results:
        errors.append("survey_results is missing.")
    elif not isinstance(survey_results, list):
        errors.append("survey_results must be a list.")
    elif len(survey_results) != 10:
        errors.append("survey_results must contain exactly 10 items.")
    else:
        question_numbers = set()
        for result in survey_results:
            # Validate question_number
            question_number = result.get('question_number')
            if question_number is None:
                errors.append("Each survey result must have a question_number.")
            elif not isinstance(question_number, int):
                errors.append("question_number must be an integer.")
            elif not (1 <= question_number <= 10):
                errors.append("question_number must be between 1 and 10.")
            elif question_number in question_numbers:
                errors.append(f"Duplicate question_number {question_number}.")
            question_numbers.add(question_number)

            # Validate question_value
            question_value = result.get('question_value')
            if question_value is None:
                errors.append("Each survey result must have a question_value.")
            elif not isinstance(question_value, int):
                errors.append("question_value must be an integer.")
            elif not (1 <= question_value <= 7):
                errors.append("question_value must be between 1 and 7.")

    return errors
