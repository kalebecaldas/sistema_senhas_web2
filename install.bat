@echo on
REM Definir o arquivo de log
set LOG_FILE=install_log.txt

REM Criar um novo arquivo de log ou limpar o arquivo existente
echo Iniciando a instalação... > %LOG_FILE%

REM Caminho para o instalador do Python que você já baixou manualmente
set INSTALLER=python-3.13.3-amd64.exe

REM Verificar se o arquivo do instalador existe
IF NOT EXIST "%INSTALLER%" (
    echo Instalador do Python não encontrado! Por favor, baixe o instalador e coloque na pasta do projeto. >> %LOG_FILE%
    echo Instalador do Python não encontrado! Por favor, baixe o instalador e coloque na pasta do projeto.
    exit /b
) else (
    echo Instalador encontrado! >> %LOG_FILE%
)

REM Verifica se o Python está instalado
echo Verificando a instalação do Python... >> %LOG_FILE%
python --version > nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python não encontrado! Instalando Python... >> %LOG_FILE%

    REM Executando o instalador do Python
    echo Iniciando o instalador do Python... >> %LOG_FILE%
    start /wait %INSTALLER% InstallAllUsers=1 PrependPath=1

    REM Verificar se o Python foi instalado corretamente
    python --version > nul 2>&1
    IF %ERRORLEVEL% NEQ 0 (
        echo Falha na instalação do Python. Por favor, instale manualmente. >> %LOG_FILE%
        echo Falha na instalação do Python. Por favor, instale manualmente.
        pause
        exit /b
    )
    echo Python instalado com sucesso! >> %LOG_FILE%

    REM Pausa para garantir que o terminal não feche automaticamente
    echo A instalação do Python foi concluída. Pressione qualquer tecla para continuar... >> %LOG_FILE%
    pause

    REM Reiniciar o terminal para garantir que o Python seja reconhecido
    exit /b
)

REM Continuar a instalação após reiniciar o terminal

REM Criar o ambiente virtual
echo Criando o ambiente virtual... >> %LOG_FILE%
python -m venv venv
IF %ERRORLEVEL% NEQ 0 (
    echo Erro ao criar o ambiente virtual. >> %LOG_FILE%
    exit /b
)

REM Ativar o ambiente virtual
echo Ativando o ambiente virtual... >> %LOG_FILE%
call venv\Scripts\activate

REM Instalar as dependências
echo Instalando as dependências... >> %LOG_FILE%
pip install -r requirements.txt
IF %ERRORLEVEL% NEQ 0 (
    echo Erro ao instalar as dependências. >> %LOG_FILE%
    exit /b
)

REM Verificar se o banco de dados já foi criado
echo Verificando se o banco de dados já foi inicializado... >> %LOG_FILE%
python -c "from app import db; print(db.engine.table_names())" >> %LOG_FILE%

REM Inicializar o banco de dados somente se não existir
echo Inicializando o banco de dados... >> %LOG_FILE%
python -c "from app import db; db.create_all()" >> %LOG_FILE% 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Erro ao inicializar o banco de dados. Detalhes do erro: >> %LOG_FILE%
    type %LOG_FILE%
    pause
    exit /b
)

REM Iniciar o servidor Flask
echo Iniciando o servidor Flask... >> %LOG_FILE%
python app.py
IF %ERRORLEVEL% NEQ 0 (
    echo Erro ao iniciar o servidor Flask. >> %LOG_FILE%
    exit /b
)

echo Instalação concluída com sucesso! >> %LOG_FILE%
pause
