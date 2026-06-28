import uuid
from domain.exceptions import FileNotFoundException, UnauthorizedFileAccessException
from domain.repository.file_repository import FileRepository
from domain.repository.file_storage import FileStorage

class UserGetFileUseCase:
    def __init__(self, file_repo: FileRepository, storage_service: FileStorage):
        self.file_repo = file_repo
        self.storage_service = storage_service

    def execute(self, file_id_str: str, user_id_str: str):
        try:
            file_id = uuid.UUID(file_id_str)
            user_id = uuid.UUID(user_id_str)
        except ValueError:
            raise FileNotFoundException("Arquivo não encontrado.")

        file_metadata = self.file_repo.find_by_id(file_id)
        if not file_metadata:
            raise FileNotFoundException("Arquivo não encontrado.")

        if not file_metadata.belongs_to(user_id):
            raise UnauthorizedFileAccessException("Você não tem permissão para acessar este arquivo.")

        # Return metadata and generator function to read chunks
        generator = self.storage_service.read_file_chunks(file_metadata.storage_name)
        return file_metadata, generator
