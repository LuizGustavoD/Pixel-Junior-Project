from datetime import datetime
from uuid import uuid4

from domain.entities.user import User
from domain.exceptions import UserAlreadyExistException
from application.dto import UserRegisterRequestDTO, UserResponseDTO


class RegisterUserUseCase:
    def __init__(self, user_repository, password_hasher):
        self.user_repository = user_repository
        self.password_hasher = password_hasher

    def execute(self, request_dto: UserRegisterRequestDTO) -> UserResponseDTO:
        if self.user_repository.exists_by_email(request_dto.email):
            raise UserAlreadyExistException("E-mail já cadastrado")

        hashed_password = self.password_hasher.hash(request_dto.password)
        user = User(
            id=uuid4(),
            email=request_dto.email,
            username=request_dto.username,
            password=hashed_password,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        saved_user = self.user_repository.save(user)
        return UserResponseDTO(saved_user)