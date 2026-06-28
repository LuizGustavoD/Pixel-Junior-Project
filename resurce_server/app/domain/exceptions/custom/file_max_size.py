from domain.exceptions.domain_exception import DomainException

class FileMaxSizeException(DomainException):
    """Exception raised when an uploaded file exceeds size limit."""
    def __init__(self, message="O arquivo excede o limite máximo permitido."):
        self.message = message
        super().__init__(self.message)