from domain.exceptions.domain_exception import DomainException

class ValidationException(DomainException):
    def __init__(self, message: str = "Erro de validação de dados", details: dict = None):
        super().__init__(message)
        self.details = details
