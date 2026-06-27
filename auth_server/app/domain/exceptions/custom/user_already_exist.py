from domain.exceptions.domain_exception import DomainException


class UserAlreadyExistException(DomainException):
    def __init__(self, message: str = "Usuário já existe"):
        super().__init__(message)