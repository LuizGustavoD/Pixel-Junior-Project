from dataclasses import dataclass

@dataclass
class DeleteFileResponse:
    message: str
    file_id: str
