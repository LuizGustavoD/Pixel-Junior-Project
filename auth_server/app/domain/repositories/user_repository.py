from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.user import User


class UserRepository(ABC):

    @abstractmethod
    def save(self, user: User) -> User:
        """Salva um usuário."""
        pass

    @abstractmethod
    def find_by_id(self, user_id: UUID) -> User | None:
        """Busca um usuário pelo ID."""
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> User | None:
        """Busca um usuário pelo e-mail."""
        pass

    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        """Verifica se o e-mail já está cadastrado."""
        pass

    @abstractmethod
    def delete(self, user_id: UUID) -> None:
        """Remove um usuário."""
        pass
    
    @abstractmethod
    def update(self, user: User) -> User:
        """Atualiza um usuário."""
        pass