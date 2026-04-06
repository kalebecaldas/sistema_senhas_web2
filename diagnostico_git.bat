@echo off
title Diagnóstico Git IAAM
color 0E

echo ======================================================
echo               DIAGNOSTICO GIT IAAM
echo ======================================================
echo.

:: Informações do sistema
echo [SISTEMA] Informacoes do ambiente:
echo.
echo Diretorio atual: %CD%
echo Usuario: %USERNAME%
echo Data/Hora: %DATE% %TIME%
echo.

:: Verificar Git
echo [TEST] Verificando instalacao do Git...
git --version
if %errorlevel% neq 0 (
    echo [ERRO] Git NAO ENCONTRADO!
    goto :end
) else (
    echo [OK] Git instalado e funcional.
)
echo.

:: Verificar estrutura de arquivos
echo [TEST] Verificando estrutura do projeto:
echo.
if exist "app" (echo [OK] Pasta 'app' encontrada) else (echo [ERRO] Pasta 'app' NAO encontrada)
if exist "run.py" (echo [OK] Arquivo 'run.py' encontrado) else (echo [ERRO] Arquivo 'run.py' NAO encontrado)
if exist ".git" (echo [OK] Pasta '.git' encontrada - repositorio Git detectado) else (echo [ERRO] Pasta '.git' NAO encontrada)
echo.

:: Verificar configuração do Git
echo [TEST] Configuracao do Git:
echo.

echo Usuario Git:
git config user.name
git config user.email
echo.

echo Repositorio remoto:
git remote -v 2>nul || echo [ERRO] Sem repositorio remoto configurado
echo.

echo Status do repositorio:
git status --porcelain 2>nul || echo [ERRO] Repositorio invalido
echo.

:: Teste de conectividade
echo [TEST] Testando conectividade com GitHub:
echo.
git ls-remote https://github.com/kalebecaldas/sistema_senhas_web2.git >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] GitHub acessivel
) else (
    echo [ERRO] Problema de conexao com GitHub
)
echo.

:: Verificar branch atual
echo [TEST] Informacoes da branch:
echo.
git branch --show-current 2>nul || echo [ERRO] Branch atual nao identificada
git branch -r 2>nul || echo [ERRO] Branches remotas nao encontradas
echo.

:: Teste de fetch
echo [TEST] Testando fetch do repositório:
echo.
git fetch --dry-run 2>&1 || echo [ERRO] Fetch falhou
echo.

echo ======================================================
echo               RESUMO DO DIAGNOSTICO
echo ======================================================
echo.

:: Verificações finais
set ERRORS=0

if not exist "app" set /a ERRORS+=1
if not exist "run.py" set /a ERRORS+=1
if not exist ".git" set /a ERRORS+=1

git remote get-url origin >nul 2>&1
if %errorlevel% neq 0 set /a ERRORS+=1

echo Total de problemas encontrados: %ERRORS%

if %ERRORS% equ 0 (
    echo [SUCESSO] Sistema esta funcionando corretamente!
    echo [INFO] Execute o atualizador normalmente.
) else (
    echo [FALHA] Encontrados %ERRORS% problemas que precisam ser corrigidos.
    echo [INFO] Verifique os testes acima para identificar os problemas.
)

:end
echo.
echo Pressione qualquer tecla para finalizar...
pause >nul
