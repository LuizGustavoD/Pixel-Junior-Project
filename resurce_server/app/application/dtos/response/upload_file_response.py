from dataclasses import dataclass
from uuid import UUID

@dataclass
class UploadFileResponse:
    id: UUID
    filename: str