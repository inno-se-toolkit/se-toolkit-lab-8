import requests

url = "http://localhost:42005/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer my-secret-qwen-key"
}
data = {
    "model": "coder-model",
    "messages": [{"role": "user", "content": "What is 2+2?"}],
    "max_tokens": 100
}

response = requests.post(url, json=data, headers=headers)
print("Status Code:", response.status_code)
print("Response:", response.text)
