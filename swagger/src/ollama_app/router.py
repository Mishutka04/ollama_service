from fastapi import APIRouter, HTTPException, status, UploadFile, File


from ollama_app.dependencies import qween_api, review_python_code_qween, review_typescript_code_qween, review_code_evraz, select_code_qween, review_с_code_qween, extract_and_read_archive, review_one_code_qween
from ollama_app.schemas import SOllamaModel

model_router = APIRouter(
    prefix='/api/qween',
    tags=['Qween Model']
)


@model_router.post("/query")
async def request_to_qween(settings: SOllamaModel):
    request = await qween_api(settings)
    if not request:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error Model")
    return request