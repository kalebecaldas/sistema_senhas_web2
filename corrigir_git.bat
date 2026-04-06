@echo off
title Correção Automática Git IAAM
color 0E

echo ======================================================
echo           CORRECAO AUTOMATICA GIT IAAM
echo ======================================================
echo.

:: Verificar se estamos na pasta correta
if not exist "app" (
    echo [ERRO] Execute este script na pasta principal do projeto IAAM
    echo [INFO] (onde fica a pasta 'app')
    pause
    exit /b 1
)

echo [OK] Pasta do projeto identificada corretamente!
echo.

:: Verificar se Git está disponível
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Git nao encontrado! Instale o Git antes de continuar.
    pause
    exit /b 1
)

echo [OK] Git encontrado e funcional!
echo.

:: Verificar se já é um repositório Git
if exist ".git" (
    echo [INFO] Repositorio Git ja existe.
    echo [INFO] Verificando configuracao atual...
    
    git remote get-url origin >nul 2>&1
    if %errorlevel% equ 0 (
        echo [INFO] Remote origin ja configurado.
        for /f "delims=" %%i in ('git remote get-url origin') do echo [INFO] URL atual: %%i
    ) else (
        echo [INFO] Remote origin nao configurado, adicionando...
        git remote add origin https://github.com/kalebecaldas/sistema_senhas_web2.git
    )
) else (
    echo [INFO] Inicializando novo repositorio Git...
    git init
    git remote add origin https://github.com/kalebecaldas/sistema_senhas_web2.git
)

echo.

:: Configurar URL correta (sempre)
echo [INFO] Configurando URL do repositorio...
git remote set-url origin https://github.com/kalebecaldas/sistema_senhas_web2.git

:: Verificar se fetch funciona
echo [INFO] Testando conexao com GitHub...
git fetch --dry-run origin >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Conexao com GitHub funcionando!
) else (
    echo [ERRO] Problema de conexao com GitHub!
    echo [INFO] Verifique sua conexao de internet.
    echo [INFO] Tentando configurar HTTPS...
    
    :: Configurar credential helper para HTTPS
    git config --global credential.helper store
)

:: Configurar branch main
echo [INFO] Configurando branch main...
git fetch origin
git checkout -B main 2>nul
git branch --set-upstream-to=origin/main main 2>nul

echo.

:: Configurar usuario Git se necessario
git config user.name >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Configurando usuario Git...
    git config user.name "Usuario IAAM"
    git config user.email "usuario@iaam.local"
)

echo.

:: Teste final
echo [INFO] Executando teste final...
echo.
echo URL do repositorio:
git remote get-url origin

echo.
echo Status:
git status --short

echo.
echo Brancch atual:
git branch --show-current

echo.
echo Ultima verificacao:
git fetch --dry-run origin >nul 2>&1 && echo [OK] Fetch funcionando || echo [AVISO] Possivel problema no fetch

echo.
echo ======================================================
echo           CORRECAO CONCLUIDA!
echo ======================================================
echo.

echo [INFO] Teste agora o atualizador:
echo [INFO]   atualizar_sistema_v2.bat
echo.
echo OU execute o diagnostico:
echo [INFO]   diagnostico_git.bat
echo.

pause
