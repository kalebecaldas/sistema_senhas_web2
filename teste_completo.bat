@echo off
title Teste Completo Sistema IAAM
color 0E

echo ======================================================
echo           TESTE COMPLETO SISTEMA IAAM
echo ======================================================
echo.

:: Apenas executar teste se estiver na pasta correta
if not exist "app" (
    echo [ERRO] Execute na pasta principal do projeto IAAM
    echo [INFO] (onde fica a pasta 'app')
    pause
    exit /b 1
)

echo [OK] Estrutura do projeto detectada
echo.

:: ==========================================================
:: TESTE 1: VERIFICAR GIT
:: ==========================================================

echo [TESTE 1] VERIFICACAO DO GIT
echo --------------------------------
echo.

git --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Git INSTALADO e funcionando
    git --version
) else (
    echo ❌ Git NAO INSTALADO
    echo.
    echo [SOLUCOES DISPONIVEIS]:
    echo [1] instalar_git.bat                    (Instalar Git automaticamente)
    echo [2] atualizar_sistema_completo.bat      (Instalar Git + Atualizar tudo)
    echo [3] Instalar manualmente do site        (https://git-scm.com/download/win)
    echo.
    set /p INSTALL_GIT="Executar instalador automatico do Git? (S/N): "
    if /i "!INSTALL_GIT!"=="S" (
        echo [INFO] Execute como administrador: instalar_git.bat
        start "" "instalar_git.bat"
        echo [INFO] Apos instalar o Git, execute novamente este teste.
        pause
        exit /b 0
    )
)

echo.

:: ==========================================================
:: TESTE 2: VERIFICAR ESTRUTURA REPOSITÓRIO
:: ==========================================================

echo [TESTE 2] VERIFICACAO DO REPOSITORIO
echo --------------------------------
echo.

if not exist ".git" (
    echo ❌ Nao e um repositorio Git
    echo [SOLUCAO]: Execute corrigir_git.bat
) else (
    echo ✅ Repositorio Git detectado
    
    :: Verificar remote
    git remote get-url origin >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ Remote 'origin' configurado
        for /f "delims=" %%i in ('git remote get-url origin') do echo [INFO] URL: %%i
    ) else (
        echo ❌ Remote 'origin' nao configurado
        echo [SOLUCAO]: Execute corrigir_git.bat
    )
)

echo.

:: ==========================================================
:: TESTE 3: TESTAR CONECTIVIDADE
:: ==========================================================

echo [TESTE 3] TESTE DE CONECTIVIDADE
echo --------------------------------
echo.

echo [INFO] Testando conexao com GitHub...
git ls-remote https://github.com/kalebecaldas/sistema_senhas_web2.git >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ GitHub acessivel
) else (
    echo ❌ Problema de conexao com GitHub
    echo [VERIFICAR]: Internet, firewall, proxy
)

echo.

:: ==========================================================
:: TESTE 4: VERIFICAR ATUALIZAÇÕES DISPONÍVEIS
:: ==========================================================

echo [TESTE 4] VERIFICACAO DE ATUALIZACOES
echo --------------------------------
echo.

echo [INFO] Buscando atualizacoes...
git fetch origin >nul 2>&1

for /f "delims=" %%i in ('git rev-list HEAD..origin/main --count 2^>nul') do set COMMITS_AHEAD=%%i

if not defined COMMITS_AHEAD (
    echo ❌ Nao foi possivel verificar atualizacoes
) else (
    if %COMMITS_AHEAD% equ 0 (
        echo ✅ Sistema atualizado (sem atualizacoes)
    ) else (
        echo ✅ Encontradas %COMMITS_AHEAD% atualizacoes disponiveis
    )
)

echo.

:: ==========================================================
:: TESTE 5: VERIFICAR DEPENDÊNCIAS PYTHON
:: ==========================================================

echo [TESTE 5] VERIFICACAO PYTHON
echo --------------------------------
echo.

python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Python encontrado
    python --version
) else (
    python3 --version >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ Python3 encontrado
        python3 --version
    ) else (
        echo ❌ Python nao encontrado
        echo [SOLUCAO]: Instalar Python do site oficial
    )
)

echo.

:: Verificar ambiente virtual
if exist "venv\Scripts\activate.bat" (
    echo ✅ Ambiente virtual Python encontrado
) else (
    echo ❌ Ambiente virtual nao encontrado (venv/)
    echo [INFO]: Dependencias serao instaladas globalmente
)

echo.

:: ==========================================================
:: RELATÓRIO FINAL
:: ==========================================================

echo ======================================================
echo              RELATORIO FINAL DO TESTE
echo ======================================================
echo.

set ERRORS=0
set WARNINGS=0

git --version ><｜tool▁calls▁end｜> 2>&1
if %errorlevel% neq 0 set /a ERRORS+=1

if not exist ".git" set /a ERRORS+=1

git remote get-url origin >nul 2>&1
if %errorlevel% neq 0 set /a WARNINGS+=1

python --version >nul 2>&1 && python3 --version >nul 2>&1
if %errorlevel% neq 0 set /a WARNINGS+=1

echo [RESULTADO]:
echo   Erros criticos: %ERRORS%
echo   Avisos: %WARNINGS%
echo.

if %ERRORS% equ 0 (
    if %WARNINGS% equ 0 (
        echo ✅ SISTEMA PERFEITO!
        echo [INFO] Voce pode usar qualquer atualizador normalmente:
        echo [INFO]   • atualizar_sistema_completo.bat (recomendado)
        echo [INFO]   • atualizar_sistema_v2.bat
        echo [INFO]   • atualizador_autonomo.py --auto
    ) else (
        echo ⚠️  SISTEMA FUNCIONAL COM AVISOS
        echo [INFO] Use o atualizador basico: atualizar_sistema_v2.bat
    )
) else (
    echo ❌ SISTEMA COM PROBLEMAS
    echo [PRECISA]: Resolver erros antes de atualizar
    echo.
    echo [SOLUCOES]:
    echo [1] Execute: instalar_git.bat (para Git)
    echo [2] Execute: corrigir_git.bat (para repositorio)
    echo [3] Instale Python do site oficial
    echo.
)

echo ======================================================
echo.

set /p CONT="Deseja executar algum solucionador automatico? (S/N): "
if /i "!CONT!"=="S" (
    echo.
    echo [SOLUCIONADORES DISPONIVEIS]:
    echo [1] instalar_git.bat                    (Só Git)
    echo [2] corrigir_git.bat                    (Só repositório)
    echo [3] atualizar_sistema_completo.bat        (Git + Atualização)
    echo.
    set /p CHOICE="Escolha (1-3): "
    
    if "!CHOICE!"=="1" (
        start "" "instalar_git.bat"
    ) else if "!CHOICE!"=="2" (
        start "" "corrigir_git.bat"
    ) else if "!CHOICE!"=="3" (
        start "" "atualizar_sistema_completo.bat"
    )
)

echo.
echo Pressione qualquer tecla para finalizar...
pause >nul
