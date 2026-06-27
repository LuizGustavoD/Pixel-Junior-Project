from datetime import datetime
from uuid import uuid4

from domain.entities.user import User
from domain.exceptions import UserAlreadyExistException


class RegisterUserUseCase:
    def __init__(self, user_repository, password_hasher):
        self.user_repository = user_repository
        self.password_hasher = password_hasher

    def execute(self, user_data):
        if self.user_repository.exists_by_email(user_data['email']):
            raise UserAlreadyExistException("E-mail já cadastrado")

        hashed_password = self.password_hasher.hash(user_data['password'])
        user = User(
            id=uuid4(),
            email=user_data['email'],
            username=user_data['username'],
            password=hashed_password,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        saved_user = self.user_repository.save(user)
        return saved_user