@echo off
echo ========================================
echo   VERIFICACAO DE MEMORIA RAM
echo ========================================
echo.

REM Obter informações de memória
for /f "tokens=2 delims==" %%a in ('wmic OS get TotalVisibleMemorySize /value') do set TOTAL=%%a
for /f "tokens=2 delims==" %%a in ('wmic OS get FreePhysicalMemory /value') do set FREE=%%a

REM Converter de KB para GB
set /a TOTAL_GB=%TOTAL:~0,-6%
set /a FREE_GB=%FREE:~0,-6%
set /a USED_GB=%TOTAL_GB%-%FREE_GB%
set /a PERCENT_USED=(%USED_GB%*100)/%TOTAL_GB%

echo Memoria Total: %TOTAL_GB% GB
echo Memoria Livre: %FREE_GB% GB
echo Memoria em Uso: %USED_GB% GB (%PERCENT_USED%%%)
echo.

REM Verificar se tem RAM suficiente
if %TOTAL_GB% LSS 4 (
    echo [AVISO] RAM total menor que 4GB - Sistema pode ficar lento!
    echo Recomendacao: Upgrade para 8GB RAM
) else if %TOTAL_GB% LSS 8 (
    echo [OK] RAM suficiente para rodar (4-8GB)
    echo Recomendacao: Use modo Kiosk e compacte videos para melhor performance
) else (
    echo [OTIMO] RAM suficiente para rodar perfeitamente (8GB+)
)

echo.
echo ========================================
echo   PROCESSOS CONSUMINDO MAIS RAM
echo ========================================
echo.

REM Mostrar top 5 processos por uso de memória
wmic process where "name='chrome.exe' or name='msedge.exe' or name='python.exe'" get name,workingsetsize /format:list 2>nul | findstr /V "^$"

echo.
echo ========================================
echo   RECOMENDACOES
echo ========================================
echo.

if %FREE_GB% LSS 1 (
    echo [CRITICO] Menos de 1GB livre!
    echo - Feche outros programas
    echo - Use modo Kiosk (iniciar_display_kiosk.bat)
    echo - Compacte videos para 720p
    echo - Considere upgrade de RAM
) else if %FREE_GB% LSS 2 (
    echo [ATENCAO] Pouca memoria livre
    echo - Feche programas desnecessarios
    echo - Use modo Kiosk
) else (
    echo [OK] Memoria suficiente para rodar o sistema
)

echo.
pause
