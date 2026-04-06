@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

:: ============================================================================
:: 🚀 Instalador e Inicializador - Sistema de Senhas IAAM (Windows)
:: ============================================================================
:: Descrição: Configura ambiente, instala dependências e inicia o sistema
:: ============================================================================

title Sistema de Senhas IAAM - Instalador
cls

echo.
echo ============================================================================
echo   🏥 SISTEMA DE SENHAS IAAM - INSTALADOR WINDOWS
echo ============================================================================
echo.

:: 1. Verificar Python
echo 🔍 Verificando instalação do Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python não encontrado!
    echo ⚠️  Por favor, instale o Python 3.8 ou superior.
    echo 🔗 Baixe em: https://www.python.org/downloads/
    echo 📝 Marque a opção "Add Python to PATH" durante a instalação.
    pause
    exit /b 1
)
echo ✅ Python encontrado!
echo.

:: 2. Verificar/Criar Ambiente Virtual
echo 🔍 Verificando ambiente virtual...
if not exist "venv" (
    echo ⚙️  Criando ambiente virtual (pode demorar um pouco)...
    python -m venv venv
    if !errorlevel! neq 0 (
        echo ❌ Erro ao criar ambiente virtual.
        pause
        exit /b 1
    )
    echo ✅ Ambiente virtual criado!
) else (
    echo ✅ Ambiente virtual já existe.
)
echo.

:: 3. Ativar Ambiente e Instalar Dependências
echo 🔌 Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo 📦 Verificando/Instalando dependências...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Erro ao instalar dependências. Verifique sua conexão.
    pause
    exit /b 1
)
echo ✅ Dependências instaladas!
echo.

:: 4. Executar Migrações do Banco de Dados
echo 🔄 Verificando banco de dados...
python migrate_playlist.py
echo.

:: 5. Iniciar Servidor
cls
echo.
echo ============================================================================
echo   🏥 SISTEMA DE SENHAS IAAM - SERVIDOR RODANDO
echo ============================================================================
echo.
echo 📍 Acesso Local:
echo    http://127.0.0.1:5003
echo.
echo 📍 Acesso na Rede (Wi-Fi):
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr "IPv4"') do (
    set IP=%%a
    echo    http:!IP:~1!:5003
)
echo.
echo ⏹️  Para parar o servidor: Feche esta janela ou pressione Ctrl+C
echo.
echo 🌐 Abrindo sistema no navegador...
start http://127.0.0.1:5003

:: Inicia o servidor Flask
python run.py

pause
