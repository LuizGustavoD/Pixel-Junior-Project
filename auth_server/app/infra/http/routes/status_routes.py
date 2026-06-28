from flask import Blueprint
from infra.http.response_builder import ResponseBuilder

status_bp = Blueprint("status", __name__)

@status_bp.route("/status", methods=["GET"])
def api_status():
    return ResponseBuilder.success(
        data={"status": "healthy", "service": "auth_server"},
        message="Servidor de autenticação online."
    )
