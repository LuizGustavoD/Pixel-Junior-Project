import uuid
from sqlalchemy.orm import Session

from domain.entities.user import User
from domain.repositories.user_repository import UserRepository
from infra.models.user_model import UserModel


class MySqlUserRepository(UserRepository):

    def __init__(self, session: Session):
        self.session = session

    def save(self, user: User) -> User:
        model = UserModel(
            id=str(user.id),
            email=user.email,
            username=user.username,
            password=user.password,
            created_at=user.created_at,
            updated_at=user.updated_at
        )

        self.session.add(model)
        self.session.commit()
        return user

    def find_by_email(self, email: str) -> User | None:
        model = (
            self.session.query(UserModel)
            .filter(UserModel.email == email)
            .first()
        )

        if model is None:
            return None

        return User(
            id=uuid.UUID(model.id),
            email=model.email,
            username=model.username,
            password=model.password,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def find_by_id(self, user_id: uuid.UUID) -> User | None:
        model = (
            self.session.query(UserModel)
            .filter(UserModel.id == str(user_id))
            .first()
        )

        if model is None:
            return None

        return User(
            id=uuid.UUID(model.id),
            email=model.email,
            username=model.username,
            password=model.password,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def exists_by_email(self, email: str) -> bool:
        return (
            self.session.query(UserModel)
            .filter(UserModel.email == email)
            .first()
            is not None
        )

    def delete(self, user_id: uuid.UUID) -> None:
        model = (
            self.session.query(UserModel)
            .filter(UserModel.id == str(user_id))
            .first()
        )

        if model is not None:
            self.session.delete(model)
            self.session.commit()

    def update(self, user: User) -> User:
        model = (
            self.session.query(UserModel)
            .filter(UserModel.id == str(user.id))
            .first()
        )
        if model is None:
            raise ValueError("Usuário não encontrado para atualização")

        model.email = user.email
        model.username = user.username
        model.password = user.password
        model.updated_at = user.updated_at

        self.session.commit()
        return user


 
 