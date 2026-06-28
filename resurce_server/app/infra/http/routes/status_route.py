from flask import Blueprint, g
from infra.http.response_builder import ResponseBuilder
from infra.security.auth_middleware import login_required

status_bp = Blueprint("status", __name__, url_prefix="/health")

@status_bp.route("/status", methods=["GET"])
@login_required
def status_check():
    return ResponseBuilder.success(
        data={
            "status": "healthy",
            "authenticated_user_id": g.user_id,
            "service": "resource_server"
        },
        message="Servidor de recursos online e autenticado."
    )