from flask import Blueprint, request, g, Response, send_file
from infra.config.db import SessionLocal
from infra.repository.mysql_file_repository import MySQLFileRepository
from infra.storage.local_storage_service import LocalStorageService
from infra.security.auth_middleware import login_required
from application.use_cases.user_upload_file import UserUploadFileUseCase
from application.use_cases.user_get_file import UserGetFileUseCase
from application.use_cases.user_delete_file import UserDeleteFileUseCase
from application.use_cases.user_list_files import UserListFilesUseCase
from application.use_cases.user_get_thumbnail import UserGetThumbnailUseCase
from application.validators.upload_file import UploadFileValidator
from application.validators.delete_file import DeleteFileValidator
from application.dtos.response.file_dto import FileResponseDTO
from infra.http.response_builder import ResponseBuilder

file_bp = Blueprint("files", __name__, url_prefix="/files")

@file_bp.route("/status", methods=["GET"])
@login_required
def files_status():
    return ResponseBuilder.success(
        data={
            "authenticated_user_id": g.user_id
        },
        message="Serviço de arquivos autenticado."
    )

@file_bp.route("", methods=["GET"])
@login_required
def list_files():
    db = SessionLocal()
    try:
        file_repo = MySQLFileRepository(db)
        use_case = UserListFilesUseCase(file_repo)
        
        files = use_case.execute(g.user_id)
        
        return ResponseBuilder.success(
            data=FileResponseDTO.to_list(files),
            message="Arquivos recuperados com sucesso."
        )
    finally:
        db.close()

@file_bp.route("/thumbnail/<file_id>", methods=["GET"])
@login_required
def get_thumbnail(file_id):
    db = SessionLocal()
    try:
        file_repo = MySQLFileRepository(db)
        storage_service = LocalStorageService()
        use_case = UserGetThumbnailUseCase(file_repo, storage_service)
        
        thumb_io, content_type = use_case.execute(file_id, g.user_id)
        
        return send_file(thumb_io, mimetype=content_type)
    finally:
        db.close()

@file_bp.route("/upload", methods=["POST"])
@login_required
def upload_file():
    if "file" not in request.files:
        return ResponseBuilder.error(code="VALIDATION_ERROR", message="Nenhum arquivo enviado.", status_code=400)
    
    file = request.files["file"]
    
    # Determine file size
    file.seek(0, 2)
    size = file.tell()
    file.seek(0)

    UploadFileValidator.validate(file, file.filename, size)

    db = SessionLocal()
    try:
        owner_username = None
        try:
            from sqlalchemy import text
            owner_username = db.execute(
                text("SELECT username FROM users WHERE id = :owner_id"),
                {"owner_id": g.user_id}
            ).scalar()
        except Exception:
            pass

        file_repo = MySQLFileRepository(db)
        storage_service = LocalStorageService()
        use_case = UserUploadFileUseCase(file_repo, storage_service)

        saved_file = use_case.execute(
            file_stream=file,
            filename=file.filename,
            content_type=file.content_type or "application/octet-stream",
            size=size,
            owner_id=g.user_id,
            owner_username=owner_username
        )

        return ResponseBuilder.success(
            data=FileResponseDTO.to_dict(saved_file),
            message="Arquivo enviado com sucesso.",
            status_code=201
        )
    finally:
        db.close()

@file_bp.route("/download/<file_id>", methods=["GET"])
@login_required
def download_file(file_id):
    db = SessionLocal()
    try:
        file_repo = MySQLFileRepository(db)
        storage_service = LocalStorageService()
        use_case = UserGetFileUseCase(file_repo, storage_service)

        metadata, generator = use_case.execute(file_id, g.user_id)

        response = Response(generator, content_type=metadata.content_type)
        response.headers["Content-Disposition"] = f"attachment; filename={metadata.original_name}"
        response.headers["Content-Length"] = metadata.size
        return response
    finally:
        db.close()

@file_bp.route("/delete/<file_id>", methods=["DELETE"])
@login_required
def delete_file(file_id):
    DeleteFileValidator.validate(file_id)
    
    db = SessionLocal()
    try:
        file_repo = MySQLFileRepository(db)
        storage_service = LocalStorageService()
        use_case = UserDeleteFileUseCase(file_repo, storage_service)

        use_case.execute(file_id, g.user_id)

        return ResponseBuilder.success(
            message="Arquivo deletado com sucesso.",
            status_code=200
        )
    finally:
        db.close()
