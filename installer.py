#!/usr/bin/env python3
"""
Instalador do Sistema de Senhas IAAM
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

class SistemaInstaller:
    def __init__(self):
        self.project_name = "Sistema de Senhas IAAM"
        self.version = "1.0.0"
        self.python_version = "3.8"
        
    def print_banner(self):
        """Exibir banner do instalador"""
        print("=" * 60)
        print(f"    {self.project_name} - Versão {self.version}")
        print("=" * 60)
        print()
    
    def check_python_version(self):
        """Verificar versão do Python"""
        print("🔍 Verificando versão do Python...")
        
        if sys.version_info < (3, 8):
            print(f"❌ Erro: Python {self.python_version} ou superior é necessário")
            print(f"   Versão atual: {sys.version}")
            return False
        
        print(f"✅ Python {sys.version} - OK")
        return True
    
    def check_git(self):
        """Verificar se o Git está instalado"""
        print("🔍 Verificando Git...")
        
        try:
            result = subprocess.run(['git', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ {result.stdout.strip()} - OK")
                return True
        except FileNotFoundError:
            pass
        
        print("❌ Git não encontrado. Instale o Git primeiro.")
        return False
    
    def create_virtual_environment(self):
        """Criar ambiente virtual"""
        print("🔧 Criando ambiente virtual...")
        
        if os.path.exists('venv'):
            print("⚠️  Ambiente virtual já existe")
            return True
        
        try:
            subprocess.run([sys.executable, '-m', 'venv', 'venv'], check=True)
            print("✅ Ambiente virtual criado")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao criar ambiente virtual: {e}")
            return False
    
    def install_dependencies(self):
        """Instalar dependências"""
        print("📦 Instalando dependências...")
        
        # Determinar o pip correto para o ambiente virtual
        if os.name == 'nt':  # Windows
            pip_path = 'venv\\Scripts\\pip'
        else:  # Unix/Linux/macOS
            pip_path = 'venv/bin/pip'
        
        try:
            # Atualizar pip
            subprocess.run([pip_path, 'install', '--upgrade', 'pip'], check=True)
            
            # Instalar dependências
            subprocess.run([pip_path, 'install', '-r', 'requirements.txt'], check=True)
            print("✅ Dependências instaladas")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao instalar dependências: {e}")
            return False
    
    def setup_database(self):
        """Configurar banco de dados"""
        print("🗄️  Configurando banco de dados...")
        
        try:
            # Criar diretório instance se não existir
            os.makedirs('instance', exist_ok=True)
            
            # Executar script de criação do banco
            if os.name == 'nt':  # Windows
                python_path = 'venv\\Scripts\\python'
            else:  # Unix/Linux/macOS
                python_path = 'venv/bin/python'
            
            subprocess.run([python_path, 'recriar_banco.py'], check=True)
            print("✅ Banco de dados configurado")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao configurar banco de dados: {e}")
            return False
    
    def create_startup_scripts(self):
        """Criar scripts de inicialização"""
        print("🚀 Criando scripts de inicialização...")
        
        # Script para Windows
        if os.name == 'nt':
            with open('iniciar_sistema.bat', 'w', encoding='utf-8') as f:
                f.write('@echo off\n')
                f.write('echo Iniciando Sistema de Senhas IAAM...\n')
                f.write('call venv\\Scripts\\activate\n')
                f.write('python run.py\n')
                f.write('pause\n')
        
        # Script para Unix/Linux/macOS
        else:
            with open('iniciar_sistema.sh', 'w') as f:
                f.write('#!/bin/bash\n')
                f.write('echo "Iniciando Sistema de Senhas IAAM..."\n')
                f.write('source venv/bin/activate\n')
                f.write('python run.py\n')
            
            # Tornar executável
            os.chmod('iniciar_sistema.sh', 0o755)
        
        print("✅ Scripts de inicialização criados")
        return True
    
    def create_directories(self):
        """Criar diretórios necessários"""
        print("📁 Criando diretórios...")
        
        directories = [
            'backups',
            'logs',
            'uploads'
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
        
        print("✅ Diretórios criados")
        return True
    
    def create_config_file(self):
        """Criar arquivo de configuração padrão"""
        print("⚙️  Criando configuração padrão...")
        
        config_content = '''# Configuração do Sistema de Senhas IAAM
SECRET_KEY = 'sua-chave-secreta-aqui'
DATABASE_URI = 'sqlite:///instance/sistema.db'
DEBUG = True
PORT = 5003
HOST = '0.0.0.0'

# Configurações do Display
DISPLAY_TITLE = 'Sistema IAAM'
DISPLAY_SUBTITLE = 'Aguarde ser chamado'
DISPLAY_FONT_SIZE = '48px'
DISPLAY_BACKGROUND_COLOR = '#1a1a1a'
DISPLAY_TEXT_COLOR = '#ffffff'

# Configurações de Som
ENABLE_SOUND = True
SOUND_FILE = 'static/audio/beep.mp3'

# Configurações de Prioridade
PESO_NORMAL = 1
PESO_PREFERENCIAL = 3
TOLERANCIA_MINUTOS = 5
'''
        
        with open('app/config.py', 'w', encoding='utf-8') as f:
            f.write(config_content)
        
        print("✅ Arquivo de configuração criado")
        return True
    
    def run_installation(self):
        """Executar instalação completa"""
        self.print_banner()
        
        steps = [
            ("Verificar Python", self.check_python_version),
            ("Verificar Git", self.check_git),
            ("Criar ambiente virtual", self.create_virtual_environment),
            ("Instalar dependências", self.install_dependencies),
            ("Criar diretórios", self.create_directories),
            ("Configurar banco de dados", self.setup_database),
            ("Criar configuração", self.create_config_file),
            ("Criar scripts de inicialização", self.create_startup_scripts)
        ]
        
        print("🚀 Iniciando instalação...\n")
        
        for step_name, step_func in steps:
            print(f"📋 {step_name}...")
            if not step_func():
                print(f"\n❌ Falha na etapa: {step_name}")
                print("Instalação interrompida.")
                return False
            print()
        
        print("🎉 Instalação concluída com sucesso!")
        print("\n📝 Próximos passos:")
        print("1. Execute o script de inicialização:")
        if os.name == 'nt':
            print("   iniciar_sistema.bat")
        else:
            print("   ./iniciar_sistema.sh")
        print("2. Acesse http://localhost:5003")
        print("3. Faça login com as credenciais padrão:")
        print("   Usuário: admin")
        print("   Senha: admin123")
        print("\n⚠️  IMPORTANTE: Altere a senha padrão após o primeiro login!")
        
        return True

def main():
    """Função principal"""
    installer = SistemaInstaller()
    
    try:
        installer.run_installation()
    except KeyboardInterrupt:
        print("\n\n❌ Instalação cancelada pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 