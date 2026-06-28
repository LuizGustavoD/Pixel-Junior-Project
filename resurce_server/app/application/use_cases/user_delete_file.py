import uuid
from domain.exceptions import FileNotFoundException, UnauthorizedFileAccessException
from domain.repository.file_repository import FileRepository
from domain.repository.file_storage import FileStorage

class UserDeleteFileUseCase:
    def __init__(self, file_repo: FileRepository, storage_service: FileStorage):
        self.file_repo = file_repo
        self.storage_service = storage_service

    def execute(self, file_id_str: str, user_id_str: str) -> None:
        try:
            file_id = uuid.UUID(file_id_str)
            user_id = uuid.UUID(user_id_str)
        except ValueError:
            raise FileNotFoundException("Arquivo não encontrado.")

        file_metadata = self.file_repo.find_by_id(file_id)
        if not file_metadata:
            raise FileNotFoundException("Arquivo não encontrado.")

        if not file_metadata.belongs_to(user_id):
            raise UnauthorizedFileAccessException("Você não tem permissão para deletar este arquivo.")

        # Physically delete the file
        self.storage_service.delete_file(file_metadata.storage_name)

        # Delete metadata from DB
        self.file_repo.delete(file_id)
