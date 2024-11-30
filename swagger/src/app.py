from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ollama_app.router import model_router

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

app.include_router(model_router)