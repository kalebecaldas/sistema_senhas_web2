@echo off
chcp 65001 >nul
title Sistema IAAM

REM Garantir que estamos no diretório correto
cd /d "%~dp0"

echo 🚀 Sistema de Senhas IAAM
echo ================================
echo.

REM Verificar estrutura básica
if not exist "run.py" (
    echo ❌ Arquivo run.py nao encontrado!
    echo 📝 Certifique-se de estar na pasta correta do projeto
    pause
    exit /b 1
)

if not exist "app" (
    echo ❌ Pasta 'app' nao encontrada!
    echo 📝 Execute este arquivo na pasta principal do projeto IAAM
    pause
    exit /b 1
)

echo ✅ Estrutura do projeto detectada
echo.

REM Verificar ambiente virtual
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Ambiente virtual nao encontrado!
    echo.
    echo 💡 SOLUCOES:
    echo 📦 Execute: instalar_sistema.bat
    echo 🔧 Execute: atualizar_sistema_completo.bat
    echo 📝 Manual: python -m veanv venv
    echo.
    set /p SETUP="Executar instalacao automatica agora? (S/N): "
    if /i not "%SETUP%"=="S" (
        echo ℹ️  Instalacao cancelada
        pause
        exit /b 1
    ) else (
        instalar_sistema.bat
        if errorlevel 1 (
            echo ❌ Falha na instalacao automatica
            pause
            exit /b 1
        )
    )
)

REM Ativar ambiente virtual silenciosamente
echo 🔧 Ativando ambiente virtual...
call venv\Scripts\activate.bat 2>nul

REM Verificação rápida de dependências
echo 📦 Verificando dependencias...
python -c "import flask, sqlalchemy" 2>nul
if errorlevel 1 (
    echo ⚠️  Algumas dependencias podem estar faltando
    echo.
    echo 💡 SOLUCOES:
    echo 📦 Execute: pip install -r requirements.txt
    echo 🔧 Execute: atualizar_sistema_completo.bat
    echo.
    set /p INSTALL="Instalar dependencias agora? (S/N): "
    if /i "%INSTALL%"=="S" (
        echo 📥 Instalando dependencias...
        pip install -r requirements.txt --quiet
        if errorlevel 1 (
            echo ❌ Falha na instalacao de dependencias!
            pause
            exit /b 1
        ) else (
            echo ✅ Dependencias instaladas!
        )
    ) else (
        echo ℹ️  Continuando sem instalar dependencias...
        echo ⚠️  Se houver erro, instale as dependencias primeiro
    )
)

echo.
echo 🌐 INICIANDO SERVIDOR FLASK...
echo ================================
echo.
echo 📍 URL Principal: http://localhost:5003
echo 📍 URL Alt.: http://127.0.0.1:5003
echo 📍 Acesso Rede: http://192.168.0.98:5003
echo.
echo ⏹️  Para parar: Ctrl+C
echo ℹ️  Para atualizar: atualizar_sistema_completo.bat
echo ================================
echo.

REM Iniciar o servidor
python run.py

echo.
echo Servidor encerrado.
echo Pressione qualquer tecla...
pause >nul 