from infra.config.settings import Settings

SECRET_KEY = Settings.SECRET_KEY

ALGORITHM = Settings.JWT_ALGORITHM

ACCESS_TOKEN_EXPIRE_MINUTES = Settings.JWT_EXPIRES_IN_MINUTES