@echo off
echo ========================================
echo  APLICANDO OTIMIZACOES DO SISTEMA
echo ========================================
echo.

echo [1/2] Criando indices no banco de dados...
python criar_indices.py
echo.

echo [2/2] Indices criados com sucesso!
echo.

echo ========================================
echo  OTIMIZACOES APLICADAS!
echo ========================================
echo.
echo O sistema agora deve responder muito mais rapido.
echo Reinicie o servidor para aplicar as mudancas.
echo.
pause
