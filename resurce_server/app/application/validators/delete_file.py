from domain.exceptions import ValidationException
import uuid

class DeleteFileValidator:
    @staticmethod
    def validate(file_id: str) -> None:
        if not file_id:
            raise ValidationException("O ID do arquivo é obrigatório")
        try:
            uuid.UUID(file_id)
        except ValueError:
            raise ValidationException("O ID do arquivo fornecido é inválido")
