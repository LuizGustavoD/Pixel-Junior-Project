from dataclasses import dataclass

from resurce_server.app.application.dtos.file_response import FileResponse

@dataclass
class ListFilesResponse:
    files: list[FileResponse]