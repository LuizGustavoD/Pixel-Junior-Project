#!/bin/bash

# Change directory to script's directory and then to root
cd "$(dirname "$0")/.."

echo "==================================================="
echo "  Pixel Driver - Finalizando Stack de Servicos"
echo "==================================================="
echo

# Verificar se o Docker está em execução
if ! docker info >/dev/null 2>&1; then
    echo "[ERRO] O Docker nao esta em execucao."
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

echo "[1/1] Derrubando containers e limpando volumes..."
$COMPOSE_CMD down -v
if [ $? -ne 0 ]; then
    echo
    echo "[ERRO] Falha ao derrubar os servicos pelo Docker Compose."
    echo
    exit 1
fi

echo
echo "==================================================="
echo "  Servicos finalizados e limpos com sucesso!"
echo "==================================================="
echo
