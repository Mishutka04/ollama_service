from fastapi import APIRouter, HTTPException, status, UploadFile, File


from ollama_app.dependencies import qween_api
from ollama_app.schemas import SOllamaModel

model_router = APIRouter(
    prefix='/api/qween',
    tags=['Qween Model']
)


