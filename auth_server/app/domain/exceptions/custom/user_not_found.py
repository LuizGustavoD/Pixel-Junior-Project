from domain.exceptions.domain_exception import DomainException

class UserNotFoundException(DomainException):
    def __init__(self, message: str = "Usuário não encontrado"):
        super().__init__(message)