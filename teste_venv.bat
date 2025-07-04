@echo off
chcp 65001 >nul
title Teste - Ambiente Virtual

REM Garantir que estamos no diretório correto
cd /d "%~dp0"

echo ========================================
echo    TESTE - AMBIENTE VIRTUAL
echo ========================================
echo.

echo [1] Diretorio atual: %CD%
echo.

echo [2] Verificando estrutura do ambiente virtual...
if exist "venv" (
    echo Pasta venv: EXISTE
    echo.
    echo Conteudo da pasta venv:
    dir /b venv
    echo.
    echo Conteudo de venv\Scripts:
    dir /b venv\Scripts 2>nul
    echo.
) else (
    echo Pasta venv: NAO EXISTE
)

echo [3] Verificando arquivos de ativacao...
if exist "venv\Scripts\activate.bat" (
    echo activate.bat: EXISTE
) else (
    echo activate.bat: NAO EXISTE
)

if exist "venv\Scripts\activate" (
    echo activate (shell): EXISTE
) else (
    echo activate (shell): NAO EXISTE
)

if exist "venv\Scripts\python.exe" (
    echo python.exe: EXISTE
) else (
    echo python.exe: NAO EXISTE
)

if exist "venv\Scripts\pip.exe" (
    echo pip.exe: EXISTE
) else (
    echo pip.exe: NAO EXISTE
)

echo.

echo [4] Testando ativacao do ambiente virtual...
if exist "venv\Scripts\activate.bat" (
    echo Tentando ativar...
    call "venv\Scripts\activate.bat"
    if errorlevel 1 (
        echo ERRO: Falha na ativacao!
    ) else (
        echo Ativacao: SUCESSO
        echo.
        echo Python ativo:
        where python
        echo.
        echo Variavel VIRTUAL_ENV:
        echo %VIRTUAL_ENV%
    )
) else (
    echo Nao foi possivel testar - arquivo nao existe
)

echo.

echo [5] Verificando Python global...
echo Python global:
where python
echo.

echo [6] Verificando pip global...
echo Pip global:
where pip
echo.

echo [7] Testando criacao de ambiente virtual...
echo Tentando criar ambiente virtual de teste...
python -m venv teste_venv
if errorlevel 1 (
    echo ERRO: Falha ao criar ambiente virtual de teste!
) else (
    echo SUCESSO: Ambiente virtual de teste criado!
    echo.
    echo Conteudo do ambiente de teste:
    dir /b teste_venv\Scripts
    echo.
    echo Removendo ambiente de teste...
    rmdir /s /q teste_venv
)

echo.
echo ========================================
echo    TESTE CONCLUIDO
echo ========================================
echo.

if exist "venv\Scripts\activate.bat" (
    echo Para tentar ativar manualmente:
    echo call "venv\Scripts\activate.bat"
    echo.
) else (
    echo Para recriar o ambiente virtual:
    echo python -m venv venv
    echo.
)

pause 