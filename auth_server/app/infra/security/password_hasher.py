import bcrypt

class PasswordHasher:

    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    def hash(self, password: str) -> str:
        return self.hash_password(password)

    def verify(self, password: str, hashed_password: str) -> bool:
        return self.verify_password(password, hashed_password)