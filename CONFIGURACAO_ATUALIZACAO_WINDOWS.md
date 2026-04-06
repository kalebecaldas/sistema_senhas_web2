# 🚀 Sistema de Atualização Automática - Windows

## 📋 **Arquivos Criados**

### **1. `atualizar_sistema.bat`** ⭐ **PRINCIPAL**
- ✅ Script `.bat` para Windows  
- ✅ Execução simples (duplo clique)
- ✅ Interface colorida em português
- ✅ Backup automático antes da atualização
- ✅ Verificação completa de atualizações
- ✅ Atualização de dependências Python

### **2. `atualizador_autonomo.py`**
- ✅ Script Python autônomo
- ✅ Funciona em qualquer sistema operacional
- ✅ Pode ser convertido em `.exe`

### **3. `criar_exe_updater.py`**
- ✅ Converte o script Python em `.exe`
- ✅ Usa PyInstaller para criar executável único
- ✅ Resultado: `AtualizadorIAAM.exe`

## 🎯 **Como Usar**

### **Opção 1: Arquivo .bat (RECOMENDADO)**
```bash
1. Copie "atualizar_sistema.bat" para o computador Windows
2. Coloque-o na pasta do projeto IAAM
3. Execute clicando duas vezes
4. Siga as instruções na tela
```

### **Opção 2: Construir como .exe**
```bash
# No macOS (onde você está agora):
python3 criar_exe_updater.py

# Isso criará:
# dist/AtualizadorIAAM.exe
```

### **Opção 3: Script Python Direto**
```bash
python3 atualizador_autonomo.py
```

## 📦 **Funcionalidades do Sistema**

### **✅ Backup Automático**
- Salva `instance/sistema.db`
- Salva `app/config.py`
- Salva `VERSION` e `requirements.txt`
- Cria pasta automática com timestamp

### **✅ Verificação Inteligente**
- Detecta repositório Git válido
- Verifica atualizações remotas
- Mostra commits pendentes
- Confirmação antes de atualizar

### **✅ Atualização Completa**
- `git pull origin main`
- Atualiza dependências Python
- Preserva configurações locais
- Log detalhado de operações

### **✅ Interface Amigável**
- Mensagens em português
- Status colorido (verde/vermelho)
- Progress visual
- Confirmações de segurança

## 🛡️ **Segurança**

### **Backup Automático**
```
📁 backup_20251002_145930/
   ├── sistema.db
   ├── config.py
   ├── VERSION
   ├── requirements.txt
   └── update_log.txt
```

### **Verificações de Segurança**
- ✅ Verifica se é repositório Git válido
- ✅ Confirma com usuário antes de atualizar
- ✅ Backup automático antes de qualquer mudança
- ✅ Log completo de todas as operações

## 🚀 **Distribuição**

### **Para o Windows:**
1. **Copie apenas:** `atualizar_sistema.bat`
2. **Instrução:** "Execute como administrador"
3. **Coloque na pasta:** Sistema IAAM

### **Como .exe (Alternativa):**
1. Execute: `python3 criar_exe_updater.py`
2. Copie: `dist/AtualizadorIAAM.exe`
3. Distribua o executável único

## 📝 **Exemplo de Uso no Windows**

```cmd
C:\SistemaIAAM> atualizar_sistema.bat

=======================================================
           SISTEMA DE ATUALIZACAO IAAM
=======================================================

[INFO] Iniciando processo de atualizacao...
[INFO] Repositorio: https://github.com/kalebecaldas/sistema_senhas_web2.git
[INFO] Backup sera salvo em: backup_20251002_150045

[OK] Repositorio Git valido detectado.

[INFO] Criando backup de seguranca...
[OK] Backup criado em: backup_20251002_150045

[INFO] Verificando atualizacoes disponiveis...
[INFO] Encontradas 1 atualizacoes disponiveis.

[INFO] Commits pendentes:
  - d86a147: Teste de Att

Deseja atualizar o sistema? (S/N): S

[INFO] Iniciando atualizacao...
remote: Counting objects: X, done.
remote: Compressing objects: XX% (X/X), done.
remote: Total X (delta X), reused X (delta X), done.
   app/services.py | 5 +++--
   1 file changed, 3 insertions(+), 2 deletions(-)

[OK] Codigo atualizado com sucesso!

[INFO] Atualizando dependencias Python...
Processing Python dependencies...
[OK] Dependencias atualizadas!

======================================================
           ATUALIZACAO CONCLUIDA COM SUCESSO!
======================================================

Deseja reiniciar o sistema automaticamente? (S/N):
```

## 💡 **Dicas Importantes**

### **Para Produção:**
- ✅ Teste sempre primeiro em ambiente de desenvolvimento
- ✅ Mantenha backups regulares
- ✅ Verifique logs após atualizações
- ✅ Configure acesso automático ao Git

### **Para Desenvolvimento:**
- 🔧 Use `--auto` para atualização sem confirmação
- 🔧 Modifique URL do repositório se necessário
- 🔧 Adicione validações específicas para seu ambiente

### **Troubleshooting:**
- ❌ **Git não encontrado:** Instale Git para Windows
- ❌ **Python não encontrado:** Configure PATH do Python
- ❌ **Permissões:** Execute como administrador
- ❌ **Rede:** Verifique acesso ao GitHub

## 📞 **Suporte**

- 📁 **Logs:** Verifique pasta `backup_YYYYMMDD_HHMMSS/`
- 🔍 **Debug:** Execute com `python3 atualizador_autonomo.py --auto`
- 🛡️ **Backup:** Sempre restaure se algo der errado
- 📧 **Contato:** Sistema IAAM
