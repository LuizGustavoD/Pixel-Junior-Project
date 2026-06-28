import uuid
from sqlalchemy.orm import Session
from domain.entities.file import File
from domain.repository.file_repository import FileRepository
from infra.models.file_model import FileModel

class MySQLFileRepository(FileRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, file: File) -> File:
        model = FileModel(
            id=str(file.id),
            owner_id=str(file.owner_id),
            original_name=file.original_name,
            storage_name=file.storage_name,
            content_type=file.content_type,
            size=file.size,
            created_at=file.created_at,
            is_deleted=file.is_deleted
        )
        
        # Check if already exists to do update or insert
        existing = self.session.query(FileModel).filter(FileModel.id == str(file.id)).first()
        if existing:
            existing.original_name = file.original_name
            existing.storage_name = file.storage_name
            existing.content_type = file.content_type
            existing.size = file.size
            existing.is_deleted = file.is_deleted
        else:
            self.session.add(model)
        self.session.commit()
        return file

    def find_by_id(self, file_id: uuid.UUID) -> File | None:
        model = self.session.query(FileModel).filter(FileModel.id == str(file_id), FileModel.is_deleted == False).first()
        if not model:
            return None
        return File(
            id=uuid.UUID(model.id),
            owner_id=uuid.UUID(model.owner_id),
            original_name=model.original_name,
            storage_name=model.storage_name,
            content_type=model.content_type,
            size=model.size,
            created_at=model.created_at,
            is_deleted=model.is_deleted
        )

    def delete(self, file_id: uuid.UUID) -> None:
        model = self.session.query(FileModel).filter(FileModel.id == str(file_id)).first()
        if model:
            self.session.delete(model)
            self.session.commit()

    def find_by_owner_id(self, owner_id: uuid.UUID) -> list[File]:
        models = self.session.query(FileModel).filter(
            FileModel.owner_id == str(owner_id),
            FileModel.is_deleted == False
        ).order_by(FileModel.created_at.desc()).all()
        
        return [
            File(
                id=uuid.UUID(m.id),
                owner_id=uuid.UUID(m.owner_id),
                original_name=m.original_name,
                storage_name=m.storage_name,
                content_type=m.content_type,
                size=m.size,
                created_at=m.created_at,
                is_deleted=m.is_deleted
            )
            for m in models
        ]