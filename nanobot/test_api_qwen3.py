import requests

url = "http://localhost:42005/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer my-secret-qwen-key"
}

# Пробуем разные модели
models_to_try = ["qwen3-coder-plus", "qwen3-coder-flash", "coder-model"]

for model in models_to_try:
    print(f"\nTrying model: {model}")
    data = {
        "model": model,
        "messages": [{"role": "user", "content": "What is 2+2?"}],
        "max_tokens": 100
    }
    response = requests.post(url, json=data, headers=headers)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()['choices'][0]['message']['content']}")
    else:
        print(f"Error: {response.text}")
