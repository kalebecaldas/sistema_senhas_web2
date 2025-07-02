# Sistema de Senhas IAAM

Sistema de gerenciamento de senhas para atendimento com interface web moderna, sistema de atualizações automáticas e instalação simplificada.

## 🚀 Instalação Rápida

### Pré-requisitos
- Python 3.8 ou superior
- Git

### Instalação Automática
```bash
# Clone o repositório
git clone https://github.com/seu-usuario/sistema_senhas_web2.git
cd sistema_senhas_web2

# Execute o instalador
python installer.py
```

### Instalação Manual
```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/sistema_senhas_web2.git
cd sistema_senhas_web2

# 2. Crie ambiente virtual
python -m venv venv

# 3. Ative o ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 4. Instale dependências
pip install -r requirements.txt

# 5. Configure o banco de dados
python recriar_banco.py

# 6. Execute o sistema
python run.py
```

## 🎯 Funcionalidades

### ✨ Principais Recursos
- **Interface moderna e responsiva**
- **Sistema de prioridades inteligente**
- **Display de senhas em tempo real**
- **Relatórios detalhados (PDF/Excel)**
- **Sistema de atualizações automáticas**
- **Backup automático de configurações**
- **TTS (Text-to-Speech) integrado**

### 📊 Dashboard e Relatórios
- Estatísticas em tempo real
- Gráficos interativos
- Relatórios personalizados
- Exportação em PDF e Excel
- Análise de tempo de espera

### 🔧 Configurações Avançadas
- Personalização do display
- Configuração de prioridades
- Sistema de som configurável
- Backup automático

## 🔄 Sistema de Atualizações

O sistema inclui um sistema de atualizações automáticas via Git:

### Verificar Atualizações
- Acesse **Configurações > Atualizações**
- Clique em **"Verificar Atualizações"**
- O sistema mostrará se há novas versões disponíveis

### Atualizar Sistema
- Clique em **"Atualizar Sistema"**
- O sistema fará backup automático das configurações
- Baixará e aplicará as atualizações
- Reiniciará automaticamente

### Informações do Sistema
- Versão atual
- Informações do Git (commit, branch)
- Status da plataforma
- Log de atualizações

## 🛠️ Configuração

### Credenciais Padrão
- **Usuário:** admin
- **Senha:** admin123

⚠️ **IMPORTANTE:** Altere a senha padrão após o primeiro login!

### Configurações do Display
- Título e subtítulo personalizáveis
- Cores e fontes configuráveis
- Som de notificação
- Vídeo de fundo

### Configurações de Prioridade
- Peso para senhas normais e preferenciais
- Tolerância de tempo para preferenciais
- Sistema de alternância automática

## 📁 Estrutura do Projeto

```
sistema_senhas_web2/
├── app/                    # Aplicação Flask
│   ├── static/            # Arquivos estáticos
│   ├── templates/         # Templates HTML
│   ├── models.py          # Modelos do banco
│   ├── routes.py          # Rotas da aplicação
│   └── version.py         # Sistema de versionamento
├── backups/               # Backups automáticos
├── instance/              # Banco de dados
├── logs/                  # Logs do sistema
├── VERSION                # Arquivo de versão
├── installer.py           # Instalador automático
├── requirements.txt       # Dependências Python
└── run.py                 # Script de inicialização
```

## 🔧 Desenvolvimento

### Estrutura de Versionamento
- **VERSION:** Contém a versão atual do sistema
- **app/version.py:** Gerenciador de versões e atualizações
- **Git:** Controle de versão e atualizações automáticas

### Adicionando Novas Funcionalidades
1. Desenvolva a funcionalidade
2. Atualize a versão no arquivo `VERSION`
3. Faça commit das mudanças
4. Push para o repositório

### Backup Automático
O sistema faz backup automático antes de cada atualização:
- Configurações do sistema
- Banco de dados
- Arquivo de versão

## 🚀 Inicialização

### Scripts de Inicialização
Após a instalação, use os scripts criados:

**Windows:**
```bash
iniciar_sistema.bat
```

**Linux/macOS:**
```bash
./iniciar_sistema.sh
```

### Acesso ao Sistema
- **URL:** http://localhost:5003
- **Painel:** http://localhost:5003/painel
- **Display:** http://localhost:5003/display

## 📝 Changelog

### Versão 1.0.0
- ✅ Sistema de atualizações automáticas
- ✅ Instalador automático
- ✅ Dashboard moderno
- ✅ Relatórios em PDF/Excel
- ✅ Sistema de prioridades
- ✅ TTS integrado
- ✅ Interface responsiva
- ✅ Backup automático

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 🆘 Suporte

Para suporte técnico ou dúvidas:
- Abra uma issue no GitHub
- Consulte a documentação
- Verifique os logs do sistema

---

**Sistema de Senhas IAAM** - Versão 1.0.0