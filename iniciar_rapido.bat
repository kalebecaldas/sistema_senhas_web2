@echo off
chcp 65001 >nul
title IAAM

REM Garantir que estamos no diretório correto
cd /d "%~dp0"

echo 🚀 Iniciando IAAM...

REM Verificação mínima
if not exist "run.py" (
    echo ❌ Erro: execute na pasta do projeto IAAM
    pause
    exit /b 1
)

if not exist "venv\Scripts\activate.bat" (
    echo ❌ Execute instalar_sistema.bat primeiro
    pause
    exit /b 1
)

REM Ativar venv e iniciar
call venv\Scripts\activate.bat 2>nul
echo 🌐 Servidor: http://localhost:5003
echo ⏹️  Para parar: Ctrl+C
echo.

python run.py
