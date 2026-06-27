FROM python:3.11-slim

WORKDIR /app

# Instala dependências do sistema necessárias para compilação (ex: bcrypt)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código fonte e recursos
COPY . .

# Porta exposta da aplicação
EXPOSE 5000

# Variáveis de ambiente padrão
ENV FLASK_APP=app/main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
ENV PYTHONUNBUFFERED=1

# Comando para rodar a aplicação
CMD ["python", "app/main.py"]
