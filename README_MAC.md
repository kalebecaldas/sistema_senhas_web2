# Sistema de Senhas - macOS

Este é um sistema de gerenciamento de senhas desenvolvido em Flask, adaptado para funcionar no macOS.

## Pré-requisitos

- macOS (testado no macOS 14+)
- Python 3.8 ou superior
- Terminal (aplicativo padrão do macOS)

## Instalação

1. **Abra o Terminal** (Applications > Utilities > Terminal)

2. **Navegue até a pasta do projeto:**
   ```bash
   cd /caminho/para/sistema_senhas_web2
   ```

3. **Crie um ambiente virtual:**
   ```bash
   python3 -m venv venv
   ```

4. **Ative o ambiente virtual:**
   ```bash
   source venv/bin/activate
   ```

5. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

## Como Usar

### Método 1: Configuração inicial (Primeira vez)

Execute o script de configuração que fará tudo automaticamente:
```bash
./setup_mac.sh
```

### Método 2: Iniciar com navegador automático (Recomendado)

O navegador será aberto automaticamente:
```bash
./iniciar_com_navegador.sh
```

### Método 3: Iniciar manualmente

1. **Execute o script básico:**
   ```bash
   ./iniciar_sistema.sh
   ```

2. **Ou execute manualmente:**
   ```bash
   source venv/bin/activate
   python run.py
   ```

### Método 4: Execução manual

1. **Ative o ambiente virtual:**
   ```bash
   source venv/bin/activate
   ```

2. **Execute o servidor:**
   ```bash
   python run.py
   ```

## Acessando o Sistema

Após iniciar o servidor, abra seu navegador e acesse:
- **http://localhost:5003** ou
- **http://127.0.0.1:5003**

## Funcionalidades

- Gerenciamento de senhas
- Sistema de prioridades
- Display de senhas
- Autenticação de usuários
- Interface web responsiva

## Solução de Problemas

### Erro: "command not found: python3"
- Instale o Python 3 através do Homebrew:
  ```bash
  brew install python3
  ```

### Erro: "permission denied"
- Execute: `chmod +x iniciar_sistema.sh`

### Erro: "port already in use"
- Encerre outros processos na porta 5003 ou altere a porta no arquivo `run.py`

## Encerrando o Servidor

Para parar o servidor, pressione `Ctrl + C` no terminal.

## Desenvolvimento

Para desenvolvimento, recomenda-se:
- Usar um editor como VS Code ou PyCharm
- Manter o ambiente virtual ativo durante o desenvolvimento
- Testar regularmente as funcionalidades

## Suporte

Em caso de problemas, verifique:
1. Se todas as dependências estão instaladas
2. Se o ambiente virtual está ativo
3. Se não há conflitos de porta
4. Os logs no terminal para mensagens de erro 