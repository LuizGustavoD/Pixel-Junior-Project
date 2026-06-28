@echo off
title Pixel Driver — Inspeção de Containers
echo ===================================================
echo   Pixel Driver - Inspecao de Containers Docker
echo ===================================================
echo.

:: Verificar se o Docker está rodando
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] O Docker nao esta em execucao.
    pause
    exit /b 1
)

echo Escolha o container para inspecionar:
echo [1] Frontend (pixel_frontend_app)
echo [2] Auth Server (auth_server_app)
echo [3] Resource Server (resurce_server_app)
echo [4] Banco MySQL (auth_mysql_db)
echo.

set /p choice="Opcao (1-4): "

if "%choice%"=="1" set CONTAINER=pixel_frontend_app
if "%choice%"=="2" set CONTAINER=auth_server_app
if "%choice%"=="3" set CONTAINER=resurce_server_app
if "%choice%"=="4" set CONTAINER=auth_mysql_db

if "%CONTAINER%"=="" (
    echo Opcao invalida.
    pause
    exit /b 1
)

echo.
echo ===================================================
echo   Inspecionando dados de: %CONTAINER%
echo ===================================================
echo.

docker inspect %CONTAINER%

echo.
pause
