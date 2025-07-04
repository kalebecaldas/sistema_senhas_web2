@echo off
chcp 65001 >nul
title Teste do Sistema

REM Garantir que estamos no diretório correto
cd /d "%~dp0"

echo ========================================
echo    TESTE DO SISTEMA DE SENHAS
echo ========================================
echo.

echo [1] Verificando diretorio...
echo Diretorio atual: %CD%
echo.

echo [2] Verificando arquivos essenciais...
if exist "run.py" (
    echo run.py: OK
) else (
    echo run.py: NAO ENCONTRADO
)

if exist "requirements.txt" (
    echo requirements.txt: OK
) else (
    echo requirements.txt: NAO ENCONTRADO
)

if exist "app\__init__.py" (
    echo app\__init__.py: OK
) else (
    echo app\__init__.py: NAO ENCONTRADO
)

echo.

echo [3] Verificando Python...
python --version
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
) else (
    echo Python: OK
)

echo.

echo [4] Verificando ambiente virtual...
if exist "venv\Scripts\activate.bat" (
    echo Ambiente virtual: EXISTE
    call venv\Scripts\activate.bat
    echo Ambiente virtual: ATIVADO
) else (
    echo Ambiente virtual: NAO ENCONTRADO
)

echo.

echo [5] Verificando dependencias...
python -c "import flask; print('Flask:', flask.__version__)" 2>nul || echo Flask: NAO INSTALADO
python -c "import flask_sqlalchemy; print('Flask-SQLAlchemy: OK')" 2>nul || echo Flask-SQLAlchemy: NAO INSTALADO
python -c "import sqlalchemy; print('SQLAlchemy:', sqlalchemy.__version__)" 2>nul || echo SQLAlchemy: NAO INSTALADO

echo.

echo [6] Testando importacao do app...
python -c "from app import create_app; print('App: OK')" 2>nul || echo App: ERRO NA IMPORTACAO

echo.

echo [7] Testando execucao do run.py...
python -c "import run; print('run.py: OK')" 2>nul || echo run.py: ERRO NA EXECUCAO

echo.
echo ========================================
echo    TESTE CONCLUIDO
echo ========================================
echo.

if exist "venv\Scripts\activate.bat" (
    echo Para iniciar o sistema:
    echo 1. Execute: INICIAR_SISTEMA.bat
    echo.
) else (
    echo Para instalar e iniciar:
    echo 1. Execute: SISTEMA DE SENHA.bat
    echo.
)

pause 