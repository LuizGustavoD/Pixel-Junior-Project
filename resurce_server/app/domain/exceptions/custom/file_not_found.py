from domain.exceptions.domain_exception import DomainException


class FileNotFoundException(DomainException):
    """Exception raised when a file is not found."""
    def __init__(self, message="File not found."):
        self.message = message
        super().__init__(self.message)