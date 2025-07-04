@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo    Sistema de Senhas IAAM - Instalação Rápida
echo ========================================
echo.

:: Definir variáveis
set "REPO_URL=https://github.com/seu-usuario/sistema_senhas_web2.git"
set "PROJECT_DIR=sistema_senhas_web2"

:: Verificar se Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python não encontrado!
    echo 💡 Execute "instalar_sistema.bat" para instalação completa
    pause
    exit /b 1
)

:: Verificar se Git está instalado
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git não encontrado!
    echo 💡 Execute "instalar_sistema.bat" para instalação completa
    pause
    exit /b 1
)

echo ✅ Python e Git encontrados
echo.

:: Clonar ou atualizar repositório
if exist "%PROJECT_DIR%" (
    echo 📁 Atualizando projeto existente...
    cd %PROJECT_DIR%
    git pull origin main
    if %errorlevel% neq 0 (
        echo ⚠️ Erro ao atualizar, clonando novamente...
        cd ..
        rmdir /s /q %PROJECT_DIR%
        git clone %REPO_URL% %PROJECT_DIR%
    )
) else (
    echo 📥 Baixando projeto...
    git clone %REPO_URL% %PROJECT_DIR%
)

if %errorlevel% neq 0 (
    echo ❌ Erro ao baixar projeto
    pause
    exit /b 1
)

:: Entrar no diretório
cd %PROJECT_DIR%

:: Criar ambiente virtual se não existir
if not exist "venv" (
    echo 🔧 Criando ambiente virtual...
    python -m venv venv
)

:: Ativar ambiente virtual
echo 🔧 Ativando ambiente virtual...
call venv\Scripts\activate.bat

:: Instalar dependências
echo 📦 Instalando dependências...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ❌ Erro ao instalar dependências
    pause
    exit /b 1
)

:: Configurar banco
echo 🗄️ Configurando banco de dados...
python recriar_banco.py

:: Criar script de inicialização
echo 🚀 Criando script de inicialização...

(
echo @echo off
echo chcp 65001 ^>nul
echo echo ========================================
echo echo    Sistema de Senhas IAAM
echo echo ========================================
echo echo.
echo echo 🔧 Iniciando sistema...
echo echo.
echo cd /d "%~dp0%PROJECT_DIR%"
echo call venv\Scripts\activate.bat
echo python run.py
echo pause
) > "..\Iniciar Sistema.bat"

:: Criar atalho no desktop
copy "..\Iniciar Sistema.bat" "%USERPROFILE%\Desktop\Sistema de Senhas IAAM.bat" >nul 2>&1

echo.
echo ========================================
echo    ✅ Instalação Concluída!
echo ========================================
echo.
echo 📁 Sistema instalado em: %CD%
echo 🌐 Acesse: http://localhost:5003
echo 👤 Usuário padrão: admin
echo 🔑 Senha padrão: admin123
echo.
echo 🚀 Para iniciar o sistema:
echo    1. Execute "Iniciar Sistema.bat" ou
echo    2. Clique no atalho no desktop
echo.

:: Perguntar se quer iniciar agora
set /p "start_now=Deseja iniciar o sistema agora? (s/n): "
if /i "%start_now%"=="s" (
    echo.
    echo 🚀 Iniciando sistema...
    python run.py
) else (
    echo.
    echo ✅ Instalação concluída! Execute "Iniciar Sistema.bat" quando quiser usar o sistema.
)

pause 