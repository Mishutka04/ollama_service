
from sqlalchemy import Column, Integer, String

from src.database import Base


class User(Base):
    """Модель пользователя в базе данных."""
    
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)