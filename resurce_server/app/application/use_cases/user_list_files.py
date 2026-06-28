import uuid
from domain.repository.file_repository import FileRepository

class UserListFilesUseCase:
    def __init__(self, file_repo: FileRepository):
        self.file_repo = file_repo

    def execute(self, user_id_str: str):
        user_id = uuid.UUID(user_id_str)
        return self.file_repo.find_by_owner_id(user_id)
