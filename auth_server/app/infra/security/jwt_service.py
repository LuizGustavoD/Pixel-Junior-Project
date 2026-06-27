import os
import jwt
from datetime import datetime, timedelta
from infra.config.settings import Settings
from domain.exceptions import InvalidCredentialsException


class JwtService:
    def __init__(self, settings=None):
        self.settings = settings if settings is not None else Settings()
        self.algorithm = self.settings.JWT_ALGORITHM
        self._private_key = None
        self._public_key = None
        
        if self.algorithm.startswith("RS"):
            self._load_keys()
        else:
            self._private_key = self.settings.SECRET_KEY
            self._public_key = self.settings.SECRET_KEY

    def _load_keys(self):
        if os.path.exists(self.settings.PRIVATE_KEY_PATH):
            with open(self.settings.PRIVATE_KEY_PATH, "r") as f:
                self._private_key = f.read()
        if os.path.exists(self.settings.PUBLIC_KEY_PATH):
            with open(self.settings.PUBLIC_KEY_PATH, "r") as f:
                self._public_key = f.read()

    def get_public_key(self):
        if self.algorithm.startswith("RS") and not self._public_key:
            self._load_keys()
        return self._public_key

    def create_access_token(self, user_id):
        if self.algorithm.startswith("RS") and not self._private_key:
            self._load_keys()
            if not self._private_key:
                raise ValueError("Chave privada para assinatura JWT não encontrada.")
                
        now = datetime.utcnow()
        expiration = now + timedelta(minutes=self.settings.JWT_EXPIRES_IN_MINUTES)
        payload = {
            "sub": str(user_id),
            "user_id": str(user_id),
            "exp": expiration,
            "iat": now
        }
        token = jwt.encode(payload, self._private_key, algorithm=self.algorithm)
        return token

    def decode_access_token(self, token):
        if self.algorithm.startswith("RS") and not self._public_key:
            self._load_keys()
            if not self._public_key:
                raise ValueError("Chave pública para verificação JWT não encontrada.")
                
        try:
            payload = jwt.decode(token, self._public_key, algorithms=[self.algorithm])
            return payload.get("user_id") or payload.get("sub")
        except jwt.ExpiredSignatureError:
            raise InvalidCredentialsException("Token expirado")
        except jwt.InvalidTokenError:
            raise InvalidCredentialsException("Token inválido")