# Sistema de Senhas IAAM - Instalação Windows

Este guia explica como instalar o Sistema de Senhas IAAM no Windows usando os scripts automatizados.

## 📋 Pré-requisitos

- Windows 10 ou superior
- Conexão com a internet
- Acesso de administrador (recomendado)

## 🚀 Instalação

### Opção 1: Instalação Completa (Recomendada)

Se você não tem Python ou Git instalados, use o script de instalação completa:

1. **Baixe os arquivos de instalação:**
   - `instalar_sistema.bat` - Instalação completa
   - `instalar_rapido.bat` - Instalação rápida

2. **Execute o instalador:**
   ```cmd
   instalar_sistema.bat
   ```

3. **O script irá:**
   - ✅ Verificar e instalar Python (se necessário)
   - ✅ Verificar e instalar Git (se necessário)
   - ✅ Baixar o sistema do GitHub
   - ✅ Criar ambiente virtual
   - ✅ Instalar dependências
   - ✅ Configurar banco de dados
   - ✅ Criar scripts de inicialização
   - ✅ Criar atalho no desktop

### Opção 2: Instalação Rápida

Se você já tem Python e Git instalados:

1. **Execute o script rápido:**
   ```cmd
   instalar_rapido.bat
   ```

## 🔧 Configuração do Repositório

**IMPORTANTE:** Antes de usar os scripts, você precisa:

1. **Criar um repositório no GitHub** com o código do sistema
2. **Editar os scripts** e alterar a URL do repositório:

   Abra `instalar_sistema.bat` e `instalar_rapido.bat` e altere:
   ```batch
   set "REPO_URL=https://github.com/SEU-USUARIO/sistema_senhas_web2.git"
   ```
   
   Substitua `SEU-USUARIO` pelo seu nome de usuário do GitHub.

## 📁 Estrutura Após Instalação

Após a instalação, você terá:

```
📁 Pasta de Instalação/
├── 📁 sistema_senhas_web2/     # Código do sistema
├── 📄 instalar_sistema.bat     # Instalador completo
├── 📄 instalar_rapido.bat      # Instalador rápido
├── 📄 Iniciar Sistema.bat      # Script para rodar o sistema
└── 📄 install_log.txt          # Log da instalação
```

## 🚀 Como Usar o Sistema

### Iniciar o Sistema

1. **Duplo clique** no arquivo `Iniciar Sistema.bat` ou
2. **Duplo clique** no atalho no desktop

### Acessar o Sistema

- 🌐 **URL:** http://localhost:5003
- 👤 **Usuário:** admin
- 🔑 **Senha:** admin123

## 🔄 Atualizações

Para atualizar o sistema:

1. **Execute novamente** o script de instalação
2. **Ou manualmente:**
   ```cmd
   cd sistema_senhas_web2
   git pull origin main
   call venv\Scripts\activate.bat
   pip install -r requirements.txt
   ```

## 🛠️ Solução de Problemas

### Erro: "Python não encontrado"
- Execute `instalar_sistema.bat` para instalação completa
- Ou instale Python manualmente: https://python.org

### Erro: "Git não encontrado"
- Execute `instalar_sistema.bat` para instalação completa
- Ou instale Git manualmente: https://git-scm.com

### Erro: "Repositório não encontrado"
- Verifique se a URL do repositório está correta nos scripts
- Certifique-se de que o repositório é público
- Verifique sua conexão com a internet

### Erro: "Porta 5003 em uso"
- Feche outros programas que possam estar usando a porta
- Ou altere a porta no arquivo `run.py`

### Erro: "Dependências não instaladas"
- Verifique sua conexão com a internet
- Execute: `pip install -r requirements.txt`

## 📞 Suporte

Se encontrar problemas:

1. **Verifique o log:** `install_log.txt`
2. **Execute em modo administrador**
3. **Desative antivírus temporariamente**
4. **Verifique firewall do Windows**

## 🔒 Segurança

- ✅ O sistema roda localmente (localhost)
- ✅ Ambiente virtual isolado
- ✅ Dependências verificadas
- ✅ Logs de instalação

## 📝 Notas

- O sistema usa SQLite como banco de dados
- Todos os dados ficam na pasta `instance/`
- O ambiente virtual fica na pasta `venv/`
- Logs de instalação ficam em `install_log.txt`

---

**Desenvolvido para IAAM** - Sistema de Gerenciamento de Senhas 