# 🔄 COMO EXECUTAR O ATUALIZADOR

## ⚠️ **INSTRUÇÕES IMPORTANTE**

Certifique-se de executar o atualizador **DENTRO DA PASTA DO PROJETO**, não em pasta separada.

---

## 🖥️ **NO WINDOWS:**

### **🚀 OPÇÃO 1 - SCRIPT COMPLETO (RECOMENDADO):**
```cmd
# Navegue até a pasta do projeto IAAM
cd "C:\caminho\para\sistema_senhas_web"

# Execute o script completo (instala Git se necessário)
atualizar_sistema_completo.bat
```

### **📦 OPÇÃO 2 - SÓ INSTALAR GIT:**
```cmd
# Se só quiser instalar o Git primeiro
instalar_git.bat

# Depois execute o atualizador
atualizar_sistema_v2.bat
```

### **🔧 OPÇÃO 3 - Script Manual:**
```cmd
# Script otimizado (Git deve estar instalado)
atualizar_sistema_v2.bat

# Ou método tradicional
atualizar_sistema.bat
```

### **🐍 OPÇÃO 4 - Atualizador Python:**
```cmd
# Execute o script Python
python atualizador_autonomo.py --auto
```

---

## 🍎 **NO MACOS/LINUX:**

```bash
# Navegue até a pasta do projeto IAAM
cd "/path/to/sistema_senhas_web"

# Execute o atualizador Python
python3 atualizador_autonomo.py --auto
```

---

## ❌ **ERRO COMUM: "Repositório não é válido"**

### **🩺 DIAGNÓSTICO PRIMEIRO:**
```cmd
# Execute este diagnóstico completo
diagnostico_git.bat
```

### **🔧 SOLUÇÕES:**

**OPÇÃO 1 - Script Otimizado:**
```cmd
# Use a versão v2 do atualizador (mais robusta)
atualizar_sistema_v2.bat
```

**OPÇÃO 2 - Verificação Manual:**
1. **Abra o terminal/Prompt**
2. **Vá até a pasta do projeto** (onde estão os arquivos `app/`, `run.py`, etc.)
3. **Execute o diagnóstico:**
   ```cmd
   diagnostico_git.bat
   ```
   
4. **Verificar configuração Git:**
   ```cmd
   git remote -v
   ```
   
5. **Deve mostrar:**
   ```
   origin  https://github.com/kalebecaldas/sistema_senhas_web2.git (fetch)
   origin  https://github.com/kalebecaldas/sistema_senhas_web2.git (push)
   ```

**OPÇÃO 0 - Correção Automática:**
```cmd
# Limpar e reconfigurar Git
git remote remove origin
git remote add origin https://github.com/kalebecaldas/sistema_senhas_web2.git
git fetch origin
git branch --set-upstream-to=origin/main main
```

---

## 🔧 **CORREÇÃO RÁPIDA:**

Se ainda não funcionar, execute estes comandos na pasta do projeto:

```cmd
# Verificar configuração
git remote get-url origin

# Se estiver diferente, corrigir:
git remote set-url origin https://github.com/kalebecaldas/sistema_senhas_web2.git

# Testar conexão
git fetch origin --dry-run

# Tentar novamente o atualizador
atualizar_sistema.bat
```

---

## ✅ **SUCESSO:**

Quando funcionar, você verá:
```
✅ Repositório Git válido
✅ Sistema já está atualizado!
```

---

## 🆘 **AINDA COM PROBLEMAS?**

Verifique se:
- ✅ Está executando na pasta correta do projeto
- ✅ Git está instalado (`git --version`)
- ✅ Tem conexão com internet
- ✅ A pasta contém os arquivos `app/`, `run.py`, `.git/`

Se ainda não funcionar, execute `teste_git.bat` primeiro para diagnosticar.

---

## 🚀 **INICIAR O SISTEMA**

### **🍎 NO MACOS/LINUX:**

**OPÇÃO 1 - Normal (com verificações):**
```bash
./iniciar_sistema.sh
```

**OPÇÃO 2 - Rápido (sem verificações):**
```bash
./iniciar_rapido.sh
```

**OPÇÃO 3 - Manual:**
```bash
source venv/bin/activate
python run.py
```

### **🖥️ NO WINDOWS:**

**OPÇÃO 1 - Normal (com verificações):**
```cmd
iniciar_sistema.bat
```

**OPÇÃO 2 - Rápido (sem verificações):**
```cmd
iniciar_rapido.bat
```

**OPÇÃO 3 - Manual:**
```cmd
venv\Scripts\activate.bat
python run.py
```

### **📋 Diferenças:**

- **Normal**: Verifica dependências e oferece instalação se necessário
- **Rápido**: Inicia diretamente, falha silenciosamente se algo estiver errado
- **Manual**: Controle total, sem verificações automáticas

---

## ❌ **ERRO: "Git não está instalado"**

### **🚀 SOLUÇÃO AUTOMÁTICA:**
```cmd
# Execute como administrador (botão direito)
atualizar_sistema_completo.bat
```

### **📦 SOLUÇÃO MANUAL:**
```cmd
# 1. Instalar apenas o Git
instalar_git.bat

# 2. Depois executar o atualizador
atualizar_sistema_v2.bat
```

### **🔗 INSTALAÇÃO MANUAL:**
1. **Baixe do site oficial:** https://git-scm.com/download/win
2. **Execute o instalador** como administrador
3. **Use configurações padrão** durante a instalação
4. **Execute novamente** o atualizador

### **⚡ INSTALAÇÃO RÁPIDA (PowerShell como Admin):**
```powershell
# Via winget (Windows 10/11)
winget install Git.Git

# Via chocolatey (se instalado)
choco install git -y
```
