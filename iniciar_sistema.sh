#!/bin/bash

# ============================================================================
# 🚀 Sistema de Senhas IAAM - Script de Inicialização
# ============================================================================
# Versão: 2.0
# Descrição: Inicia o sistema de gerenciamento de senhas com verificações
#            inteligentes e opções de configuração
# ============================================================================

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Configurações padrão
DEFAULT_PORT=5003
PORT=$DEFAULT_PORT
OPEN_BROWSER=false
AUTO_INSTALL=false

# Função para exibir banner
show_banner() {
    clear
    echo -e "${CYAN}${BOLD}"
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║                                                            ║"
    echo "║           🏥 SISTEMA DE SENHAS IAAM v2.0                  ║"
    echo "║                                                            ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Função para verificar se porta está em uso
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0  # Porta em uso
    else
        return 1  # Porta livre
    fi
}

# Função para encontrar porta disponível
find_available_port() {
    local port=$DEFAULT_PORT
    while check_port $port; do
        echo -e "${YELLOW}⚠️  Porta $port já está em uso${NC}"
        port=$((port + 1))
    done
    echo $port
}

# Processar argumentos
while [[ $# -gt 0 ]]; do
    case $1 in
        -p|--port)
            PORT="$2"
            shift 2
            ;;
        -b|--browser)
            OPEN_BROWSER=true
            shift
            ;;
        -a|--auto-install)
            AUTO_INSTALL=true
            shift
            ;;
        -h|--help)
            echo "Uso: $0 [opções]"
            echo ""
            echo "Opções:"
            echo "  -p, --port PORT        Define a porta (padrão: 5003)"
            echo "  -b, --browser          Abre o navegador automaticamente"
            echo "  -a, --auto-install     Instala dependências automaticamente"
            echo "  -h, --help             Mostra esta ajuda"
            echo ""
            echo "Exemplos:"
            echo "  $0                     # Inicia normalmente"
            echo "  $0 -b                  # Inicia e abre o navegador"
            echo "  $0 -p 8080 -b          # Usa porta 8080 e abre navegador"
            exit 0
            ;;
        *)
            echo -e "${RED}❌ Opção desconhecida: $1${NC}"
            echo "Use -h ou --help para ver as opções disponíveis"
            exit 1
            ;;
    esac
done

# Exibir banner
show_banner

# Verificar se o ambiente virtual existe
echo -e "${BLUE}🔍 Verificando ambiente virtual...${NC}"
if [ ! -d "venv" ]; then
    echo -e "${RED}❌ Ambiente virtual não encontrado!${NC}"
    echo ""
    echo -e "${YELLOW}📝 Para configurar o ambiente, execute:${NC}"
    echo -e "   ${CYAN}./setup_mac.sh${NC}"
    echo ""
    echo -e "${YELLOW}Ou manualmente:${NC}"
    echo -e "   ${CYAN}python3 -m venv venv${NC}"
    echo -e "   ${CYAN}source venv/bin/activate${NC}"
    echo -e "   ${CYAN}pip install -r requirements.txt${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Ambiente virtual encontrado${NC}"

# Ativar o ambiente virtual
echo -e "${BLUE}🔌 Ativando ambiente virtual...${NC}"
source venv/bin/activate 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Ambiente virtual ativado${NC}"
else
    echo -e "${RED}❌ Falha ao ativar ambiente virtual${NC}"
    exit 1
fi

# Verificar dependências
echo -e "${BLUE}📦 Verificando dependências...${NC}"
if ! python -c "import flask, sqlalchemy, flask_login" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Algumas dependências estão faltando${NC}"
    echo ""
    
    if [ "$AUTO_INSTALL" = true ]; then
        INSTALL="s"
    else
        read -p "$(echo -e ${CYAN}Deseja instalar as dependências agora? \(s/N\): ${NC})" INSTALL
    fi
    
    if [[ $INSTALL =~ ^[Ss]$ ]]; then
        echo -e "${BLUE}📥 Instalando dependências...${NC}"
        pip install -r requirements.txt --quiet --upgrade
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ Dependências instaladas com sucesso!${NC}"
        else
            echo -e "${RED}❌ Falha na instalação de dependências${NC}"
            exit 1
        fi
    else
        echo -e "${YELLOW}⚠️  Continuando sem instalar dependências...${NC}"
        echo -e "${YELLOW}⚠️  O sistema pode não funcionar corretamente!${NC}"
    fi
else
    echo -e "${GREEN}✅ Todas as dependências estão instaladas${NC}"
fi

# Verificar porta
echo -e "${BLUE}🔌 Verificando disponibilidade da porta...${NC}"
if check_port $PORT; then
    echo -e "${YELLOW}⚠️  Porta $PORT já está em uso${NC}"
    NEW_PORT=$(find_available_port)
    echo -e "${GREEN}✅ Porta $NEW_PORT está disponível${NC}"
    read -p "$(echo -e ${CYAN}Deseja usar a porta $NEW_PORT? \(S/n\): ${NC})" USE_NEW_PORT
    if [[ ! $USE_NEW_PORT =~ ^[Nn]$ ]]; then
        PORT=$NEW_PORT
    else
        echo -e "${RED}❌ Não é possível iniciar na porta $PORT (já em uso)${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ Porta $PORT está disponível${NC}"
fi

# Obter IP local
LOCAL_IP=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo "localhost")

# Exibir informações de inicialização
echo ""
echo -e "${PURPLE}${BOLD}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}${BOLD}║                  🌐 SERVIDOR INICIANDO                     ║${NC}"
echo -e "${PURPLE}${BOLD}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${CYAN}📍 Acesso Local:${NC}"
echo -e "   ${GREEN}http://localhost:$PORT${NC}"
echo -e "   ${GREEN}http://127.0.0.1:$PORT${NC}"
echo ""
echo -e "${CYAN}📍 Acesso na Rede:${NC}"
echo -e "   ${GREEN}http://$LOCAL_IP:$PORT${NC}"
echo ""
echo -e "${CYAN}⏹️  Para parar o servidor:${NC} ${YELLOW}Ctrl+C${NC}"
echo ""
echo -e "${PURPLE}${BOLD}════════════════════════════════════════════════════════════${NC}"
echo ""

# Abrir navegador se solicitado
if [ "$OPEN_BROWSER" = true ]; then
    echo -e "${BLUE}🌐 Abrindo navegador em 3 segundos...${NC}"
    (sleep 3 && open "http://localhost:$PORT" 2>/dev/null) &
fi

# Atualizar porta no run.py temporariamente se necessário
if [ $PORT -ne $DEFAULT_PORT ]; then
    export FLASK_RUN_PORT=$PORT
    python -c "
from app import create_app
app = create_app()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=$PORT, debug=True)
"
else
    # Iniciar o servidor
    python run.py
fi 