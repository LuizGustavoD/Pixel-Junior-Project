from abc import ABC, abstractmethod
from typing import Generator

class FileStorage(ABC):
    @abstractmethod
    def save_file(self, file_stream, storage_name: str) -> None:
        """Saves file from a stream/file object to the storage medium."""
        pass

    @abstractmethod
    def delete_file(self, storage_name: str) -> None:
        """Deletes a file from the storage medium."""
        pass

    @abstractmethod
    def get_file_path(self, storage_name: str) -> str:
        """Gets absolute path/identifier to a file."""
        pass

    @abstractmethod
    def read_file_chunks(self, storage_name: str, chunk_size: int = 8192) -> Generator[bytes, None, None]:
        """Generator to stream the file in chunks from storage."""
        pass
