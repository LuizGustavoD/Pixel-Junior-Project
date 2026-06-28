@echo off
title Pixel Driver — Inicializando Serviços
echo ===================================================
echo   Pixel Driver - Inicializando Stack de Servicos
echo ===================================================
echo.

:: Verificar se o Docker está em execução
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] O Docker nao esta em execucao. 
    echo Certifique-se de iniciar o Docker Desktop antes de executar este script.
    echo.
    pause
    exit /b 1
)

:: Desabilitar BuildKit temporariamente para evitar conflitos com OneDrive no Windows
set DOCKER_BUILDKIT=0

echo [1/3] Iniciando build e execucao dos containers...
cd ..
docker compose up -d --build
if %errorlevel% neq 0 (
    echo.
    echo [ERRO] Falha ao subir os containers pelo Docker Compose.
    echo.
    pause
    exit /b 1
)

echo.
echo [2/3] Aguardando inicializacao e saude dos servicos...
echo.

:: Loop simples de healthcheck para o banco MySQL
:health_loop
echo Aguardando banco de dados ficar saudavel...
docker inspect --format="{{json .State.Health.Status}}" auth_mysql_db 2>nul | findstr /i "healthy" >nul
if %errorlevel% neq 0 (
    timeout /t 3 /nobreak >nul
    goto health_loop
)

echo.
echo [OK] Banco de dados ativo e saudavel!
echo.
echo [3/3] Reiniciando containers de backend para sincronizar schemas...
docker restart auth_server_app resurce_server_app >nul

echo.
echo ===================================================
echo   Stack Pixel Driver iniciada com sucesso!
echo ===================================================
echo.
echo   * Frontend: http://localhost:3000
echo   * Auth Server API: http://localhost:5000
echo   * Resource Server API: http://localhost:5001
echo.
echo Para derrubar os servicos, execute o script: stop_services.bat
echo.
pause
