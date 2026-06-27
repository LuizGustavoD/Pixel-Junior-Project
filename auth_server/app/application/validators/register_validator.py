from domain.exceptions import ValidationException

class RegisterValidator:
    
    @staticmethod
    def validate(data: dict) -> None:
        if not data:
            raise ValidationException("Todos os campos são obrigatórios")
            
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        
        # Se qualquer um dos campos principais for ausente ou vazio
        if not email or not username or not password:
            raise ValidationException("Todos os campos são obrigatórios")
            
        # Validar formato do email de forma simples
        if "@" not in email or "." not in email:
            raise ValidationException("E-mail com formato inválido")
            
        # Validar tamanho da senha
        if len(password) < 6:
            raise ValidationException("A senha deve conter pelo menos 6 caracteres")
