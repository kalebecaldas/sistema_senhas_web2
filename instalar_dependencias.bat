@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo    Sistema de Senhas IAAM - Instalador
echo ========================================
echo.

:: Verificar se Python está instalado
echo 🔍 Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python não encontrado!
    echo 📥 Instalando Python...
    
    :: Verificar se o instalador do Python existe
    if exist "python-3.13.3-amd64.exe" (
        echo 🔧 Instalando Python 3.13.3...
        start /wait python-3.13.3-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
        if %errorlevel% neq 0 (
            echo ❌ Erro ao instalar Python
            echo 💡 Tente executar como administrador
            pause
            exit /b 1
        )
        echo ✅ Python instalado com sucesso!
    ) else (
        echo ❌ Instalador do Python não encontrado!
        echo 💡 Certifique-se de que o arquivo 'python-3.13.3-amd64.exe' está na mesma pasta
        pause
        exit /b 1
    )
    
    :: Recarregar PATH
    echo 🔄 Recarregando variáveis de ambiente...
    call refreshenv >nul 2>&1
    if %errorlevel% neq 0 (
        set "PATH=%PATH%;C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python313;C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python313\Scripts"
    )
) else (
    echo ✅ Python já está instalado
)

:: Verificar novamente se Python está funcionando
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python ainda não está funcionando
    echo 💡 Tente reiniciar o computador e executar novamente
    pause
    exit /b 1
)

echo ✅ Python funcionando corretamente
echo.

:: Criar ambiente virtual se não existir
if not exist "venv" (
    echo 🔧 Criando ambiente virtual...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ❌ Erro ao criar ambiente virtual
        pause
        exit /b 1
    )
    echo ✅ Ambiente virtual criado
) else (
    echo ✅ Ambiente virtual já existe
)

:: Ativar ambiente virtual
echo 🔧 Ativando ambiente virtual...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ❌ Erro ao ativar ambiente virtual
    pause
    exit /b 1
)

:: Atualizar pip
echo 📦 Atualizando pip...
python -m pip install --upgrade pip >nul 2>&1

:: Instalar dependências
echo 📦 Instalando dependências...
if exist "requirements.txt" (
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ Erro ao instalar dependências
        echo 💡 Verifique sua conexão com a internet
        pause
        exit /b 1
    )
    echo ✅ Dependências instaladas com sucesso!
) else (
    echo ❌ Arquivo requirements.txt não encontrado!
    echo 💡 Certifique-se de que o arquivo está na pasta do sistema
    pause
    exit /b 1
)

:: Configurar banco de dados
echo 🗄️ Configurando banco de dados...
if exist "recriar_banco.py" (
    python recriar_banco.py
    if %errorlevel% neq 0 (
        echo ⚠️ Erro ao configurar banco de dados, continuando...
    ) else (
        echo ✅ Banco de dados configurado
    )
) else (
    echo ⚠️ Script de banco não encontrado, pulando...
)

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
echo call venv\Scripts\activate.bat
echo python run.py
echo pause
) > "Iniciar Sistema.bat"

echo ✅ Script de inicialização criado
echo.

:: Mostrar informações finais
echo ========================================
echo    ✅ Instalação Concluída!
echo ========================================
echo.
echo 🌐 Para acessar o sistema:
echo    1. Execute "Iniciar Sistema.bat"
echo    2. Acesse: http://localhost:5003
echo    3. Usuário: admin
echo    4. Senha: admin123
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