#!/bin/bash

# Script para iniciar o Sistema de Senhas no macOS
# Baseado no arquivo "SISTEMA DE SENHA.bat"

echo "=== Sistema de Senhas ==="
echo "Iniciando o servidor..."

# Verificar se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "Erro: Ambiente virtual não encontrado!"
    echo "Execute: python3 -m venv venv"
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

# Rodar o servidor Flask
echo "Iniciando servidor Flask..."
python run.py 