import requests
import json

# Flask server endpoint URL
url = 'http://127.0.0.1:5000/api/calculate'

# Test data defined in JSON format
test_data = {
    "경계 지수": 85,
    "애정 지수": 75,
    "친밀 지수": 72,
    "대화 흐름 지수": 88,
    "상호존중 및 공감 지수": 80,
    "호기심 지수": 77,
    "유머 지수": 73,
    "개인 맞춤형 조언": "test"
}

# JSON data sent to the server
try:
    response = requests.post(url, json={"data": test_data})
    response.raise_for_status()  # Raises an exception if the response is not successful
    result = response.json()

    # Output the response result
    print("Calculated H:", result.get("H"))
    print("개인 맞춤형 조언:", result.get("개인 맞춤형 조언"))

except requests.exceptions.RequestException as e:
    print(f"Error sending request to server: {e}")

except json.JSONDecodeError:
    print("Error decoding the JSON response from the server.")