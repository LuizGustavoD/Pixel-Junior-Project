from flask import Flask
from flask_cors import CORS

from infra.config.db_init import init_db
from infra.http.routes.authentication_routes import auth_bp
from infra.http.routes.status_routes import status_bp
from infra.http.routes.token_routes import token_bp
from infra.http.error_handler import register_error_handlers

def create_app():
    # Initialize DB tables
    init_db()

    app = Flask(__name__)
    CORS(app)

    register_error_handlers(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(status_bp)
    app.register_blueprint(token_bp)

    @app.route("/health", methods=["GET"])
    def health_check():
        return {"status": "healthy"}, 200

    return app
