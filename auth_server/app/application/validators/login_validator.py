from domain.exceptions import ValidationException

class LoginValidator:
    
    @staticmethod
    def validate(data: dict) -> None:
        if not data:
            raise ValidationException("Todos os campos são obrigatórios")
            
        email = data.get('email')
        password = data.get('password')
        
        # Se qualquer um dos campos obrigatórios for ausente ou vazio
        if not email or not password:
            raise ValidationException("Todos os campos são obrigatórios")
