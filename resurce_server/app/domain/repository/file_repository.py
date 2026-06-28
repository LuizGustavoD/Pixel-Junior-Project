from abc import ABC, abstractmethod
from uuid import UUID
from domain.entities.file import File

class FileRepository(ABC):
    
    @abstractmethod
    def save(self, file: File) -> File:
        """Save file metadata."""
        pass

    @abstractmethod
    def find_by_id(self, file_id: UUID) -> File | None:
        """Find file metadata by ID."""
        pass

    @abstractmethod
    def delete(self, file_id: UUID) -> None:
        """Delete file metadata."""
        pass

    @abstractmethod
    def find_by_owner_id(self, owner_id: UUID) -> list[File]:
        """Retrieve all non-deleted files belonging to a specific owner."""
        pass