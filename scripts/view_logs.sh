#!/bin/bash

echo "==================================================="
echo "  Pixel Driver - Visualizador de Logs do Docker"
echo "==================================================="
echo

# Verificar se o Docker está rodando
if ! docker info >/dev/null 2>&1; then
    echo "[ERRO] O Docker nao esta em execucao."
    exit 1
fi

echo "Escolha o container para visualizar os logs:"
echo "[1] Frontend (pixel_frontend_app)"
echo "[2] Auth Server (auth_server_app)"
echo "[3] Resource Server (resurce_server_app)"
echo "[4] Banco MySQL (auth_mysql_db)"
echo

read -p "Opcao (1-4): " choice

case $choice in
    1) CONTAINER="pixel_frontend_app" ;;
    2) CONTAINER="auth_server_app" ;;
    3) CONTAINER="resurce_server_app" ;;
    4) CONTAINER="auth_mysql_db" ;;
    *) echo "Opcao invalida." ; exit 1 ;;
esac

echo
echo "Escolha o modo de visualizacao:"
echo "[1] Ultimas 100 linhas"
echo "[2] Acompanhar logs em tempo real (-f)"
echo

read -p "Opcao (1-2): " mode

echo
echo "==================================================="
echo "  Exibindo logs de: $CONTAINER"
echo "  Pressione CTRL+C para sair do acompanhamento"
echo "==================================================="
echo

if [ "$mode" == "2" ]; then
    docker logs -f $CONTAINER
else
    docker logs --tail 100 $CONTAINER
fi
