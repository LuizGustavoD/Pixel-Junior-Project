from flask import Flask
from flask_cors import CORS

from infra.config.db_init import init_db
from infra.http.routes.file_routes import file_bp
from infra.http.routes.status_route import status_bp
from infra.http.error_handler import register_error_handlers

def create_app():
    # Initialize DB tables
    init_db()

    app = Flask(__name__)
    CORS(app)

    register_error_handlers(app)

    app.register_blueprint(file_bp)
    app.register_blueprint(status_bp)

    return app
