from domain.exceptions import UserNotFoundException, InvalidCredentialsException

class LoginUserUseCase:
    def __init__(self, user_repository, password_hasher, jwt_manager):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.jwt_manager = jwt_manager

    def execute(self, credentials):
        user = self.user_repository.find_by_email(credentials['email'])
        if user is None:
            raise UserNotFoundException("Usuário não encontrado")

        if not self.password_hasher.verify(credentials['password'], user.password):
            raise InvalidCredentialsException("Senha incorreta")

        access_token = self.jwt_manager.create_access_token(user.id)
        return {"access_token": access_token}