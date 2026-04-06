@echo off
title Instalador Git para IAAM
color 0E

echo =======================================================
echo              INSTALADOR GIT PARA IAAM
echo =======================================================
echo.

:: Verificar se já tem Git
git --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Git já está instalado!
    git --version
    echo.
    echo Deseja reinstalar o Git mesmo assim? (S/N)
    set /p REINSTALL=
    if /i not "!REINSTALL!"=="S" (
        echo [INFO] Instalacao cancelada.
        pause
        exit /b 0
    )
)

echo [INFO] Baixando e instalando Git...
echo.

:: Informacoes do sistema
echo [SISTEMA] Informacoes:
echo [INFO]   OS: %OS%
echo [INFO]   Arquitetura: %PROCESSOR_ARCHITECTURE%
echo.

:: Diretorio temporario
set TEMP_DIR=%TEMP%\git-install
if not exist "%TEMP_DIR%" mkdir "%TEMP_DIR%"

:: URLs de download
set GIT_URL=https://github.com/git-for-windows/git/releases/download/v2.45.2.windows.2/Git-2.45.2-64-bit.exe

echo [INFO] Baixando instalador do Git...
echo [INFO] URL: %GIT_URL%
echo [INFO] Destino: %TEMP_DIR%\git-installer.exe
echo.

:: Baixar usando PowerShell
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; try { $ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest -Uri '%GIT_URL%' -OutFile '%TEMP_DIR%\git-installer.exe' -UseBasicParsing
write-output 'Download concluido'
} catch { 
write-output 'Erro: ' + $_.Exception.Message
exit 1
}}"

if %errorlevel% neq 0 (
    echo [ERRO] Falha no download do Git!
    echo.
    echo Opcoes alternativas:
    echo [1] Baixar manualmente do site oficial
    echo [2] Tentar novamente o download
    echo [3] Cancelar instalacao
    echo.
    
    set /p CHOICE="Escolha uma opcao (1-3): "
    
    if "!CHOICE!"=="1" (
        echo [INFO] Abrindo site do Git...
        start "" "https://git-scm.com/download/win"
        echo [INFO] Instale manualmente o Git e execute novamente o atualizador.
        pause
        exit /b 0
    ) else if "!CHOICE!"=="2" (
        goto :download_git_retry
    ) else (
        echo [INFO] Instalacao cancelada.
        pause
        exit /b 0
    )
)

echo [OK] Download concluido!
echo.

:: Verificar se arquivo existe
if not exist "%TEMP_DIR%\git-installer.exe" (
    echo [ERRO] Arquivo de instalacao nao encontrado!
    pause
    exit /b 1
)

echo [INFO] Arquivo de instalacao encontrado.
echo [INFO] Tamanho: 
for %%i in ("%TEMP_DIR%\git-installer.exe") do echo %%~zi bytes

echo.
echo [INFO] Executando instalador do Git...
echo [INFO] Aguarde a instalacao (pode demorar alguns minutos)...
echo.

:: Executar instalador silenciosamente
"%TEMP_DIR%\git-installer.exe" /SILENT /NORESTART /SUPPRESSMSGBOXES /DIR="C:\Program Files\Git"

if %errorlevel% equ 0 (
    echo [OK] Git instalado com sucesso!
) else (
    echo [AVISO] Instalacao concluida com avisos.
    echo [INFO] Verificando se Git esta funcionando...
)

echo.

:: Adicionar Git ao PATH da sessao atual
set "PATH=C:\Program Files\Git\bin;%PATH%"

:: Verificar instalacao
git --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Git instalado e funcionando!
    git --version
    echo.
    echo [INFO] Agora voce pode executar o atualizador normalmente:
    echo [INFO]   atualizar_sistema_completo.bat
) else (
    echo [AVISO] Git instalado mas pode nao estar no PATH atual.
    echo [INFO] Reinicie o prompt/powershell e tente novamente.
)

echo.

:: Limpar arquivos temporarios
if exist "%TEMP_DIR%\git-installer.exe" (
    echo [INFO] Limpando arquivos temporarios...
    del "%TEMP_DIR%\git-installer.exe"
)

rmdir "%TEMP_DIR%" >nul 2>&1

echo =======================================================
echo              INSTALACAO CONCLUIDA!
echo =======================================================
echo.

echo Proximo passo:
echo [1] Execute: atualizar_sistema_completo.bat
echo [2] Ou execute: atualizar_sistema_v2.bat
echo.

pause

:download_git_retry
echo [INFO] Tentando download novamente...
goto :start
