@echo off
title Sistema de Atualização IAAM - Completo
color 0A
setlocal enabledelayedexpansion

echo =======================================================
echo        SISTEMA DE ATUALIZACAO IAAM COMPLETO
echo =======================================================
echo.

:: Verificar se script está sendo executado como administrador
net session >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Executando como administrador
) else (
    echo [AVISO] Para instalar o Git, execute como administrador
    echo [INFO] Clique com botao direito e "Executar como administrador"
    echo.
    set /p CONT="Continuar mesmo assim? (S/N): "
    if /i not "!CONT!"=="S" exit /b 1
)
echo.

set REPO_URL=https://github.com/kalebecaldas/sistema_senhas_web2.git
set BACKUP_DIR=backup_%date:~-4%%date:~4,2%%date:~7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set BACKUP_DIR=!BACKUP_DIR: =0!

echo [INFO] Configuracao:
echo [INFO]   Repositorio: %REPO_URL%
echo [INFO]   Backup: !BACKUP_DIR!
echo.

if not exist "app" (
    echo [ERRO] Execute este script na pasta principal do projeto IAAM
    echo [INFO] (onde ficam as pastas: app, static, templates, etc.)
    pause
    exit /b 1
)

echo [OK] Projeto IAAM detectado!
echo.

:: ==========================================================
:: VERIFICAR E INSTALAR GIT
:: ==========================================================

echo =======================================================
echo               VERIFICACAO DO GIT
echo =======================================================
echo.

git --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Git ja esta instalado!
    git --version
) else (
    echo [AVISO] Git nao encontrado!
    echo.
    echo Opcoes disponiveis:
    echo [1] Instalar Git automaticamente
    echo [2] Baixar instalador do Git
    echo [3] Continuar sem Git (limitado)
    echo [4] Sair
    echo.
    
    set /p CHOICE="Escolha uma opcao (1-4): "
    
    if "!CHOICE!"=="1" goto :install_git
    if "!CHOICE!"=="2" goto :download_git
    if "!CHOICE!"=="3" goto :continue_no_git
    if "!CHOICE!"=="4" exit /b 0
    
    echo [ERRO] Opcao invalida!
    goto :continue_no_git
)

echo.
goto :git_configured

:install_git
echo [INFO] Instalando Git automaticamente...
echo.

:: Tentar instalar via winget (Windows 10/11)
winget --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [INFO] Executando: winget install --id Git.Git -e --source winget
    winget install --id Git.Git -e --source winget --silent --accept-package-agreements --accept-source-agreements
    if !errorlevel! equ 0 (
        echo [OK] Git instalado via winget!
        goto :refresh_path
    ) else (
        echo [AVISO] Falha no winget, tentando chocolatey...
    )
)

:: Tentar instalar via chocolatey
choco --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [INFO] Executando: choco install git -y
    choco install git -y
    if !errorlevel! equ 0 (
        echo [OK] Git instalado via chocolatey!
        goto :refresh_path
    ) else (
        echo [AVISO] Falha no chocolatey...
    )
)

:: Tentar baixar e instalar diretamente
echo [INFO] Baixando instalador do Git...
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://github.com/git-for-windows/git/releases/latest/download/Git-%23.5.1-64-bit.exe' -OutFile 'git-installer.exe'}"
if %errorlevel% equ 0 (
    echo [INFO] Executando instalador do Git...
    "./git-installer.exe" /SILENT /NORESTART
    if !errorlevel! equ 0 (
        echo [OK] Git instalado!
        del "git-installer.exe" >nul 2>&1
        goto :refresh_path
    ) else (
        echo [ERRO] Falha na instalacao do Git
        del "git-installer.exe" >nul 2>&1
    )
) else (
    echo [ERRO] Falha ao baixar instalador do Git
)

echo [AVISO] Instalacao automatica falhou.
echo [INFO] Execute manualmente o instalador do Git.
echo.
goto :download_git

:download_git
echo [INFO] Baixando instalador do Git...
echo.
start "" "https://git-scm.com/download/win"
echo [INFO] Instalador aberto no navegador.
echo [INFO] Instale o Git manualmente e execute novamente este script.
pause
exit /b 0

:refresh_path
echo [INFO] Atualizando variaveis de ambiente...
call "refreshenv" >nul 2>&1
echo [OK] Variaveis atualizadas!

:: Verificar se Git esta disponivel agora
git --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Git funcionando apos instalacao!
    git --version
) else (
    echo [AVISO] Git instalado mas nao disponivel no PATH atual.
    echo [INFO] Reinicie o prompt/powershell e execute novamente este script.
    echo [INFO] OU adicione manualmente o Git ao PATH do sistema.
    pause
    exit /b 1
)

:git_configured
echo.

:: ==========================================================
:: CONFIGURAR GIT E REPOSITORIO
:: ==========================================================

echo =======================================================
echo              CONFIGURACAO DO REPOSITORIO
echo =======================================================
echo.

:: Configurar usuario Git se necessario
git config user.name >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Configurando usuario Git...
    git config --global user.name "Usuario IAAM"
    git config --global user.email "usuario@iaam.local"
    echo [OK] Usuario Git configurado!
)

:: Configurar credential helper para HTTPS
echo [INFO] Configurando HTTPS helper...
git config --global credential.helper store >nul 2>&1

:: Verificar se repositorio ja existe
if exist ".git" (
    echo [INFO] Repositorio Git ja existe.
    
    :: Verificar remote
    git remote get-url origin >nul 2>&1
    if %errorlevel% equ 0 (
        echo [INFO] Remote origin configurado.
    ) else (
        echo [INFO] Configurando remote origin...
        git remote add origin %REPO_URL%
    )
) else (
    echo [INFO] Inicializando repositorio Git...
    git init
    git remote add origin %REPO_URL%
)

:: Configurar URL correta
echo [INFO] Configurando URL do repositorio...
git remote set-url origin %REPO_URL%

echo [OK] Repositorio configurado!
echo.

:: ==========================================================
:: VERIFICAR E FAZER UPDATE
:: ==========================================================

echo =======================================================
echo               PROCESSAO DE ATUALIZACAO
echo =======================================================
echo.

:: Fazer backup
echo [INFO] Criando backup de seguranca...
if not exist "!BACKUP_DIR!" mkdir "!BACKUP_DIR!"

copy "instance\sistema.db" "!BACKUP_DIR!\" >nul 2>&1
copy "app\config.py" "!BACKUP_DIR!\" >nul 2>&1
copy "VERSION" "!BACKUP_DIR!\" >nul 2>&1
copy "requirements.txt" "!BACKUP_DIR!\" >nul 2>&1

echo [OK] Backup salvo em: !BACKUP_DIR!
echo.

:: Verificar atualizacoes
echo [INFO] Verificando atualizacoes...
git fetch origin >nul 2>&1

for /f "delims=" %%i in ('git rev-list HEAD..origin/main --count 2^>nul') do set COMMITS_AHEAD=%%i

if not defined COMMITS_AHEAD (
    echo [AVISO] Verificacao de commits falhou.
    echo [INFO] Tentando fetch manual...
    git fetch origin
    
    :: Tentar pull direto
    echo [INFO] Tentando atualizacao forcada...
    git pull origin main --no-verify
    if %errorlevel% equ 0 (
        echo [OK] Atualizacao forcada realizada!
        goto :success
    ) else (
        echo [ERRO] Falha na atualizacao!
        pause
        exit /b 1
    )
)

if %COMMITS_AHEAD% equ 0 (
    echo [INFO] Sistema ja esta atualizado!
    goto :success
)

echo [INFO] Encontradas %COMMITS_AHEAD% atualizacoes disponiveis.
echo.

:: Mostrar commits
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
echo [INFO] Atualizando sistema...

:: Verificar mudanças locais
git status --porcelain >nul 2>&1
for /f "delims=" %%i in ('git status --porcelain') do (
    set HAS_CHANGES=1
    goto :stash_changes
)

:stash_changes
if "%HAS_CHANGES%"=="1" (
    echo [INFO] Mudancas locais detectadas, fazendo stash...
    git stash push -m "Backup antes da atualizacao automatizada"
)

:: Pull das atualizações
git pull origin main --no-verify
if %errorlevel% neq 0 (
    echo [ERRO] Falha ao atualizar o sistema!
    
    if "%HAS_CHANGES%"=="1" (
        echo [INFO] Restaurando mudancas locais...
        git stash pop
    )
    
    echo [INFO] Considere atualizar manualmente.
    pause
    exit /b 1
)

:: Restaurar mudanças
if "%HAS_CHANGES%"=="1" (
    git stash list | findstr "." >nul 2>&1
    if !errorlevel! equ 0 (
        echo [INFO] Restaurando mudancas locais...
        git stash pop
    )
)

:success
echo [OK] Codigo atualizado com sucesso!
echo.

:: ==========================================================
:: ATUALIZAR DEPENDENCIAS
:: ==========================================================

echo =======================================================
echo              ATUALIZACAO DE DEPENDENCIAS
echo =======================================================
echo.

if exist "venv\Scripts\activate.bat" (
    echo [INFO] Ambiente virtual encontrado, atualizando dependencias Python...
    call venv\Scripts\activate.bat
    pip install -r requirements.txt --upgrade --no-cache-dir
    deactivate
    echo [OK] Dependencias Python atualizadas!
) else (
    echo [AVISO] Ambiente virtual nao encontrado.
    echo [INFO] Tentando com Python global...
    python -m pip install -r requirements.txt --upgrade --no-cache-dir
)

echo.

:: ==========================================================
:: FINALIZACAO
:: ==========================================================

echo =======================================================
echo           ATUALIZACAO CONCLUIDA COM SUCESSO!
echo =======================================================
echo.
echo [OK] Git configurado e funcionando
echo [OK] Sistema atualizado
echo [OK] Backup salvo em: !BACKUP_DIR!
echo [OK] Dependencias atualizadas
echo.

set /p RESTART="Deseja reiniciar o sistema automaticamente? (S/N): "
if /i "!RESTART!"=="S" (
    if exist "iniciar_sistema.bat" (
        echo [INFO] Reiniciando sistema...
        start "Sistema IAAM" iniciar_sistema.bat
    ) else (
        echo [INFO] Execute manualmente: python run.py
    )
) else (
    echo [INFO] Execute manualmente o iniciar_sistema.bat para iniciar.
)

echo.
echo Pressione qualquer tecla para finalizar...
pause >nul

exit /b 0
