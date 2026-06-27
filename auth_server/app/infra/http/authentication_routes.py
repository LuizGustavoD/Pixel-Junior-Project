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

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    RegisterValidator.validate(data)
        
    db = SessionLocal()
    try:
        user_repo = MySqlUserRepository(db)
        hasher = PasswordHasher()
        use_case = RegisterUserUseCase(user_repo, hasher)
        
        user_data = {
            "email": data['email'],
            "username": data['username'],
            "password": data['password']
        }
        saved_user = use_case.execute(user_data)
        
        response_data = {
            "id": str(saved_user.id),
            "email": saved_user.email,
            "username": saved_user.username,
            "created_at": saved_user.created_at.isoformat()
        }
        return ResponseBuilder.success(
            data=response_data,
            message="Usuário registrado com sucesso",
            status_code=201
        )
    finally:
        db.close()

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    LoginValidator.validate(data)
        
    db = SessionLocal()
    try:
        user_repo = MySqlUserRepository(db)
        hasher = PasswordHasher()
        jwt_service = JwtService()
        use_case = LoginUserUseCase(user_repo, hasher, jwt_service)
        
        credentials = {
            "email": data['email'],
            "password": data['password']
        }
        result = use_case.execute(credentials)
        return ResponseBuilder.success(
            data=result,
            message="Login realizado com sucesso",
            status_code=200
        )
    finally:
        db.close()

@auth_bp.route('/public-key', methods=['GET'])
def public_key():
    jwt_service = JwtService()
    pub_key = jwt_service.get_public_key()
    if not pub_key:
        raise ValueError("Chave pública não configurada no servidor")
    return ResponseBuilder.success(
        data={"public_key": pub_key},
        message="Chave pública recuperada com sucesso"
    )

@auth_bp.route('/verify', methods=['POST'])
def verify_token():
    data = request.get_json(silent=True) or {}
    token = data.get('token')
    
    if not token:
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            
    if not token:
        raise ValidationException("Token de acesso é obrigatório")
        
    jwt_service = JwtService()
    user_id = jwt_service.decode_access_token(token)
    
    return ResponseBuilder.success(
        data={"user_id": user_id},
        message="Token válido"
    )

