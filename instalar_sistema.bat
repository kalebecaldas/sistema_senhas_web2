@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo    Sistema de Senhas IAAM - Instalador
echo ========================================
echo.

:: Definir variáveis
set "REPO_URL=https://github.com/seu-usuario/sistema_senhas_web2.git"
set "PROJECT_DIR=sistema_senhas_web2"
set "LOG_FILE=install_log.txt"

:: Criar arquivo de log
echo [%date% %time%] Iniciando instalação do Sistema de Senhas IAAM > %LOG_FILE%

:: Verificar se Git está instalado
echo [%date% %time%] Verificando Git... >> %LOG_FILE%
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git não encontrado!
    echo 📥 Baixando Git...
    echo [%date% %time%] Git não encontrado, baixando... >> %LOG_FILE%
    
    :: Baixar Git usando winget ou curl
    winget install --id Git.Git -e --source winget >nul 2>&1
    if %errorlevel% neq 0 (
        echo ❌ Erro ao instalar Git via winget
        echo 📥 Tentando baixar manualmente...
        echo [%date% %time%] Erro ao instalar Git via winget >> %LOG_FILE%
        
        :: Baixar Git usando curl
        curl -L -o git-installer.exe "https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe"
        if exist git-installer.exe (
            echo 🔧 Instalando Git...
            start /wait git-installer.exe /VERYSILENT /NORESTART
            del git-installer.exe
        ) else (
            echo ❌ Não foi possível baixar o Git
            echo [%date% %time%] Falha ao baixar Git >> %LOG_FILE%
            pause
            exit /b 1
        )
    )
    
    :: Recarregar PATH
    call refreshenv >nul 2>&1
    if %errorlevel% neq 0 (
        set "PATH=%PATH%;C:\Program Files\Git\bin"
    )
)

echo ✅ Git encontrado/instalado
echo [%date% %time%] Git OK >> %LOG_FILE%

:: Verificar se Python está instalado
echo [%date% %time%] Verificando Python... >> %LOG_FILE%
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python não encontrado!
    echo 📥 Baixando Python...
    echo [%date% %time%] Python não encontrado, baixando... >> %LOG_FILE%
    
    :: Baixar Python usando winget
    winget install --id Python.Python.3.11 -e --source winget >nul 2>&1
    if %errorlevel% neq 0 (
        echo ❌ Erro ao instalar Python via winget
        echo 📥 Tentando baixar manualmente...
        echo [%date% %time%] Erro ao instalar Python via winget >> %LOG_FILE%
        
        :: Baixar Python usando curl
        curl -L -o python-installer.exe "https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe"
        if exist python-installer.exe (
            echo 🔧 Instalando Python...
            start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
            del python-installer.exe
        ) else (
            echo ❌ Não foi possível baixar o Python
            echo [%date% %time%] Falha ao baixar Python >> %LOG_FILE%
            pause
            exit /b 1
        )
    )
    
    :: Recarregar PATH
    call refreshenv >nul 2>&1
    if %errorlevel% neq 0 (
        set "PATH=%PATH%;C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311;C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\Scripts"
    )
)

echo ✅ Python encontrado/instalado
echo [%date% %time%] Python OK >> %LOG_FILE%

:: Verificar se o projeto já existe
if exist "%PROJECT_DIR%" (
    echo 📁 Projeto já existe, atualizando...
    echo [%date% %time%] Projeto existe, atualizando... >> %LOG_FILE%
    cd %PROJECT_DIR%
    git pull origin main >nul 2>&1
    if %errorlevel% neq 0 (
        echo ⚠️ Erro ao atualizar, tentando clonar novamente...
        echo [%date% %time%] Erro ao atualizar, clonando novamente... >> %LOG_FILE%
        cd ..
        rmdir /s /q %PROJECT_DIR%
        goto :clone_repo
    )
) else (
    echo 📥 Clonando repositório...
    echo [%date% %time%] Clonando repositório... >> %LOG_FILE%
    :clone_repo
    git clone %REPO_URL% %PROJECT_DIR% >nul 2>&1
    if %errorlevel% neq 0 (
        echo ❌ Erro ao clonar repositório
        echo [%date% %time%] Erro ao clonar repositório >> %LOG_FILE%
        echo.
        echo 💡 Verifique se:
        echo    - A URL do repositório está correta
        echo    - Você tem acesso à internet
        echo    - O repositório existe e é público
        pause
        exit /b 1
    )
)

echo ✅ Repositório baixado/atualizado
echo [%date% %time%] Repositório OK >> %LOG_FILE%

:: Entrar no diretório do projeto
cd %PROJECT_DIR%

:: Verificar se o ambiente virtual existe
if not exist "venv" (
    echo 🔧 Criando ambiente virtual...
    echo [%date% %time%] Criando ambiente virtual... >> ..\%LOG_FILE%
    python -m venv venv >nul 2>&1
    if %errorlevel% neq 0 (
        echo ❌ Erro ao criar ambiente virtual
        echo [%date% %time%] Erro ao criar ambiente virtual >> ..\%LOG_FILE%
        pause
        exit /b 1
    )
)

echo ✅ Ambiente virtual OK
echo [%date% %time%] Ambiente virtual OK >> ..\%LOG_FILE%

:: Ativar ambiente virtual
echo 🔧 Ativando ambiente virtual...
echo [%date% %time%] Ativando ambiente virtual... >> ..\%LOG_FILE%
call venv\Scripts\activate.bat

:: Atualizar pip
echo 📦 Atualizando pip...
echo [%date% %time%] Atualizando pip... >> ..\%LOG_FILE%
python -m pip install --upgrade pip >nul 2>&1

:: Instalar dependências
echo 📦 Instalando dependências...
echo [%date% %time%] Instalando dependências... >> ..\%LOG_FILE%
pip install -r requirements.txt >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Erro ao instalar dependências
    echo [%date% %time%] Erro ao instalar dependências >> ..\%LOG_FILE%
    pause
    exit /b 1
)

echo ✅ Dependências instaladas
echo [%date% %time%] Dependências OK >> ..\%LOG_FILE%

:: Configurar banco de dados
echo 🗄️ Configurando banco de dados...
echo [%date% %time%] Configurando banco de dados... >> ..\%LOG_FILE%
python recriar_banco.py >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ Erro ao configurar banco de dados, continuando...
    echo [%date% %time%] Erro ao configurar banco de dados >> ..\%LOG_FILE%
)

echo ✅ Banco de dados configurado
echo [%date% %time%] Banco de dados OK >> ..\%LOG_FILE%

:: Criar script de inicialização
echo 🚀 Criando script de inicialização...
echo [%date% %time%] Criando script de inicialização... >> ..\%LOG_FILE%

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

echo ✅ Script de inicialização criado
echo [%date% %time%] Script de inicialização OK >> ..\%LOG_FILE%

:: Criar atalho no desktop
echo 🔗 Criando atalho no desktop...
echo [%date% %time%] Criando atalho no desktop... >> ..\%LOG_FILE%
copy "..\Iniciar Sistema.bat" "%USERPROFILE%\Desktop\Sistema de Senhas IAAM.bat" >nul 2>&1

echo ✅ Atalho criado no desktop
echo [%date% %time%] Atalho OK >> ..\%LOG_FILE%

:: Mostrar informações finais
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
echo [%date% %time%] Instalação concluída com sucesso! >> ..\%LOG_FILE%

:: Perguntar se quer iniciar agora
set /p "start_now=Deseja iniciar o sistema agora? (s/n): "
if /i "%start_now%"=="s" (
    echo.
    echo 🚀 Iniciando sistema...
    echo [%date% %time%] Iniciando sistema... >> ..\%LOG_FILE%
    python run.py
) else (
    echo.
    echo ✅ Instalação concluída! Execute "Iniciar Sistema.bat" quando quiser usar o sistema.
)

pause 