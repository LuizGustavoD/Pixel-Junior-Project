from domain.entities.file import File

class FileResponseDTO:
    @staticmethod
    def to_dict(file: File) -> dict:
        return {
            "id": str(file.id),
            "original_name": file.original_name,
            "content_type": file.content_type,
            "size": file.size,
            "created_at": file.created_at.isoformat()
        }

    @staticmethod
    def to_list(files: list[File]) -> list[dict]:
        return [FileResponseDTO.to_dict(f) for f in files]
