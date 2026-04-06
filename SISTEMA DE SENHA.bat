@echo off
setlocal enabledelayedexpansion

REM Configurar tratamento de erro global e caminhos basicos
set "ERROR_OCCURRED=0"
set "PYTHON_CMD="
set "VENV_PY=venv\Scripts\python.exe"
set "VENV_PIP=venv\Scripts\pip.exe"
set "VENV_EXISTS=0"

REM Configurar codificação UTF-8 e título
chcp 65001 >nul 2>&1
title Sistema de Senhas - Tudo em Um

REM Garantir que estamos no diretório correto
cd /d "%~dp0" 2>nul || (
    echo ERRO: Nao foi possivel mudar para o diretorio do script!
    pause
    exit /b 1
)

echo.
echo ========================================
echo    SISTEMA DE SENHAS - TUDO EM UM
echo ========================================
echo.
echo Diretorio atual: %CD%
echo.

REM Verificar se o ambiente virtual ja existe
if exist "%VENV_PY%" (
    set "VENV_EXISTS=1"
)

REM Verificar se o arquivo run.py existe
if not exist "run.py" (
    echo ERRO: Arquivo run.py nao encontrado!
    echo Certifique-se de que este arquivo BAT esta na pasta raiz do projeto.
    pause
    exit /b 1
)

REM Verificar se o arquivo requirements.txt existe
if not exist "requirements.txt" (
    echo ERRO: Arquivo requirements.txt nao encontrado!
    echo Certifique-se de que este arquivo BAT esta na pasta raiz do projeto.
    pause
    exit /b 1
)

echo [1/6] Verificando Python...

REM 1) Tentar o launcher do Windows (py -3)
py -3 --version >nul 2>&1 && set "PYTHON_CMD=py -3"

REM 2) Tentar python (PATH)
if not defined PYTHON_CMD (
    python --version >nul 2>&1 && set "PYTHON_CMD=python"
)

REM 3) Tentar python3 (PATH)
if not defined PYTHON_CMD (
    python3 --version >nul 2>&1 && set "PYTHON_CMD=python3"
)

if not defined PYTHON_CMD (
    echo ERRO: Python 3 nao encontrado no PATH.
    echo Instale o Python 3.11+ e marque a opcao "Add python.exe to PATH".
    echo Download: https://www.python.org/downloads/windows/
    pause
    exit /b 1
) else (
    echo Python detectado: %PYTHON_CMD%
)

echo [2/6] Verificando pip...
%PYTHON_CMD% -m pip --version >nul 2>&1
if errorlevel 1 (
    echo Instalando pip...
    %PYTHON_CMD% -m ensurepip --upgrade
    if errorlevel 1 (
        echo ERRO: Falha ao instalar pip!
        pause
        exit /b 1
    )
)

echo [3/6] Verificando ambiente virtual...
if "%VENV_EXISTS%"=="1" (
    echo Ambiente virtual ja existe. Nao sera recriado.
) else (
    REM Criar novo ambiente virtual
    echo Criando novo ambiente virtual...
    %PYTHON_CMD% -m venv venv
    if errorlevel 1 (
        echo ERRO: Falha ao criar ambiente virtual!
        echo Tentando novamente...
        timeout /t 5 /nobreak >nul
        %PYTHON_CMD% -m venv venv
        if errorlevel 1 (
            echo ERRO: Falha ao criar ambiente virtual novamente!
            pause
            exit /b 1
        )
    )
    echo Ambiente virtual criado com sucesso!
)

echo [4/6] Ativando ambiente virtual...
REM Verificar se o arquivo de ativação existe
if not exist "%VENV_PY%" (
    echo ERRO: Arquivo de ativacao nao encontrado!
    echo Verificando arquivos do ambiente virtual...
    if exist "venv\Scripts" (
        echo Arquivos encontrados:
        dir /b "venv\Scripts\*.bat" 2>nul
    )
    pause
    exit /b 1
)

REM Ativar o ambiente virtual
call "venv\Scripts\activate.bat" 2>nul
if errorlevel 1 (
    echo ERRO: Falha ao ativar ambiente virtual!
    echo Usando Python diretamente do ambiente virtual...
    set "PATH=%~dp0venv\Scripts;%PATH%"
) else (
    echo Ambiente virtual ativado com sucesso!
)

echo [5/6] Instalando dependencias...
if "%VENV_EXISTS%"=="1" (
    echo Ambiente virtual ja configurado anteriormente.
    echo Pulando instalacao completa de dependencias.
) else (
    echo Atualizando pip...
    if exist "%VENV_PY%" (
        echo Usando Python do ambiente virtual...
        "%VENV_PY%" -m pip install --upgrade pip --timeout 60 2>nul
        if errorlevel 1 (
            echo AVISO: Falha ao atualizar pip, continuando...
        )
    ) else (
        echo Usando Python global...
        %PYTHON_CMD% -m pip install --upgrade pip --timeout 60 2>nul
        if errorlevel 1 (
            echo AVISO: Falha ao atualizar pip, continuando...
        )
    )

    echo Instalando dependencias do requirements.txt...
    if exist "%VENV_PIP%" (
        echo Usando pip do ambiente virtual...
        echo Instalando todas as dependencias de uma vez...
        "%VENV_PIP%" install -r requirements.txt --timeout 120 2>nul
        if errorlevel 1 (
            echo AVISO: Primeira tentativa falhou. Tentando metodo alternativo...
            echo Instalando com --no-cache-dir...
            "%VENV_PIP%" install -r requirements.txt --no-cache-dir --timeout 120 2>nul
            if errorlevel 1 (
                echo AVISO: Metodo alternativo falhou. Instalando dependencias principais...
                echo Instalando Flask primeiro...
                "%VENV_PIP%" install Flask==3.1.0 --timeout 60 2>nul
                if errorlevel 1 (
                    echo ERRO: Falha ao instalar Flask!
                    echo Tentando sem versao especifica...
                    "%VENV_PIP%" install Flask --timeout 60 2>nul
                    if errorlevel 1 (
                        echo ERRO CRITICO: Flask nao conseguiu ser instalado!
                        pause
                        exit /b 1
                    )
                )
                
                echo Instalando outras dependencias principais...
                "%VENV_PIP%" install Flask-Login==0.6.3 --timeout 60 2>nul
                "%VENV_PIP%" install Flask-SQLAlchemy==3.1.1 --timeout 60 2>nul
                "%VENV_PIP%" install SQLAlchemy==2.0.40 --timeout 60 2>nul
                "%VENV_PIP%" install requests==2.32.3 --timeout 60 2>nul
                "%VENV_PIP%" install Werkzeug==3.1.3 --timeout 60 2>nul
                "%VENV_PIP%" install Jinja2==3.1.6 --timeout 60 2>nul
            ) else (
                echo Dependencias instaladas com sucesso usando metodo alternativo!
            )
        ) else (
            echo Dependencias instaladas com sucesso!
        )
        
        REM Verificar se Flask foi instalado
        echo.
        echo Verificando instalacao do Flask...
        "%VENV_PY%" -c "import flask; print('Flask instalado - Versao:', flask.__version__)" 2>nul || (
            echo ERRO: Flask nao foi instalado! Tentando instalacao manual...
            "%VENV_PIP%" install flask flask-login flask-sqlalchemy sqlalchemy werkzeug jinja2 requests reportlab pandas openpyxl psutil --force-reinstall 2>nul
        )
        
        REM Verificar se requests foi instalado
        echo Verificando instalacao do requests...
        "%VENV_PY%" -c "import requests; print('Requests instalado - Versao:', requests.__version__)" 2>nul || (
            echo AVISO: Requests nao foi instalado! Tentando instalacao manual...
            "%VENV_PIP%" install requests --force-reinstall 2>nul
        )
        
        REM Verificar se pandas foi instalado
        echo Verificando instalacao do pandas...
        "%VENV_PY%" -c "import pandas; print('Pandas instalado - Versao:', pandas.__version__)" 2>nul || (
            echo AVISO: Pandas nao foi instalado! Tentando instalacao final...
            "%VENV_PIP%" install pandas --force-reinstall --no-cache-dir 2>nul
        )
    ) else (
        echo Usando pip global...
        echo Instalando dependencias do requirements.txt...
        %PYTHON_CMD% -m pip install -r requirements.txt --timeout 120 2>nul
        if errorlevel 1 (
            echo AVISO: Falha ao instalar do requirements.txt. Tentando metodo alternativo...
            %PYTHON_CMD% -m pip install -r requirements.txt --no-cache-dir --timeout 120 2>nul
            if errorlevel 1 (
                echo AVISO: Metodo alternativo falhou. Instalando dependencias principais...
                %PYTHON_CMD% -m pip install Flask==3.1.0 --timeout 60 2>nul
                %PYTHON_CMD% -m pip install Flask-Login==0.6.3 --timeout 60 2>nul
                %PYTHON_CMD% -m pip install Flask-SQLAlchemy==3.1.1 --timeout 60 2>nul
                %PYTHON_CMD% -m pip install SQLAlchemy==2.0.40 --timeout 60 2>nul
                %PYTHON_CMD% -m pip install requests==2.32.3 --timeout 60 2>nul
                %PYTHON_CMD% -m pip install Werkzeug==3.1.3 --timeout 60 2>nul
                %PYTHON_CMD% -m pip install Jinja2==3.1.6 --timeout 60 2>nul
            )
        )
    )
)

echo [6/6] Verificacao final...
REM Verificar se tudo está instalado
if exist "%VENV_PY%" (
    echo Testando Flask...
    "%VENV_PY%" -c "import flask; print('Flask: OK')" 2>nul || (
        echo ERRO: Flask nao esta funcionando!
        echo Tentando reinstalar Flask...
        "%VENV_PIP%" install flask --force-reinstall 2>nul
        "%VENV_PY%" -c "import flask; print('Flask: OK')" 2>nul || (
            echo ERRO CRITICO: Flask nao conseguiu ser instalado!
            pause
            exit /b 1
        )
    )
    
    echo Testando Flask-SQLAlchemy...
    "%VENV_PY%" -c "import flask_sqlalchemy; print('Flask-SQLAlchemy: OK')" 2>nul || (
        echo AVISO: Flask-SQLAlchemy nao esta funcionando, mas continuando...
    )
    
    echo Testando SQLAlchemy...
    "%VENV_PY%" -c "import sqlalchemy; print('SQLAlchemy: OK')" 2>nul || (
        echo AVISO: SQLAlchemy nao esta funcionando, mas continuando...
    )
    
    echo Testando requests...
    "%VENV_PY%" -c "import requests; print('Requests: OK')" 2>nul || (
        echo AVISO: Requests nao esta funcionando, mas continuando...
    )
    
    echo Testando reportlab...
    "%VENV_PY%" -c "import reportlab; print('ReportLab: OK')" 2>nul || (
        echo AVISO: ReportLab nao esta funcionando, mas continuando...
    )
    
    echo Testando pandas...
    "%VENV_PY%" -c "import pandas; print('Pandas: OK')" 2>nul || (
        echo AVISO: Pandas nao esta funcionando, mas continuando...
        echo O sistema pode funcionar sem pandas para algumas funcionalidades.
    )
) else (
    echo Testando com Python global...
    %PYTHON_CMD% -c "import flask; print('Flask: OK')" 2>nul || (
        echo ERRO: Flask nao esta funcionando!
        pause
        exit /b 1
    )
    
    %PYTHON_CMD% -c "import flask_sqlalchemy; print('Flask-SQLAlchemy: OK')" 2>nul || (
        echo AVISO: Flask-SQLAlchemy nao esta funcionando, mas continuando...
    )
    
    %PYTHON_CMD% -c "import sqlalchemy; print('SQLAlchemy: OK')" 2>nul || (
        echo AVISO: SQLAlchemy nao esta funcionando, mas continuando...
    )
    
    %PYTHON_CMD% -c "import requests; print('Requests: OK')" 2>nul || (
        echo AVISO: Requests nao esta funcionando, mas continuando...
    )
    
    %PYTHON_CMD% -c "import reportlab; print('ReportLab: OK')" 2>nul || (
        echo AVISO: ReportLab nao esta funcionando, mas continuando...
    )
    
    %PYTHON_CMD% -c "import pandas; print('Pandas: OK')" 2>nul || (
        echo AVISO: Pandas nao esta funcionando, mas continuando...
        echo O sistema pode funcionar sem pandas para algumas funcionalidades.
    )
)

echo.
echo ========================================
echo    TUDO PRONTO! INICIANDO SISTEMA
echo ========================================
echo.
echo O sistema sera iniciado em: http://localhost:5003
echo.
echo Para acessar o sistema:
echo 1. Abra seu navegador
echo 2. Digite: http://localhost:5003
echo.
echo Para parar o servidor, pressione Ctrl+C
echo.

REM Aguardar um pouco antes de iniciar
timeout /t 3 /nobreak >nul

REM Limpar a tela e iniciar o servidor
cls
echo ========================================
echo    SISTEMA DE SENHAS - RODANDO
echo ========================================
echo.
echo Iniciando servidor Flask...
echo.
echo URL: http://localhost:5003
echo.
echo Pressione Ctrl+C para parar o servidor
echo.

REM Garantir que estamos no diretório correto
cd /d "%~dp0" 2>nul

REM Iniciar o servidor Flask
if exist "%VENV_PY%" (
    "%VENV_PY%" run.py
) else (
    %PYTHON_CMD% run.py
)

REM Se chegou aqui, houve algum erro ou o servidor foi encerrado
echo.
echo ========================================
echo    SERVIDOR ENCERRADO
echo ========================================
echo.
echo O servidor foi encerrado.
echo.
echo Para reiniciar, execute este arquivo novamente.
echo.
pause
