class UserLoginRequestDTO:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

    @staticmethod
    def from_dict(data: dict) -> 'UserLoginRequestDTO':
        if not data:
            return UserLoginRequestDTO(None, None)
        return UserLoginRequestDTO(
            email=data.get('email'),
            password=data.get('password')
        )
    
    @staticmethod
    def to_dict(dto: 'UserLoginRequestDTO') -> dict:
        return {
            'email': dto.email,
            'password': dto.password
        }