class TokenVerifyRequestDTO:
    def __init__(self, token: str):
        self.token = token

    @staticmethod
    def from_dict(data: dict) -> 'TokenVerifyRequestDTO':
        if not data:
            return TokenVerifyRequestDTO(None)
        return TokenVerifyRequestDTO(
            token=data.get('token')
        )
