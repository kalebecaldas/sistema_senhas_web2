@echo off
setlocal enabledelayedexpansion

REM Configurar tratamento de erro global
set "ERROR_OCCURRED=0"

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
python --version >nul 2>&1
if errorlevel 1 (
    echo Python nao encontrado. Verificando instalador...
    if not exist "python-3.13.3-amd64.exe" (
        echo ERRO: Instalador do Python nao encontrado!
        echo Baixe o Python 3.13.3 e coloque na pasta raiz.
        pause
        exit /b 1
    )
    
    echo Instalando Python 3.13.3...
    echo Por favor, aguarde...
    
    REM Instalar Python silenciosamente
    python-3.13.3-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    if errorlevel 1 (
        echo ERRO: Falha na instalacao do Python!
        pause
        exit /b 1
    )
    
    REM Aguardar instalação
    timeout /t 30 /nobreak >nul
    
    REM Verificar se a instalação foi bem-sucedida
    python --version >nul 2>&1
    if errorlevel 1 (
        echo ERRO: Falha na instalacao do Python!
        echo Tente instalar manualmente executando: python-3.13.3-amd64.exe
        pause
        exit /b 1
    )
    echo Python instalado com sucesso!
) else (
    echo Python ja esta instalado.
)

echo [2/6] Verificando pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo Instalando pip...
    python -m ensurepip --upgrade
    if errorlevel 1 (
        echo ERRO: Falha ao instalar pip!
        pause
        exit /b 1
    )
)

echo [3/6] Recriando ambiente virtual...
REM Remover ambiente virtual existente
if exist "venv" (
    echo Removendo ambiente virtual atual...
    rmdir /s /q venv 2>nul
    if errorlevel 1 (
        echo AVISO: Nao foi possivel remover ambiente virtual completamente.
        echo Tentando continuar...
    )
)

REM Criar novo ambiente virtual
echo Criando novo ambiente virtual...
python -m venv venv
if errorlevel 1 (
    echo ERRO: Falha ao criar ambiente virtual!
    echo Tentando novamente...
    timeout /t 5 /nobreak >nul
    python -m venv venv
    if errorlevel 1 (
        echo ERRO: Falha ao criar ambiente virtual novamente!
        pause
        exit /b 1
    )
)
echo Ambiente virtual criado com sucesso!

echo [4/6] Ativando ambiente virtual...
REM Verificar se o arquivo de ativação existe
if not exist "venv\Scripts\activate.bat" (
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
echo Atualizando pip...
if exist "venv\Scripts\python.exe" (
    echo Usando Python do ambiente virtual...
    "venv\Scripts\python.exe" -m pip install --upgrade pip --timeout 60 2>nul
    if errorlevel 1 (
        echo AVISO: Falha ao atualizar pip, continuando...
    )
) else (
    echo Usando Python global...
    python -m pip install --upgrade pip --timeout 60 2>nul
    if errorlevel 1 (
        echo AVISO: Falha ao atualizar pip, continuando...
    )
)

echo Instalando dependencias do requirements.txt...
if exist "venv\Scripts\pip.exe" (
    echo Usando pip do ambiente virtual...
    echo Instalando todas as dependencias de uma vez...
    "venv\Scripts\pip.exe" install -r requirements.txt --timeout 120 2>nul
    if errorlevel 1 (
        echo AVISO: Primeira tentativa falhou. Tentando metodo alternativo...
        echo Instalando com --no-cache-dir...
        "venv\Scripts\pip.exe" install -r requirements.txt --no-cache-dir --timeout 120 2>nul
        if errorlevel 1 (
            echo AVISO: Metodo alternativo falhou. Instalando dependencias principais...
            echo Instalando Flask primeiro...
            "venv\Scripts\pip.exe" install Flask==3.1.0 --timeout 60 2>nul
            if errorlevel 1 (
                echo ERRO: Falha ao instalar Flask!
                echo Tentando sem versao especifica...
                "venv\Scripts\pip.exe" install Flask --timeout 60 2>nul
                if errorlevel 1 (
                    echo ERRO CRITICO: Flask nao conseguiu ser instalado!
                    pause
                    exit /b 1
                )
            )
            
            echo Instalando outras dependencias principais...
            "venv\Scripts\pip.exe" install Flask-Login==0.6.3 --timeout 60 2>nul
            "venv\Scripts\pip.exe" install Flask-SQLAlchemy==3.1.1 --timeout 60 2>nul
            "venv\Scripts\pip.exe" install SQLAlchemy==2.0.40 --timeout 60 2>nul
            "venv\Scripts\pip.exe" install requests==2.32.3 --timeout 60 2>nul
            "venv\Scripts\pip.exe" install Werkzeug==3.1.3 --timeout 60 2>nul
            "venv\Scripts\pip.exe" install Jinja2==3.1.6 --timeout 60 2>nul
        ) else (
            echo Dependencias instaladas com sucesso usando metodo alternativo!
        )
    ) else (
        echo Dependencias instaladas com sucesso!
    )
    
    REM Verificar se Flask foi instalado
    echo.
    echo Verificando instalacao do Flask...
    "venv\Scripts\python.exe" -c "import flask; print('Flask instalado - Versao:', flask.__version__)" 2>nul || (
        echo ERRO: Flask nao foi instalado! Tentando instalacao manual...
        "venv\Scripts\pip.exe" install flask flask-login flask-sqlalchemy sqlalchemy werkzeug jinja2 requests reportlab pandas openpyxl psutil --force-reinstall 2>nul
    )
    
    REM Verificar se requests foi instalado
    echo Verificando instalacao do requests...
    "venv\Scripts\python.exe" -c "import requests; print('Requests instalado - Versao:', requests.__version__)" 2>nul || (
        echo AVISO: Requests nao foi instalado! Tentando instalacao manual...
        "venv\Scripts\pip.exe" install requests --force-reinstall 2>nul
    )
    
    REM Verificar se pandas foi instalado
    echo Verificando instalacao do pandas...
    "venv\Scripts\python.exe" -c "import pandas; print('Pandas instalado - Versao:', pandas.__version__)" 2>nul || (
        echo AVISO: Pandas nao foi instalado! Tentando instalacao final...
        "venv\Scripts\pip.exe" install pandas --force-reinstall --no-cache-dir 2>nul
    )
) else (
    echo Usando pip global...
    echo Instalando dependencias do requirements.txt...
    pip install -r requirements.txt --timeout 120 2>nul
    if errorlevel 1 (
        echo AVISO: Falha ao instalar do requirements.txt. Tentando metodo alternativo...
        pip install -r requirements.txt --no-cache-dir --timeout 120 2>nul
        if errorlevel 1 (
            echo AVISO: Metodo alternativo falhou. Instalando dependencias principais...
            pip install Flask==3.1.0 --timeout 60 2>nul
            pip install Flask-Login==0.6.3 --timeout 60 2>nul
            pip install Flask-SQLAlchemy==3.1.1 --timeout 60 2>nul
            pip install SQLAlchemy==2.0.40 --timeout 60 2>nul
            pip install requests==2.32.3 --timeout 60 2>nul
            pip install Werkzeug==3.1.3 --timeout 60 2>nul
            pip install Jinja2==3.1.6 --timeout 60 2>nul
        )
    )
)

echo [6/6] Verificacao final...
REM Verificar se tudo está instalado
if exist "venv\Scripts\python.exe" (
    echo Testando Flask...
    "venv\Scripts\python.exe" -c "import flask; print('Flask: OK')" 2>nul || (
        echo ERRO: Flask nao esta funcionando!
        echo Tentando reinstalar Flask...
        "venv\Scripts\pip.exe" install flask --force-reinstall 2>nul
        "venv\Scripts\python.exe" -c "import flask; print('Flask: OK')" 2>nul || (
            echo ERRO CRITICO: Flask nao conseguiu ser instalado!
            pause
            exit /b 1
        )
    )
    
    echo Testando Flask-SQLAlchemy...
    "venv\Scripts\python.exe" -c "import flask_sqlalchemy; print('Flask-SQLAlchemy: OK')" 2>nul || (
        echo AVISO: Flask-SQLAlchemy nao esta funcionando, mas continuando...
    )
    
    echo Testando SQLAlchemy...
    "venv\Scripts\python.exe" -c "import sqlalchemy; print('SQLAlchemy: OK')" 2>nul || (
        echo AVISO: SQLAlchemy nao esta funcionando, mas continuando...
    )
    
    echo Testando requests...
    "venv\Scripts\python.exe" -c "import requests; print('Requests: OK')" 2>nul || (
        echo AVISO: Requests nao esta funcionando, mas continuando...
    )
    
    echo Testando reportlab...
    "venv\Scripts\python.exe" -c "import reportlab; print('ReportLab: OK')" 2>nul || (
        echo AVISO: ReportLab nao esta funcionando, mas continuando...
    )
    
    echo Testando pandas...
    "venv\Scripts\python.exe" -c "import pandas; print('Pandas: OK')" 2>nul || (
        echo AVISO: Pandas nao esta funcionando, mas continuando...
        echo O sistema pode funcionar sem pandas para algumas funcionalidades.
    )
) else (
    echo Testando com Python global...
    python -c "import flask; print('Flask: OK')" 2>nul || (
        echo ERRO: Flask nao esta funcionando!
        pause
        exit /b 1
    )
    
    python -c "import flask_sqlalchemy; print('Flask-SQLAlchemy: OK')" 2>nul || (
        echo AVISO: Flask-SQLAlchemy nao esta funcionando, mas continuando...
    )
    
    python -c "import sqlalchemy; print('SQLAlchemy: OK')" 2>nul || (
        echo AVISO: SQLAlchemy nao esta funcionando, mas continuando...
    )
    
    python -c "import requests; print('Requests: OK')" 2>nul || (
        echo AVISO: Requests nao esta funcionando, mas continuando...
    )
    
    python -c "import reportlab; print('ReportLab: OK')" 2>nul || (
        echo AVISO: ReportLab nao esta funcionando, mas continuando...
    )
    
    python -c "import pandas; print('Pandas: OK')" 2>nul || (
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
if exist "venv\Scripts\python.exe" (
    "venv\Scripts\python.exe" run.py
) else (
    python run.py
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
