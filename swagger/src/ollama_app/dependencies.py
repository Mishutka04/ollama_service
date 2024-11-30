from os import getenv
from dotenv import load_dotenv
from fastapi import HTTPException
import openai

from ollama_app.schemas import SOllamaModel

load_dotenv()

# Set your OpenAI API key and base URL
openai.api_key = 'ollama'  # Replace with your actual API key
base_url = 'http://localhost:11434/v1'  # Replace with your actual base URL

async def qween_api(comment: SOllamaModel):
    
    try:
        response = openai.ChatCompletion.create(
            model="qwen2.5:32b",
            messages={"role": comment.role, "content": comment.content},
            api_base=base_url  # Use the specified base URL
        )
        # Extract the response content
        response_content = response.choices[0].message.content
        return {"response": response_content}
    except Exception as e:
        return False

