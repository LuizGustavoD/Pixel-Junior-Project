from domain.exceptions.domain_exception import DomainException

class UnauthorizedFileAccessException(DomainException):
    """Exception raised when a user tries to access a file they do not own."""
    def __init__(self, message="Você não tem permissão para acessar este arquivo."):
        self.message = message
        super().__init__(self.message)