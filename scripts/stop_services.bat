@echo off
title Pixel Driver — Finalizando Serviços
echo ===================================================
echo   Pixel Driver - Finalizando Stack de Servicos
echo ===================================================
echo.

:: Verificar se o Docker está em execução
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] O Docker nao esta em execucao.
    echo.
    pause
    exit /b 1
)

echo [1/1] Derrubando containers e limpando volumes...
cd ..
docker compose down -v
if %errorlevel% neq 0 (
    echo.
    echo [ERRO] Falha ao derrubar os servicos pelo Docker Compose.
    echo.
    pause
    exit /b 1
)

echo.
echo ===================================================
echo   Servicos finalizados e limpos com sucesso!
echo ===================================================
echo.
pause
