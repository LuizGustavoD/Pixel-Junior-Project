import os
import sys
from flask import Flask
from flask_cors import CORS

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from infra.config.db import engine
from infra.models.user_model import Base

from infra.http.routes.authentication_routes import auth_bp
from infra.http.routes.status_routes import status_bp
from infra.http.routes.token_routes import token_bp
from infra.http.error_handler import register_error_handlers

import time

for attempt in range(10):
    try:
        print(f"Criando tabelas no banco de dados se não existirem (tentativa {attempt + 1}/10)...")
        Base.metadata.create_all(bind=engine)
        print("Tabelas verificadas/criadas com sucesso!")
        break
    except Exception as e:
        print(f"Erro ao inicializar o banco de dados (tentativa {attempt + 1}/10): {e}")
        if attempt < 9:
            time.sleep(3)
        else:
            print("Falha definitiva ao inicializar o banco de dados. Continuando inicialização da aplicação...")


app = Flask(__name__)
CORS(app)

register_error_handlers(app)

app.register_blueprint(auth_bp)
app.register_blueprint(status_bp)
app.register_blueprint(token_bp)

@app.route("/health", methods=["GET"])
def health_check():
    return {"status": "healthy"}, 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
