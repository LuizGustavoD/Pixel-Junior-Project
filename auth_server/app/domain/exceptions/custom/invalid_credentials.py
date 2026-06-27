from domain.exceptions.domain_exception import DomainException

class InvalidCredentialsException(DomainException):
    def __init__(self, message: str = "Credenciais inválidas"):
        super().__init__(message)
        