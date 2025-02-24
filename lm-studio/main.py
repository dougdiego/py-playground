import requests

# Define the API endpoint and model
API_URL = "http://127.0.0.1:1234/v1/completions"
MODEL_NAME = "deepseek-r1-distill-qwen-7b"

# Define the request payload
payload = {
    "model": MODEL_NAME,
    "prompt": "What is the capital of France?",
    "max_tokens": 50,
    "temperature": 0.7
}

# Make the request
response = requests.post(API_URL, json=payload)

# Parse and print the response
if response.status_code == 200:
    result = response.json()
    print("Model response:", result.get("choices", [{}])[0].get("text", "").strip())
else:
    print("Error:", response.status_code, response.text)