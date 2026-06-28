from domain.exceptions.domain_exception import DomainException

class NotSupportFileTypeException(DomainException):
    """Exception raised when an uploaded file type is not supported."""
    def __init__(self, message="Tipo de arquivo não suportado."):
        self.message = message
        super().__init__(self.message)