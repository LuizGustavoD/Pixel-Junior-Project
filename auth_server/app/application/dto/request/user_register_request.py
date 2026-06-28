class UserRegisterRequestDTO:
    def __init__(self, email: str, username: str, password: str):
        self.email = email
        self.username = username
        self.password = password

    @staticmethod
    def from_dict(data: dict) -> 'UserRegisterRequestDTO':
        if not data:
            return UserRegisterRequestDTO(None, None, None)
        return UserRegisterRequestDTO(
            email=data.get('email'),
            username=data.get('username'),
            password=data.get('password')
        )
    
    @staticmethod
    def to_dict(dto: 'UserRegisterRequestDTO') -> dict:
        return {
            'email': dto.email,
            'username': dto.username,
            'password': dto.password
        }