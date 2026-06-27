from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

class User:
  id: UUID
  email: str
  username: str
  password: str
  created_at: datetime
  updated_at: datetime

  def __init__(self, id: UUID, email: str, username: str, password: str, created_at: datetime, updated_at: datetime):
    self.id = id
    self.email = email
    self.username = username
    self.password = password
    self.created_at = created_at
    self.updated_at = updated_at