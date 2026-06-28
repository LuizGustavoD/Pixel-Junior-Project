import os
import sys
from flask import Flask
from flask_cors import CORS

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from infra.config.db import engine, Base
from infra.http.routes.file_routes import file_bp
from infra.http.routes.status_route import status_bp
from infra.http.error_handler import register_error_handlers

import time

for attempt in range(10):
    try:
        print(f"Criando tabelas no banco de dados se não existirem (tentativa {attempt + 1}/10)...")
        Base.metadata.create_all(bind=engine)
        print("Tabelas de recursos verificadas/criadas com sucesso!")
        break
    except Exception as e:
        print(f"Erro ao inicializar o banco de dados de recursos (tentativa {attempt + 1}/10): {e}")
        if attempt < 9:
            time.sleep(3)
        else:
            print("Falha definitiva ao inicializar o banco de dados de recursos. Continuando inicialização da aplicação...")


app = Flask(__name__)
CORS(app)

register_error_handlers(app)

app.register_blueprint(file_bp)
app.register_blueprint(status_bp)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
