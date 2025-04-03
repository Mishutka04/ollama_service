from src.auth.models import User

from src.service.base import BaseService

class UserService(BaseService):
    model = User