from domain.exceptions import ValidationException
from application.dto import UserLoginRequestDTO

class LoginValidator:
    
    @staticmethod
    def validate(dto: UserLoginRequestDTO) -> None:
        if not dto:
            raise ValidationException("Todos os campos são obrigatórios")
            
        # Se qualquer um dos campos obrigatórios for ausente ou vazio
        if not dto.email or not dto.password:
            raise ValidationException("Todos os campos são obrigatórios")
