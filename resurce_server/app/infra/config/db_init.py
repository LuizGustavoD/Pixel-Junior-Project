import time
from infra.config.db import engine, Base

def init_db():
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
