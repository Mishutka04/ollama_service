import json
from os import getenv
from dotenv import load_dotenv
from fastapi import HTTPException
import requests
import openai

from ollama_app.schemas import SOllamaModel
from openai import OpenAI
load_dotenv()

# Set your OpenAI API key and base URL
openai.api_key = 'ollama'  # Replace with your actual API key
base_url = 'http://localhost:11434/v1'  # Replace with your actual base URL
client = OpenAI(
    api_key='ollama',  # This is the default and can be omitted
)
async def qween_api(comment: SOllamaModel):
        # URL и параметры запроса
    url = "http://localhost:11434/api/generate"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "model": "qwen2.5:32b",
        "prompt": "Что такое вода?"
    }

    # Отправка POST-запроса
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Проверка статуса ответа
    if response.status_code == 200:
        response_data = response.json()
        print(response_data)  # Выводим ответ от модели
    else:
        print(f"Ошибка: {response.status_code} - {response.text}")
    