from flask import Flask
from werkzeug.exceptions import HTTPException
from domain.exceptions import (
    DomainException,
    InvalidCredentialsException,
    UserAlreadyExistException,
    UserNotFoundException,
    ValidationException
)
from infra.http.response_builder import ResponseBuilder

def register_error_handlers(app: Flask):
    
    @app.errorhandler(InvalidCredentialsException)
    def handle_invalid_credentials(error: InvalidCredentialsException):
        return ResponseBuilder.error(
            code="INVALID_CREDENTIALS",
            message=error.message,
            status_code=401
        )
        
    @app.errorhandler(UserAlreadyExistException)
    def handle_user_already_exist(error: UserAlreadyExistException):
        return ResponseBuilder.error(
            code="USER_ALREADY_EXISTS",
            message=error.message,
            status_code=400
        )
        
    @app.errorhandler(UserNotFoundException)
    def handle_user_not_found(error: UserNotFoundException):
        return ResponseBuilder.error(
            code="USER_NOT_FOUND",
            message=error.message,
            status_code=404
        )
        
    @app.errorhandler(ValidationException)
    def handle_validation(error: ValidationException):
        return ResponseBuilder.error(
            code="VALIDATION_ERROR",
            message=error.message,
            details=error.details,
            status_code=400
        )
        
    @app.errorhandler(DomainException)
    def handle_domain_exception(error: DomainException):
        return ResponseBuilder.error(
            code="DOMAIN_ERROR",
            message=error.message,
            status_code=400
        )
        
    @app.errorhandler(HTTPException)
    def handle_http_exception(error: HTTPException):
        return ResponseBuilder.error(
            code="HTTP_ERROR",
            message=error.description,
            status_code=error.code
        )
        
    @app.errorhandler(Exception)
    def handle_unexpected_exception(error: Exception):
        app.logger.error(f"Erro inesperado capturado: {str(error)}", exc_info=True)
        return ResponseBuilder.error(
            code="INTERNAL_SERVER_ERROR",
            message="Ocorreu um erro interno no servidor.",
            status_code=500
        )
