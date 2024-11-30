from pydantic import BaseModel


class SOllamaModel(BaseModel):
    role: str
    content: str