from flask import Flask
from werkzeug.exceptions import HTTPException
from domain.exceptions import (
    DomainException,
    FileNotFoundException,
    UnauthorizedFileAccessException,
    EmptyFileException,
    FileMaxSizeException,
    NotSupportFileTypeException,
    UploadFailedException,
    ValidationException
)
from infra.http.response_builder import ResponseBuilder

def register_error_handlers(app: Flask):

    @app.errorhandler(FileNotFoundException)
    def handle_file_not_found(error: FileNotFoundException):
        return ResponseBuilder.error(code="FILE_NOT_FOUND", message=error.message, status_code=404)

    @app.errorhandler(UnauthorizedFileAccessException)
    def handle_unauthorized_file(error: UnauthorizedFileAccessException):
        return ResponseBuilder.error(code="UNAUTHORIZED_ACCESS", message=error.message, status_code=403)

    @app.errorhandler(EmptyFileException)
    def handle_empty_file(error: EmptyFileException):
        return ResponseBuilder.error(code="EMPTY_FILE", message=error.message, status_code=400)

    @app.errorhandler(FileMaxSizeException)
    def handle_file_max_size(error: FileMaxSizeException):
        return ResponseBuilder.error(code="FILE_TOO_LARGE", message=error.message, status_code=400)

    @app.errorhandler(NotSupportFileTypeException)
    def handle_not_supported_type(error: NotSupportFileTypeException):
        return ResponseBuilder.error(code="UNSUPPORTED_TYPE", message=error.message, status_code=400)

    @app.errorhandler(UploadFailedException)
    def handle_upload_failed(error: UploadFailedException):
        return ResponseBuilder.error(code="UPLOAD_FAILED", message=error.message, status_code=500)

    @app.errorhandler(ValidationException)
    def handle_validation_error(error: ValidationException):
        return ResponseBuilder.error(code="VALIDATION_ERROR", message=error.message, details=error.details, status_code=400)

    @app.errorhandler(DomainException)
    def handle_domain_error(error: DomainException):
        return ResponseBuilder.error(code="DOMAIN_ERROR", message=error.message, status_code=400)

    @app.errorhandler(HTTPException)
    def handle_http_error(error: HTTPException):
        return ResponseBuilder.error(code="HTTP_ERROR", message=error.description, status_code=error.code)

    @app.errorhandler(Exception)
    def handle_unexpected_error(error: Exception):
        app.logger.error(f"Erro inesperado no servidor de recursos: {str(error)}", exc_info=True)
        return ResponseBuilder.error(code="INTERNAL_SERVER_ERROR", message="Ocorreu um erro interno no servidor de recursos.", status_code=500)