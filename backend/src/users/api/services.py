from dataclasses import dataclass

from app.services import BaseService
from users.models import User


@dataclass
class UserRegisterService(BaseService):
    username: str
    password: str

    def act(self) -> User:
        return User.objects.create_user(username=self.username, password=self.password, is_active=True)
