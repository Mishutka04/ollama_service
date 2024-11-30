import json
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from openai import BaseModel

from ollama_app.router import model_router
from ollama_app.dependencies import qween_api
from ollama_app.schemas import SOllamaModel
import requests
app = FastAPI(
    title="GitCTO auto review API",
    description="FastAPI api for review.gitcto.space",
    version="0.0.1",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],   # Allows all headers
)
@app.post("/query")
async def request_to_qween(settings: SOllamaModel):
    request = await qween_api(settings)
    return request

class GenerateRequest(BaseModel):
    model: str              # Name of the model to be used
    prompt: str             # Prompt to be sent to the model
    stream: bool = False    # Flag to enable streaming of responses

# Define endpoint to handle requests and return the full raw JSON response
@app.post("/generate")
async def generate_full(request: GenerateRequest):
    url = "http://localhost:11434/api/generate"     # URL of the local model API
    headers = {"Content-Type": "application/json"}  # Specify the content type as JSON
    data = {
        "model": request.model,     # Model name from the request
        "prompt": request.prompt,   # Prompt from the request
        "stream": request.stream    # Streaming flag from the request
    }

    # Send a POST request to the model API
    response = requests.post(url, headers=headers, data=json.dumps(data), stream=True)
    
    # Capture streamed responses line by line
    raw_response = ""
    for line in response.iter_lines():
        if line:
            raw_response += line.decode('utf-8') + "\n"     # Accumulate the response
    
    # Return the full JSON response as a string
    return raw_response
app.include_router(model_router)