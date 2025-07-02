#!/bin/bash

# Script de configuração inicial para macOS
# Este script configura todo o ambiente necessário para o Sistema de Senhas

echo "=== Configuração do Sistema de Senhas para macOS ==="
echo ""

# Verificar se Python 3 está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado!"
    echo "Por favor, instale o Python 3 primeiro:"
    echo "  brew install python3"
    echo "  ou baixe de: https://www.python.org/downloads/"
    exit 1
fi

echo "✅ Python 3 encontrado: $(python3 --version)"

# Criar ambiente virtual se não existir
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
    echo "✅ Ambiente virtual criado!"
else
    echo "✅ Ambiente virtual já existe!"
fi

# Ativar ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências
echo "📥 Instalando dependências..."
pip install -r requirements.txt

# Tornar script executável
echo "🔐 Configurando permissões..."
chmod +x iniciar_sistema.sh

echo ""
echo "🎉 Configuração concluída com sucesso!"
echo ""
echo "Para iniciar o sistema, execute:"
echo "  ./iniciar_sistema.sh"
echo ""
echo "Ou manualmente:"
echo "  source venv/bin/activate"
echo "  python run.py"
echo ""
echo "O sistema estará disponível em: http://localhost:5003" 