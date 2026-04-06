@echo off
chcp 65001 > nul
setlocal

title Sistema de Senhas IAAM - Iniciando...
cls

echo.
echo ============================================================================
echo   🏥 INICIANDO SISTEMA DE SENHAS
echo ============================================================================
echo.

:: Verifica se foi instalado
if not exist "venv" (
    echo ❌ O sistema ainda não foi instalado!
    echo ⚠️  Por favor, execute o arquivo "instalador_windows.bat" primeiro.
    pause
    exit /b
)

:: Ativa e Inicia
echo 🔌 Ativando sistema...
call venv\Scripts\activate.bat

echo 🌐 Abrindo navegador...
start http://127.0.0.1:5003

echo 🚀 Servidor rodando...
echo 📍 Local: http://127.0.0.1:5003
echo ⏹️  Feche esta janela para encerrar.
echo.

python run.py

pause
