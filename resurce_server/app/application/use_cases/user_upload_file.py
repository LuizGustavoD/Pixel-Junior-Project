from datetime import datetime
import uuid
from domain.entities.file import File
from domain.repository.file_repository import FileRepository
from domain.repository.file_storage import FileStorage

class UserUploadFileUseCase:
    def __init__(self, file_repo: FileRepository, storage_service: FileStorage):
        self.file_repo = file_repo
        self.storage_service = storage_service

    def execute(self, file_stream, filename: str, content_type: str, size: int, owner_id: str, owner_username: str = None) -> File:
        file_id = uuid.uuid4()
        extension = filename.split(".")[-1].lower() if "." in filename else ""
        
        folder_name = owner_username if owner_username else owner_id
        file_key = f"{file_id}.{extension}" if extension else f"{file_id}"
        storage_name = f"users/{folder_name}/{file_key}"

        # Write to physical storage
        self.storage_service.save_file(file_stream, storage_name)

        # Write metadata to DB
        file_entity = File(
            id=file_id,
            owner_id=uuid.UUID(owner_id),
            original_name=filename,
            storage_name=storage_name,
            content_type=content_type,
            size=size,
            created_at=datetime.utcnow()
        )

        self.file_repo.save(file_entity)
        return file_entity
