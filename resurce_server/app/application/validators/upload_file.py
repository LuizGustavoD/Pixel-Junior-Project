from domain.exceptions import (
    ValidationException,
    NotSupportFileTypeException,
    FileMaxSizeException
)
import os

class UploadFileValidator:
    ALLOWED_EXTENSIONS = {'.png', '.jpg', '.pdf', '.txt'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

    @staticmethod
    def validate(file, filename: str, size: int) -> None:
        if not file or not filename:
            raise ValidationException("Arquivo é obrigatório")

        _, ext = os.path.splitext(filename.lower())
        if ext not in UploadFileValidator.ALLOWED_EXTENSIONS:
            raise NotSupportFileTypeException("Extensão de arquivo não permitida. Apenas .png, .jpg, .pdf e .txt são aceitas.")

        if size > UploadFileValidator.MAX_FILE_SIZE:
            raise FileMaxSizeException("O arquivo excede o limite máximo de 10MB.")

