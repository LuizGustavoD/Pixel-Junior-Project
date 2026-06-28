from domain.entities.user import User


class UserResponseDTO:
    def __init__(self, user: User):
        self.id = str(user.id)
        self.email = user.email
        self.username = user.username
        self.created_at = user.created_at

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }