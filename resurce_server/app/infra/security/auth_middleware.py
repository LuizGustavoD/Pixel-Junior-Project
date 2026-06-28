from functools import wraps
import os
from flask import request, g
import jwt
import requests
from infra.config.settings import Settings
from infra.http.response_builder import ResponseBuilder

settings = Settings()

def get_token_from_header():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    return auth_header.split(" ")[1]

def verify_token_locally(token: str) -> str | None:
    if os.path.exists(settings.PUBLIC_KEY_PATH):
        try:
            with open(settings.PUBLIC_KEY_PATH, "r") as f:
                public_key = f.read()
            payload = jwt.decode(token, public_key, algorithms=[settings.JWT_ALGORITHM])
            return payload.get("user_id") or payload.get("sub")
        except Exception:
            return None
    return None

def verify_token_remotely(token: str) -> str | None:
    try:
        response = requests.post(
            f"{settings.AUTH_SERVER_URL}/token/verify",
            json={"token": token},
            headers={"Authorization": f"Bearer {token}"},
            timeout=5
        )
        if response.status_code == 200:
            res_data = response.json()
            if res_data.get("success"):
                return res_data.get("data", {}).get("user_id")
    except Exception:
        pass
    return None

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_from_header()
        if not token:
            return ResponseBuilder.error(
                code="UNAUTHORIZED",
                message="Token de acesso ausente ou inválido.",
                status_code=401
            )
        
        user_id = verify_token_locally(token)
        if not user_id:
            user_id = verify_token_remotely(token)
            
        if not user_id:
            return ResponseBuilder.error(
                code="UNAUTHORIZED",
                message="Token inválido ou expirado.",
                status_code=401
            )
            
        g.user_id = user_id
        return f(*args, **kwargs)
    return decorated
