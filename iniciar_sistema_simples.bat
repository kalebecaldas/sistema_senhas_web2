@echo off
setlocal

REM Ir para a pasta deste script (pasta do sistema)
cd /d "%~dp0" 2>nul || exit /b 1

REM Caminhos padrao
set "VENV_PY=venv\Scripts\python.exe"
set "PYTHON_CMD="

REM Garantir que estamos na raiz do projeto (onde fica run.py)
if not exist "run.py" (
    exit /b 1
)

REM Se nao existir venv, nao tenta instalar nada (apenas sai silencioso)
if exist "%VENV_PY%" (
    set "PYTHON_CMD=%VENV_PY%"
) else (
    REM Tentar py -3
    py -3 --version >nul 2>&1 && set "PYTHON_CMD=py -3"
    REM Tentar python
    if not defined PYTHON_CMD (
        python --version >nul 2>&1 && set "PYTHON_CMD=python"
    )
)

REM Se ainda nao tiver Python, sai sem mensagem (para uso em inicializacao silenciosa)
if not defined PYTHON_CMD (
    exit /b 1
)

REM Tentar ativar o venv se existir (nao e obrigatorio para rodar)
if exist "venv\Scripts\activate.bat" (
    call "venv\Scripts\activate.bat" 2>nul
)

REM Iniciar o servidor Flask
%PYTHON_CMD% run.py

endlocal
