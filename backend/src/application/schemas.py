from pydantic import BaseModel, HttpUrl
from typing import List, Optional


class WebAnalysisRequest(BaseModel):
    url: HttpUrl


class WebAnalysisResponse(BaseModel):
    summary: str
    chunks_count: int
    documents_count: int


class TextAddRequest(BaseModel):
    texts: List[str]


class TextSearchRequest(BaseModel):
    query: str
    k: Optional[int] = 3


class TextSearchResponse(BaseModel):
    answer: str
    sources: List[dict]
