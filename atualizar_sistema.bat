@echo off
title Sistema de Atualização - IAAM
color 0A

echo =======================================================
echo           SISTEMA DE ATUALIZACAO IAAM
echo =======================================================
echo.

set REPO_URL=https://github.com/kalebecaldas/sistema_senhas_web2.git
set BACKUP_DIR=backup_%date:~-4%%date:~4,2%%date:~7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set BACKUP_DIR=%BACKUP_DIR: =0%

echo [INFO] Iniciando processo de atualizacao...
echo [INFO] Repositorio: %REPO_URL%
echo [INFO] Backup sera salvo em: %BACKUP_DIR%
echo.

:: Verificar configuração do repositório atual
echo [INFO] Verificando repositorio atual...
for /f %%i in ('git remote get-url origin 2^>nul') do set CURRENT_REPO=%%i
if "%CURRENT_REPO%"=="" (
    echo [ERRO] Nao foi possivel obter URL do repositorio remoto!
    echo [INFO] Execute este script dentro da pasta do projeto IAAM
    pause
    exit /b 1
)

echo [INFO] Repositorio atual: %CURRENT_REPO%
echo %CURRENT_REPO% | findstr /i "sistema_senhas_web2" >nul
if %errorlevel% neq 0 (
    echo [AVISO] O repositorio atual pode nao ser o oficial
    echo [INFO] Continuando mesmo assim...
)
echo.

:: Verificar se estamos em um diretório git válido
git status >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Este diretorio nao e um repositorio Git valido!
    echo [ERRO] Execute este arquivo dentro do diretorio do projeto.
    pause
    exit /b 1
)

echo [OK] Repositorio Git valido detectado.
echo.

:: Fazer backup dos arquivos importantes
echo [INFO] Criando backup de seguranca...
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

:: Arquivos importantes para backup
copy "instance\sistema.db" "%BACKUP_DIR%\" >nul 2>&1
copy "app\config.py" "%BACKUP_DIR%\" >nul 2>&1
copy "VERSION" "%BACKUP_DIR%\" >nul 2>&1
copy "requirements.txt" "%BACKUP_DIR%\" >nul 2>&1

echo [OK] Backup criado em: %BACKUP_DIR%
echo.

:: Verificar atualizações disponíveis
echo [INFO] Verificando atualizacoes disponiveis...
git fetch origin >nul 2>&1

for /f %%i in ('git rev-list HEAD..origin/main --count') do set COMMITS_AHEAD=%%i

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
git log HEAD..origin/main --oneline --pretty=format:"  - %%h: %%s" | head -5
echo.

:: Perguntar ao usuário se deseja continuar
echo Deseja atualizar o sistema? (S/N)
set /p RESPONSE=
if /i not "%RESPONSE%"=="S" if /i not "%RESPONSE%"=="SIM" (
    echo [INFO] Atualizacao cancelada pelo usuario.
    pause
    exit /b 0
)

echo.
echo [INFO] Iniciando atualizacao...

:: Verificar mudanças locais e fazer stash se necessário
git status --porcelain >nul 2>&1
if %errorlevel% equ 0 (
    git status --porcelain | findstr /n "^" >nul
    if %errorlevel% equ 0 (
        echo [INFO] Mudancas locais detectadas, fazendo backup em stash...
        git stash
        if %errorlevel% equ 0 (
            echo [OK] Mudancas locais salvas em stash
        )
    )
)

:: Atualizar o sistema
git pull origin main
if %errorlevel% neq 0 (
    echo [ERRO] Falha ao atualizar o sistema via Git!
    echo [INFO] Tentando restaurar mudancas locais...
    git stash pop
    echo [INFO] Considere atualizar manualmente ou restaurar o backup.
    pause
    exit /b 1
)

:: Restaurar mudanças locais se existirem
git stash list | findstr /n "^" >nul
if %errorlevel% equ 0 (
    echo [INFO] Restaurando mudancas locais salvos em stash...
    git stash pop
)

echo [OK] Codigo atualizado com sucesso!
echo.

:: Atualizar dependências Python se o ambiente virtual existir
if exist "venv\Scripts\activate.bat" (
    echo [INFO] Atualizando dependencias Python...
    call venv\Scripts\activate.bat
    pip install -r requirements.txt --upgrade
    deactivate
    echo [OK] Dependencias atualizadas!
) else (
    echo [AVISO] Ambiente virtual nao encontrado.
    echo [AVISO] Dependencias nao foram atualizadas automaticamente.
    echo [INFO] Execute manualmente: pip install -r requirements.txt --upgrade
)

echo.
echo =======================================================
echo           ATUALIZACAO CONCLUIDA COM SUCESSO!
echo =======================================================
echo.
echo [INFO] Backup salvo em: %BACKUP_DIR%
echo [INFO] Sistema atualizado com %COMMITS_AHEAD% commits.
echo [INFO] Reinicie o sistema para aplicar as mudancas.
echo.

:: Perguntar se deseja reiniciar o sistema
echo Deseja reiniciar o sistema automaticamente? (S/N)
set /p RESTART=
if /i "%RESTART%"=="S" if exist "iniciar_sistema.bat" (
    echo [INFO] Reiniciando sistema...
    start "Sistema IAAM" iniciar_sistema.bat
) else (
    echo [INFO] Execute manualmente o iniciar_sistema.bat para iniciar.
)

echo.
echo Pressione qualquer tecla para finalizar...
pause >nul
