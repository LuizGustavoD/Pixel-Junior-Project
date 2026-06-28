from flask import Blueprint, request
from infra.security.jwt_service import JwtService
from domain.exceptions import ValidationException
from infra.http.response_builder import ResponseBuilder
from application.dto import TokenVerifyRequestDTO, TokenVerifyResponseDTO, PublicKeyResponseDTO

token_bp = Blueprint('token', __name__, url_prefix='/token')

@token_bp.route('/public-key', methods=['GET'])
def public_key():
    jwt_service = JwtService()
    pub_key = jwt_service.get_public_key()
    if not pub_key:
        raise ValueError("Chave pública não configurada no servidor")
        
    response_dto = PublicKeyResponseDTO(pub_key)
    return ResponseBuilder.success(
        data=response_dto.to_dict(),
        message="Chave pública recuperada com sucesso"
    )

@token_bp.route('/verify', methods=['POST'])
def verify_token():
    data = request.get_json(silent=True) or {}
    token = data.get('token')
    
    if not token:
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            
    dto = TokenVerifyRequestDTO(token)
    if not dto.token:
        raise ValidationException("Token de acesso é obrigatório")
        
    jwt_service = JwtService()
    user_id = jwt_service.decode_access_token(dto.token)
    
    response_dto = TokenVerifyResponseDTO(str(user_id))
    return ResponseBuilder.success(
        data=response_dto.to_dict(),
        message="Token válido"
    )
