from domain.exceptions.domain_exception import DomainException

class EmptyFileException(DomainException):
    """Exception raised when an uploaded file is empty."""
    def __init__(self, message="O arquivo enviado está vazio."):
        self.message = message
        super().__init__(self.message)