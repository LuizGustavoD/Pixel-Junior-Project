import uuid
import io
from PIL import Image
from domain.exceptions import FileNotFoundException, UnauthorizedFileAccessException, ValidationException
from domain.repository.file_repository import FileRepository
from domain.repository.file_storage import FileStorage

class UserGetThumbnailUseCase:
    def __init__(self, file_repo: FileRepository, storage_service: FileStorage):
        self.file_repo = file_repo
        self.storage_service = storage_service

    def execute(self, file_id_str: str, user_id_str: str) -> tuple[io.BytesIO, str]:
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

        if not file_metadata.content_type.startswith("image/"):
            raise ValidationException("O arquivo solicitado não é uma imagem válida para miniatura.")

        file_path = self.storage_service.get_file_path(file_metadata.storage_name)
        
        try:
            with Image.open(file_path) as img:
                # Convert RGBA or Palette mode to RGB for JPEG compatibility
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                
                img.thumbnail((120, 120))
                
                thumb_io = io.BytesIO()
                img.save(thumb_io, "JPEG", quality=85)
                thumb_io.seek(0)
                
                return thumb_io, "image/jpeg"
        except Exception as e:
            raise ValidationException(f"Erro ao processar imagem para miniatura: {str(e)}")
