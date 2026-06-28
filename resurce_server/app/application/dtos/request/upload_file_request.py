from dataclasses import dataclass
from uuid import UUID

@dataclass
class UploadFileRequest:
    owner_id: UUID
    original_name: str
    content_type: str
    size: int
    content: bytes