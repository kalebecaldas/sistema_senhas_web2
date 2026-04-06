@echo off
echo ========================================
echo   INICIANDO DISPLAY - MODO OTIMIZADO
echo ========================================
echo.
echo Este script vai:
echo 1. Iniciar o sistema Flask
echo 2. Abrir Chrome em modo Kiosk (tela cheia otimizada)
echo.
echo Modo Kiosk economiza RAM e CPU automaticamente!
echo.

REM Ativar ambiente virtual
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo [OK] Ambiente virtual ativado
) else (
    echo [ERRO] Ambiente virtual nao encontrado!
    echo Execute primeiro: iniciar_rapido.bat
    pause
    exit /b 1
)

REM Iniciar Flask em segundo plano
echo.
echo [*] Iniciando servidor Flask...
start /B python run.py

REM Aguardar servidor iniciar (10 segundos)
echo [*] Aguardando servidor inicializar...
timeout /t 10 /nobreak >nul

REM Detectar caminho do Chrome
set CHROME_PATH=
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    set CHROME_PATH=C:\Program Files\Google\Chrome\Application\chrome.exe
) else if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
    set CHROME_PATH=C:\Program Files (x86)\Google\Chrome\Application\chrome.exe
) else (
    echo [AVISO] Chrome nao encontrado. Abrindo navegador padrao...
    start http://localhost:5000/display
    goto :end
)

REM Abrir Chrome em modo Kiosk
echo [OK] Abrindo display em modo Kiosk (otimizado)...
start "" "%CHROME_PATH%" --kiosk --app=http://localhost:5000/display --disable-extensions --disable-background-networking --disable-sync --disable-translate --disable-features=TranslateUI --no-first-run --no-default-browser-check

:end
echo.
echo ========================================
echo   DISPLAY INICIADO COM SUCESSO!
echo ========================================
echo.
echo O display esta rodando em modo otimizado.
echo Para sair: Pressione Alt+F4 ou feche esta janela
echo.
pause
