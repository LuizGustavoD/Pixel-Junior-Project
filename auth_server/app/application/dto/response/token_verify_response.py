class TokenVerifyResponseDTO:
    def __init__(self, user_id: str):
        self.user_id = user_id

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id
        }
