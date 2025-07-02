#!/bin/bash

# Script para iniciar o Sistema de Senhas e abrir o navegador automaticamente

echo "=== Sistema de Senhas ==="
echo "Iniciando o servidor e abrindo o navegador..."

# Verificar se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "Erro: Ambiente virtual não encontrado!"
    echo "Execute: ./setup_mac.sh"
    exit 1
fi

# Ativar o ambiente virtual
echo "Ativando ambiente virtual..."
source venv/bin/activate

# Verificar se as dependências estão instaladas
if ! python -c "import flask" 2>/dev/null; then
    echo "Instalando dependências..."
    pip install -r requirements.txt
fi

# Aguardar um pouco para o servidor iniciar e depois abrir o navegador
echo "Iniciando servidor Flask..."
echo "O navegador será aberto automaticamente em alguns segundos..."
echo ""

# Iniciar o servidor em background e abrir o navegador
python run.py &
SERVER_PID=$!

# Aguardar 3 segundos para o servidor inicializar
sleep 3

# Abrir o navegador
echo "Abrindo navegador..."
open http://localhost:5003

echo "Servidor iniciado! Pressione Ctrl+C para parar."
echo "O sistema está disponível em: http://localhost:5003"

# Aguardar o usuário parar o servidor
wait $SERVER_PID 