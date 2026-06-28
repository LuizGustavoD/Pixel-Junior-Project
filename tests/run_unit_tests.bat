@echo off
setlocal enabledelayedexpansion

:: Navegar para o diretorio raiz do projeto
cd /d "%~dp0\.."

:: Garantir existencia do ambiente virtual para o Auth Server
if not exist "auth_server\.venv\" (
    echo [SETUP] Criando ambiente virtual para Auth Server...
    python -m venv auth_server\.venv
    if !errorlevel! neq 0 (
        echo [ERRO] Falha ao criar virtualenv do Auth Server!
        exit /b !errorlevel!
    )
    echo [SETUP] Instalando dependencias do Auth Server...
    call auth_server\.venv\Scripts\pip install -r auth_server\requirements.txt >nul
)

:: Garantir existencia do ambiente virtual para o Resource Server
if not exist "resurce_server\.venv\" (
    echo [SETUP] Criando ambiente virtual para Resource Server...
    python -m venv resurce_server\.venv
    if !errorlevel! neq 0 (
        echo [ERRO] Falha ao criar virtualenv do Resource Server!
        exit /b !errorlevel!
    )
    echo [SETUP] Instalando dependencias do Resource Server...
    call resurce_server\.venv\Scripts\pip install -r resurce_server\requirements.txt >nul
)

echo ===================================================
echo [1/4] Executando Testes Unitarios do Auth Server...
echo ===================================================
call .\auth_server\.venv\Scripts\python -m unittest discover -s auth_server/tests -p "*.py"
if %ERRORLEVEL% neq 0 (
    echo [ERRO] Testes unitarios do Auth Server falharam!
    exit /b %ERRORLEVEL%
)

echo ===================================================
echo [2/4] Executando Testes Unitarios do Resource Server...
echo ===================================================
call .\resurce_server\.venv\Scripts\python -m unittest discover -s resurce_server/tests -p "*.py"
if %ERRORLEVEL% neq 0 (
    echo [ERRO] Testes unitarios do Resource Server falharam!
    exit /b %ERRORLEVEL%
)

echo ===================================================
echo [3/4] Inicializando Servicos via Docker Compose...
echo ===================================================
docker compose up -d --build
if %ERRORLEVEL% neq 0 (
    echo [ERRO] Falha ao subir os servicos no Docker!
    exit /b %ERRORLEVEL%
)

echo ===================================================
echo [4/4] Executando Testes de Integracao...
echo ===================================================
call .\resurce_server\.venv\Scripts\python -m unittest tests/test_integration.py
set INTEGRATION_ERR=%ERRORLEVEL%

echo ===================================================
echo Finalizando e desligando os containers Docker...
echo ===================================================
docker compose down -v

if %INTEGRATION_ERR% neq 0 (
    echo [ERRO] Testes de integracao falharam com codigo %INTEGRATION_ERR%!
    exit /b %INTEGRATION_ERR%
)

echo ===================================================
echo [SUCESSO] Todos os testes passaram com exito!
echo ===================================================
exit /b 0
