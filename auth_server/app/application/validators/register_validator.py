from domain.exceptions import ValidationException
from application.dto import UserRegisterRequestDTO

class RegisterValidator:
    
    @staticmethod
    def validate(dto: UserRegisterRequestDTO) -> None:
        if not dto:
            raise ValidationException("Todos os campos são obrigatórios")
            
        # Se qualquer um dos campos principais for ausente ou vazio
        if not dto.email or not dto.username or not dto.password:
            raise ValidationException("Todos os campos são obrigatórios")
            
        # Validar formato do email de forma simples
        if "@" not in dto.email or "." not in dto.email:
            raise ValidationException("E-mail com formato inválido")
            
        # Validar tamanho da senha
        if len(dto.password) < 6:
            raise ValidationException("A senha deve conter pelo menos 6 caracteres")
