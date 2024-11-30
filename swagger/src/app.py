from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from ollama_app.router import model_router
from ollama_service.swagger.src.ollama_app.dependencies import qween_api
from ollama_service.swagger.src.ollama_app.schemas import SOllamaModel

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
    if not request:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error Model")
    return request
app.include_router(model_router)