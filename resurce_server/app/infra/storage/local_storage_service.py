import os
import shutil
from typing import Generator
from domain.repository.file_storage import FileStorage
from infra.config.settings import Settings

class LocalStorageService(FileStorage):
    def __init__(self, settings: Settings = None):
        self.settings = settings or Settings()
        os.makedirs(self.settings.UPLOAD_DIR, exist_ok=True)

    def save_file(self, file_stream, storage_name: str) -> None:
        file_path = os.path.join(self.settings.UPLOAD_DIR, storage_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file_stream, buffer)

    def delete_file(self, storage_name: str) -> None:
        file_path = os.path.join(self.settings.UPLOAD_DIR, storage_name)
        if os.path.exists(file_path):
            os.remove(file_path)

    def get_file_path(self, storage_name: str) -> str:
        return os.path.join(self.settings.UPLOAD_DIR, storage_name)

    def read_file_chunks(self, storage_name: str, chunk_size: int = 8192) -> Generator[bytes, None, None]:
        file_path = self.get_file_path(storage_name)
        if not os.path.exists(file_path):
            raise FileNotFoundError()
        with open(file_path, "rb") as f:
            while chunk := f.read(chunk_size):
                yield chunk
