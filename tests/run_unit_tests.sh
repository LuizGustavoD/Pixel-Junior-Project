#!/bin/bash

# Navegar para o diretorio raiz do projeto
cd "$(dirname "$0")/.."

# Garantir existencia do ambiente virtual para o Auth Server
if [ ! -d "auth_server/.venv" ]; then
    echo "[SETUP] Criando ambiente virtual para Auth Server..."
    python3 -m venv auth_server/.venv
    if [ $? -ne 0 ]; then
        echo "[ERRO] Falha ao criar virtualenv do Auth Server!"
        exit 1
    fi
    echo "[SETUP] Instalando dependencias do Auth Server..."
    ./auth_server/.venv/bin/pip install -r auth_server/requirements.txt >/dev/null
fi

# Garantir existencia do ambiente virtual para o Resource Server
if [ ! -d "resurce_server/.venv" ]; then
    echo "[SETUP] Criando ambiente virtual para Resource Server..."
    python3 -m venv resurce_server/.venv
    if [ $? -ne 0 ]; then
        echo "[ERRO] Falha ao criar virtualenv do Resource Server!"
        exit 1
    fi
    echo "[SETUP] Instalando dependencias do Resource Server..."
    ./resurce_server/.venv/bin/pip install -r resurce_server/requirements.txt >/dev/null
fi

echo "==================================================="
echo "[1/4] Executando Testes Unitarios do Auth Server..."
echo "==================================================="
./auth_server/.venv/bin/python -m unittest discover -s auth_server/tests -p "*.py"
if [ $? -ne 0 ]; then
    echo "[ERRO] Testes unitarios do Auth Server falharam!"
    exit 1
fi

echo "==================================================="
echo "[2/4] Executando Testes Unitarios do Resource Server..."
echo "==================================================="
./resurce_server/.venv/bin/python -m unittest discover -s resurce_server/tests -p "*.py"
if [ $? -ne 0 ]; then
    echo "[ERRO] Testes unitarios do Resource Server falharam!"
    exit 1
fi

echo "==================================================="
echo "[3/4] Inicializando Servicos via Docker Compose..."
echo "==================================================="
docker compose up -d --build
if [ $? -ne 0 ]; then
    echo "[ERRO] Falha ao subir os servicos no Docker!"
    exit 1
fi

echo "==================================================="
echo "[4/4] Executando Testes de Integracao..."
echo "==================================================="
./resurce_server/.venv/bin/python -m unittest tests/test_integration.py
INTEGRATION_ERR=$?

echo "==================================================="
echo "Finalizando e desligando os containers Docker..."
echo "==================================================="
docker compose down -v

if [ $INTEGRATION_ERR -ne 0 ]; then
    echo "[ERRO] Testes de integracao falharam com codigo $INTEGRATION_ERR!"
    exit $INTEGRATION_ERR
fi

echo "==================================================="
echo "[SUCESSO] Todos os testes passaram com exito!"
echo "==================================================="
exit 0
