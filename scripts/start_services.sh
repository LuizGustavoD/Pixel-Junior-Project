#!/bin/bash

# Change directory to script's directory and then to root
cd "$(dirname "$0")/.."

echo "==================================================="
echo "  Pixel Driver - Inicializando Stack de Servicos"
echo "==================================================="
echo

# Verificar se o Docker está em execução
if ! docker info >/dev/null 2>&1; then
    echo "[ERRO] O Docker nao esta em execucao."
    echo "Certifique-se de iniciar o servico do Docker antes de prosseguir."
    echo
    exit 1
fi

# Detectar comando docker-compose ou docker compose
COMPOSE_CMD="docker compose"
if ! docker compose version >/dev/null 2>&1; then
    if docker-compose version >/dev/null 2>&1; then
        COMPOSE_CMD="docker-compose"
    else
        echo "[ERRO] Nem 'docker compose' nem 'docker-compose' foram encontrados."
        exit 1
    fi
fi

echo "[1/3] Iniciando build e execucao dos containers..."
$COMPOSE_CMD up -d --build
if [ $? -ne 0 ]; then
    echo
    echo "[ERRO] Falha ao subir os containers pelo Docker Compose."
    echo
    exit 1
fi

echo
echo "[2/3] Aguardando inicializacao e saude dos servicos..."
echo

# Loop simples de healthcheck para o banco MySQL
until [ "$(docker inspect --format='{{json .State.Health.Status}}' auth_mysql_db 2>/dev/null)" == "\"healthy\"" ]; do
    echo "Aguardando banco de dados ficar saudavel..."
    sleep 3
done

echo
echo "[OK] Banco de dados ativo e saudavel!"
echo
echo "[3/3] Reiniciando containers de backend para sincronizar schemas..."
docker restart auth_server_app resurce_server_app >/dev/null

echo
echo "==================================================="
echo "  Stack Pixel Driver iniciada com sucesso!"
echo "==================================================="
echo
echo "  * Frontend: http://localhost:3000"
echo "  * Auth Server API: http://localhost:5000"
echo "  * Resource Server API: http://localhost:5001"
echo
echo "Para derrubar os servicos, execute: ./scripts/stop_services.sh"
echo
