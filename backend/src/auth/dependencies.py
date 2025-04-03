from fastapi import HTTPException, Request, Depends

async def get_token(request: Request) -> str:
    """
    Асинхронная функция для получения токена из cookies.
    
    Args:
        request (Request): FastAPI Request объект
        
    Returns:
        str: Токен доступа
        
    Raises:
        HTTPException: Если токен отсутствует
    """
    token = request.cookies.get('access_token')
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Authentication credentials were not provided"
        )
    return token