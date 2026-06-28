class PublicKeyResponseDTO:
    def __init__(self, public_key: str):
        self.public_key = public_key

    def to_dict(self) -> dict:
        return {
            "public_key": self.public_key
        }