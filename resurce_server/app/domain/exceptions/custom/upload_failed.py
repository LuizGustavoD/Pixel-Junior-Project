from domain.exceptions.domain_exception import DomainException 

class UploadFailedException(DomainException):
    """Exception raised when a file upload fails."""
    def __init__(self, message="File upload failed."):
        self.message = message
        super().__init__(self.message)