import time
from infra.config.db import engine
from infra.models.user_model import Base

def init_db():
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
