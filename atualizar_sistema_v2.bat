@echo off
title Sistema de Atualização IAAM v2
color 0A
setlocal enabledelayedexpansion

echo =======================================================
echo           SISTEMA DE ATUALIZACAO IAAM v2
echo =======================================================
echo.

set REPO_URL=https://github.com/kalebecaldas/sistema_senhas_web2.git
set BACKUP_DIR=backup_%date:~-4%%date:~4,2%%date:~7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set BACKUP_DIR=!BACKUP_DIR: =0!

echo [INFO] Iniciando processo de atualizacao...
echo [INFO] Repositorio configurado: %REPO_URL%
echo [INFO] Backup sera salvo em: !BACKUP_DIR!
echo.

:: Verificar se Git está instalado
echo [TEST] Verificando instalacao do Git...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Git nao esta instalado ou nao encontrado!
    echo [INFO] Instale o Git antes de continuar.
    pause
    exit /b 1
)
echo [OK] Git detectado correctamente!
echo.

:: Verificar se estamos em uma pasta válida do projeto
echo [TEST] Verificando estrutura do projeto...
if not exist "app" (
    echo [ERRO] Pasta 'app' nao encontrada!
    echo [INFO] Execute este script na pasta principal do projeto IAAM
    echo [INFO] (onde ficam as pastas: app, static, templates, etc.)
    pause
    exit /b 1
)

if not exist "run.py" (
    echo [ERRO] Arquivo 'run.py' nao encontrado!
    echo [INFO] Execute este script na pasta principal do projeto IAAM
    pause
    exit /b 1
)

echo [OK] Estrutura do projeto detectada corretamente!
echo.

:: Verificar se é um repositório Git
echo [TEST] Verificando repositorio Git...
git status >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Este diretorio nao e um repositorio Git!
    echo [INFO] Inicializando repositorio Git...
    
    git init
    git remote add origin %REPO_URL%
    git fetch origin
    git checkout -b main origin/main
    
    if %errorlevel% neq 0 (
        echo [ERRO] Falha ao configurar repositorio!
        pause
        exit /b 1
    )
    
    echo [OK] Repositorio Git configurado com sucesso!
)

:: Obter URL atual do repositório
echo [INFO] Verificando configuracao do repositorio...
for /f "delims=" %%i in ('git remote get-url origin 2^>nul') do set CURRENT_REPO=%%i

if "%CURRENT_REPO%"=="" (
    echo [ERRO] Nao foi possivel obter URL do repositorio remoto!
    echo [INFO] Configurando remote origin...
    git remote add origin %REPO_URL%
    set CURRENT_REPO=%REPO_URL%
)

echo [INFO] Repositorio remoto atual:
echo [INFO]   %CURRENT_REPO%

:: Verificar se é o repositório correto
echo %CURRENT_REPO% | findstr /i "kalebecaldas" >nul
if %errorlevel% neq 0 (
    echo [AVISO] Repositorio pode nao ser o oficial
    echo [INFO] Continuando mesmo assim...
)

echo [OK] Repositorio Git configurado e valido!
echo.

:: Fazer backup dos arquivos importantes
echo [INFO] Criando backup de seguranca...
if not exist "!BACKUP_DIR!" mkdir "!BACKUP_DIR!"

:: Arquivos importantes para backup
echo [INFO] Backup arquivos importantes...
if exist "instance\sistema.db" copy "instance\sistema.db" "!BACKUP_DIR!\" >nul 2>&1
if exist "app\config.py" copy "app\config.py" "!BACKUP_DIR!\" >nul 2>&1
if exist "VERSION" copy "VERSION" "!BACKUP_DIR!\" >nul 2>&1
if exist "requirements.txt" copy "requirements.txt" "!BACKUP_DIR!\" >nul 2>&1

echo [OK] Backup criado em: !BACKUP_DIR!
echo.

:: Buscar atualizações
echo [INFO] Verificando atualizacoes disponiveis...
git fetch origin

:: Verificar se há mudanças
for /f "delims=" %%i in ('git rev-list HEAD..origin/main --count 2^>nul') do set COMMITS_AHEAD=%%i

if not defined COMMITS_AHEAD (
    echo [ERRO] Nao foi possivel verificar atualizacoes!
    echo [INFO] Verificando se existe branch main...
    git ls-remote origin main >nul
    if %errorlevel% neq 0 (
        echo [ERRO] Branch main nao encontrada no repositorio!
        pause
        exit /b 1
    )
    echo [INFO] Branch encontrada, tentando atualizar...
    git pull origin main --no-verify
    echo [OK] Atualizacao forçada realizada!
    goto :success
)

if %COMMITS_AHEAD% equ 0 (
    echo [INFO] Sistema já está atualizado!
    echo [INFO] Nenhuma atualização disponível.
    pause
    exit /b 0
)

echo [INFO] Encontradas %COMMITS_AHEAD% atualizacoes disponiveis.
echo.

:: Mostrar commits pendentes
echo [INFO] Commits pendentes:
git log HEAD..origin/main --oneline --pretty=format:"  - %%h: %%s"
echo.

:: Confirmar atualização
set /p RESPONSE="Deseja atualizar o sistema? (S/N): "
if /i not "!RESPONSE!"=="S" if /i not "!RESPONSE!"=="SIM" (
    echo [INFO] Atualizacao cancelada pelo usuario.
    pause
    exit /b 0
)

echo.
echo [INFO] Iniciando atualizacao...

:: Verificar mudanças locais
git status --porcelain >nul 2>&1
if %errorlevel% equ 0 (
    for /f "delims=" %%i in ('git status --porcelain') do (
        set HAS_CHANGES=1
        goto :stash_changes
    )
)

:stash_changes
if "%HAS_CHANGES%"=="1" (
    echo [INFO] Mudancas locais detectadas, fazendo stash...
    git stash push -m "Backup antes da atualizacao automatizada"
    echo [OK] Mudancas locais salvas em stash
)

:: Atualizar sistema
git pull origin main --no-verify
if %errorlevel% neq 0 (
    echo [ERRO] Falha ao atualizar o sistema via Git!
    
    :: Tentar restaurar mudanças locais
    if "%HAS_CHANGES%"=="1" (
        echo [INFO] Restaurando mudancas locais...
        git stash pop
    )
    
    echo [INFO] Considere atualizar manualmente ou restaurar o backup.
    pause
    exit /b 1
)

:: Restaurar mudanças locais se existirem
if "%HAS_CHANGES%"=="1" (
    echo [INFO] Verificando se há mudanças para restaurar...
    git stash list | findstr "." >nul 2>&1
    if !errorlevel! equ 0 (
        echo [INFO] Restaurando mudancas locais...
        git stash pop
    )
)

:success
echo [OK] Codigo atualizado com sucesso!
echo.

:: Atualizar dependências Python
echo [INFO] Verificando ambiente Python...
if exist "venv\Scripts\activate.bat" (
    echo [INFO] Ambiente virtual encontrado, atualizando dependencias...
    call venv\Scripts\activate.bat
    pip install -r requirements.txt --upgrade --no-cache-dir
    deactivate
    echo [OK] Dependencias Python atualizadas!
) else (
    echo [AVISO] Ambiente virtual nao encontrado (venv\Scripts\activate.bat)
    if exist "python.exe" (
        echo [INFO] Tentando com Python global...
        python -m pip install -r requirements.txt --upgrade --no-cache-dir
    ) else (
        echo [AVISO] Execute manualmente: pip install -r requirements.txt --upgrade
    )
)

echo.
echo =======================================================
echo           ATUALIZACAO CONCLUIDA COM SUCESSO!
echo =======================================================
echo.
echo [INFO] Backup salvo em: !BACKUP_DIR!
echo [INFO] Sistema atualizado com sucesso!
echo [INFO] Reinicie o sistema para aplicar as mudancas.
echo.

:: Perguntar sobre reinicialização
set /p RESTART="Deseja reiniciar o sistema automaticamente? (S/N): "
if /i "!RESTART!"=="S" (
    if exist "iniciar_sistema.bat" (
        echo [INFO] Reiniciando sistema...
        start "Sistema IAAM" iniciar_sistema.bat
    ) else (
        echo [INFO] Arquivo iniciar_sistema.bat nao encontrado.
        echo [INFO] Execute manualmente: python run.py
    )
) else (
    echo [INFO] Execute manualmente o iniciar_sistema.bat para iniciar.
)

echo.
echo Pressione qualquer tecla para finalizar...
pause >nul
