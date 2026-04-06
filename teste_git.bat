@echo off
title Teste Git Repositório IAAM
color 0A

echo =======================================================
echo           TESTE DE REPOSITORIO GIT IAAM
echo =======================================================
echo.

:: Verificar se git está funcionando
echo [TEST] Verificando Git...
git --version
if %errorlevel% neq 0 (
    echo [ERRO] Git nao encontrado!
    pause
    exit /b 1
)

echo.

:: Verificar se estamos em um repositório Git
echo [TEST] Verificando repositorio atual...
git status >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Este diretorio nao e um repositorio Git!
    echo [INFO] Execute este script dentro da pasta do projeto
    pause
    exit /b 1
)

echo [OK] Repositorio Git encontrado!
echo.

:: Mostrar configuração atual
echo [TEST] Configuracao do repositorio:
echo.

echo URL remota atual:
for /f %%i in ('git remote get-url origin 2^>nul') do echo   %%i

echo.
echo Branches:
git branch -r

echo.
echo Ultima verificacao de atualizacoes:
git fetch origin --dry-run 2>&1

echo.
echo =======================================================
echo [INFO] Repositorio configurado corretamente!
echo =======================================================
echo.

pause
