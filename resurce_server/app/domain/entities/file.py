from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass
class File:
  id: UUID
  owner_id: UUID
  original_name: str
  storage_name: str
  content_type: str
  size: int
  created_at: datetime
  is_deleted: bool = False

  def belongs_to(self, user_id: UUID) -> bool:
      return self.owner_id == user_id

  @property
  def extension(self) -> str:
      return self.original_name.split(".")[-1].lower()