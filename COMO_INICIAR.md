# 🚀 Como Iniciar o Sistema de Senhas IAAM

Este documento explica as diferentes formas de iniciar o sistema.

## 📋 Pré-requisitos

Antes de iniciar o sistema, certifique-se de que:
- O ambiente virtual está configurado (`venv/`)
- As dependências estão instaladas

Se ainda não configurou, execute:
```bash
./setup_mac.sh
```

---

## 🎯 Formas de Iniciar

### 1. **Inicialização Padrão** (Recomendado)
```bash
./iniciar_sistema.sh
```

**Características:**
- ✅ Verificação completa do ambiente
- ✅ Verificação de dependências
- ✅ Detecção automática de porta em uso
- ✅ Interface colorida e informativa
- ✅ Suporte a argumentos personalizados

---

### 2. **Inicialização Rápida com Navegador**
```bash
./iniciar_rapido.sh
```

**Características:**
- ✅ Abre o navegador automaticamente
- ✅ Todas as verificações do modo padrão
- 🚀 Ideal para desenvolvimento

---

### 3. **Inicialização com Navegador (Manual)**
```bash
./iniciar_com_navegador.sh
```

**Características:**
- ✅ Abre o navegador após 3 segundos
- ⚠️ Script legado (use `./iniciar_rapido.sh` ao invés)

---

## 🎛️ Opções Avançadas

O script `iniciar_sistema.sh` suporta várias opções:

### Abrir Navegador Automaticamente
```bash
./iniciar_sistema.sh --browser
# ou
./iniciar_sistema.sh -b
```

### Usar Porta Personalizada
```bash
./iniciar_sistema.sh --port 8080
# ou
./iniciar_sistema.sh -p 8080
```

### Instalar Dependências Automaticamente
```bash
./iniciar_sistema.sh --auto-install
# ou
./iniciar_sistema.sh -a
```

### Combinar Opções
```bash
# Porta 8080 + Abrir navegador + Auto-instalar
./iniciar_sistema.sh -p 8080 -b -a
```

### Ver Ajuda
```bash
./iniciar_sistema.sh --help
# ou
./iniciar_sistema.sh -h
```

---

## 🌐 URLs de Acesso

Após iniciar, o sistema estará disponível em:

- **Local:** `http://localhost:5003`
- **Alternativo:** `http://127.0.0.1:5003`
- **Rede Local:** `http://[SEU_IP]:5003`

> **Nota:** Se a porta 5003 estiver em uso, o sistema oferecerá automaticamente uma porta alternativa.

---

## 🛑 Como Parar o Sistema

Pressione `Ctrl+C` no terminal onde o servidor está rodando.

---

## 🔧 Solução de Problemas

### Erro: "Ambiente virtual não encontrado"
```bash
# Execute a configuração inicial
./setup_mac.sh
```

### Erro: "Porta já em uso"
```bash
# Use uma porta diferente
./iniciar_sistema.sh -p 8080
```

### Erro: "Dependências faltando"
```bash
# Instale automaticamente
./iniciar_sistema.sh --auto-install

# Ou manualmente
source venv/bin/activate
pip install -r requirements.txt
```

### Permissão Negada
```bash
# Torne os scripts executáveis
chmod +x iniciar_sistema.sh
chmod +x iniciar_rapido.sh
chmod +x setup_mac.sh
```

---

## 📊 Comparação dos Scripts

| Script | Navegador | Verificações | Opções | Velocidade |
|--------|-----------|--------------|--------|------------|
| `iniciar_sistema.sh` | ❌ (opcional) | ✅ Completas | ✅ Muitas | ⚡ Normal |
| `iniciar_rapido.sh` | ✅ Auto | ✅ Completas | ❌ Nenhuma | ⚡⚡ Rápido |
| `iniciar_com_navegador.sh` | ✅ Auto | ⚠️ Básicas | ❌ Nenhuma | ⚡ Normal |

---

## 💡 Dicas

1. **Para desenvolvimento diário:** Use `./iniciar_rapido.sh`
2. **Para produção/demo:** Use `./iniciar_sistema.sh`
3. **Para debugging:** Use `./iniciar_sistema.sh -p 8080` (porta diferente)
4. **Para primeira execução:** Use `./iniciar_sistema.sh -a` (auto-instalar)

---

## 📝 Exemplos Práticos

### Desenvolvimento Normal
```bash
./iniciar_rapido.sh
```

### Apresentação/Demo
```bash
./iniciar_sistema.sh --browser
```

### Teste em Porta Diferente
```bash
./iniciar_sistema.sh -p 8080 -b
```

### Configuração Inicial Completa
```bash
./setup_mac.sh
./iniciar_sistema.sh -a -b
```

---

## 🆘 Suporte

Se encontrar problemas:
1. Verifique os logs no terminal
2. Consulte `README_MAC.md` para mais detalhes
3. Execute `./iniciar_sistema.sh --help` para ver todas as opções
