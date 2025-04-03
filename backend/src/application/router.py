import re
from fastapi import APIRouter, Depends, HTTPException
from src.application.schemas import (
    WebAnalysisRequest, WebAnalysisResponse,
    TextAddRequest, TextSearchRequest, TextSearchResponse
)
from src.application.service import WebAnalysisService, TextAnalysisService

router = APIRouter()
web_analysis_service = WebAnalysisService()
text_analysis_service = TextAnalysisService()


@router.post("/analyze-webpage", response_model=WebAnalysisResponse, summary="Анализ веб-страницы")
async def analyze_webpage(request: WebAnalysisRequest):
    """
    Анализирует веб-страницу с использованием LangChain и Ollama.
    
    Этот эндпоинт:
    1. Загружает содержимое веб-страницы
    2. Разбивает его на чанки
    3. Создает векторное представление
    4. Использует LLM для создания краткого содержания
    
    Args:
        request: Запрос с URL веб-страницы
        
    Returns:
        WebAnalysisResponse: Результаты анализа
    """
    try:
        result = await web_analysis_service.analyze_webpage(str(request.url))
        return WebAnalysisResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при анализе веб-страницы: {str(e)}")

@router.post("/add-texts", summary="Добавление текстов для анализа")
async def add_texts(request: TextAddRequest):
    """
    Добавляет тексты в векторное хранилище для последующего поиска.
    
    Args:
        request: Запрос со списком текстов
        
    Returns:
        dict: Статус операции
    """
    try:
        await text_analysis_service.add_texts(request.texts)
        return {"status": "success", "message": "Тексты успешно добавлены"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при добавлении текстов: {str(e)}")

@router.post("/search-texts", response_model=TextSearchResponse, summary="Поиск по текстам")
async def search_texts(request: TextSearchRequest):
    """
    Выполняет поиск по добавленным текстам с использованием RAG.
    
    Args:
        request: Запрос с поисковым запросом
        
    Returns:
        TextSearchResponse: Результаты поиска
    """
    try:
        result = await text_analysis_service.search(request.query, request.k)
        return TextSearchResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при поиске: {str(e)}")