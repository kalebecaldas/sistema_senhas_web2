#!/bin/bash

# Script de Atualização Segura do Sistema de Senhas
# Uso: ./update_system.sh

set -e  # Parar em caso de erro

echo "🔄 Iniciando atualização do Sistema de Senhas..."
echo "================================================"

# Verificar se estamos no diretório correto
if [ ! -f "run.py" ]; then
    echo "❌ Erro: Execute este script no diretório raiz do projeto"
    exit 1
fi

# Verificar se é um repositório Git
if [ ! -d ".git" ]; then
    echo "❌ Erro: Este não é um repositório Git"
    exit 1
fi

# Verificar se é o repositório oficial
REMOTE_URL=$(git config --get remote.origin.url)
if [[ ! "$REMOTE_URL" == *"kalebecaldas/sistema_senhas_web2"* ]]; then
    echo "❌ Erro: Repositório não autorizado: $REMOTE_URL"
    exit 1
fi

echo "✅ Repositório oficial verificado"

# Fazer backup
echo "📦 Fazendo backup das configurações..."
BACKUP_DIR="backups/manual_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Arquivos importantes para backup
IMPORTANT_FILES=(
    "instance/sistema.db"
    "app/config.py"
    "VERSION"
    "requirements.txt"
)

for file in "${IMPORTANT_FILES[@]}"; do
    if [ -f "$file" ]; then
        cp "$file" "$BACKUP_DIR/"
        echo "  ✅ Backup: $file"
    else
        echo "  ⚠️  Arquivo não encontrado: $file"
    fi
done

echo "✅ Backup salvo em: $BACKUP_DIR"

# Verificar atualizações disponíveis
echo "🔍 Verificando atualizações..."
git fetch origin

COMMITS_AHEAD=$(git rev-list HEAD..origin/main --count)
if [ "$COMMITS_AHEAD" -eq 0 ]; then
    echo "✅ Sistema já está atualizado"
    exit 0
fi

echo "📥 Encontradas $COMMITS_AHEAD atualizações disponíveis"

# Confirmar atualização
read -p "Deseja continuar com a atualização? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Atualização cancelada"
    exit 0
fi

# Fazer pull das atualizações
echo "⬇️  Baixando atualizações..."
git pull origin main

# Verificar se requirements.txt foi modificado
if git diff --name-only HEAD~1 HEAD | grep -q "requirements.txt"; then
    echo "📦 Atualizando dependências..."
    pip install -r requirements.txt --upgrade
    echo "✅ Dependências atualizadas"
else
    echo "ℹ️  Nenhuma dependência nova"
fi

# Verificar se há migrações de banco
if [ -f "app/migrar_colunas.py" ]; then
    echo "🗄️  Executando migrações de banco..."
    python app/migrar_colunas.py
    echo "✅ Migrações concluídas"
fi

echo "================================================"
echo "✅ Atualização concluída com sucesso!"
echo "📦 Backup salvo em: $BACKUP_DIR"
echo "🔄 Reinicie o sistema para aplicar as mudanças"
echo "================================================" 