from flask import Blueprint, request
from infra.config.db import SessionLocal
from infra.repository.mysql_user_repository import MySqlUserRepository
from infra.security.password_hasher import PasswordHasher
from infra.security.jwt_service import JwtService
from application.use_cases.register_user import RegisterUserUseCase
from application.use_cases.login_user import LoginUserUseCase
from domain.exceptions import ValidationException
from infra.http.response_builder import ResponseBuilder
from application.validators import RegisterValidator, LoginValidator
from application.dto import UserRegisterRequestDTO, UserLoginRequestDTO

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    dto = UserRegisterRequestDTO.from_dict(data)
    RegisterValidator.validate(dto)
        
    db = SessionLocal()
    
    try:
        user_repo = MySqlUserRepository(db)
        hasher = PasswordHasher()
        use_case = RegisterUserUseCase(user_repo, hasher)
        
        response_dto = use_case.execute(dto)
        return ResponseBuilder.success(
            data=response_dto.to_dict(),
            message="Usuário registrado com sucesso",
            status_code=201
        )
    finally:
        db.close()

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    dto = UserLoginRequestDTO.from_dict(data)
    LoginValidator.validate(dto)
        
    db = SessionLocal()
    try:
        user_repo = MySqlUserRepository(db)
        hasher = PasswordHasher()
        jwt_service = JwtService()
        use_case = LoginUserUseCase(user_repo, hasher, jwt_service)
        
        result = use_case.execute(dto)
        return ResponseBuilder.success(
            data=result,
            message="Login realizado com sucesso",
            status_code=200
        )
    finally:
        db.close()

