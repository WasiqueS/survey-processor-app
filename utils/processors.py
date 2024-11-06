import statistics

def process_survey_results(payload):
    survey_results = payload['survey_results']
    user_id = payload['user_id']

    # Map question_number to question_value
    question_dict = {item['question_number']: item['question_value'] for item in survey_results}
    question_values = list(question_dict.values())

    # Calculate statistics
    mean_value = round(statistics.mean(question_values), 1)
    median_value = round(statistics.median(question_values), 1)
    std_dev_value = round(statistics.stdev(question_values), 1)

    # Rule 1: Overall Analysis
    if question_dict[1] == 7 and question_dict[4] < 3:
        overall_analysis = "unsure"
    else:
        overall_analysis = "certain"

    # Rule 2: Cat or Dog
    if question_dict[10] > 5 and question_dict[9] <= 5:
        cat_dog = "cats"
    else:
        cat_dog = "dogs"

    # Rule 3: Fur Value
    fur_value = "long" if mean_value > 5 else "short"

    # Rule 4: Tail Value
    tail_value = "long" if question_dict[7] > 4 else "short"

    # Rule 5: Description Generation
    description = generate_description(mean_value)

    # Prepare the response data
    response_data = {
        "overall_analysis": overall_analysis,
        "cat_dog": cat_dog,
        "fur_value": fur_value,
        "tail_value": tail_value,
        "description": description,
        "statistics": {
            "mean": mean_value,
            "median": median_value,
            "std_dev": std_dev_value
        }
    }

    return response_data

def generate_description(average_value):
    with open('data/system_prompt.txt', 'r') as f:
        system_prompt = f.read()

    if average_value > 4:
        file_name = 'data/the_value_of_short_hair.txt'
    else:
        file_name = 'data/the_value_of_long_hair.txt'

    with open(file_name, 'r') as f:
        content = f.read()

    description = f"Generated description based on {'short hair' if average_value > 4 else 'long hair'}."

    return description
