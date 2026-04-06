#!/usr/bin/env python3
"""
Script para criar arquivo .exe do atualizador
===========================================

Este script cria um arquivo .exe do atualizador usando PyInstaller.

Uso:
    python criar_exe_updater.py

Pré-requisitos:
    pip install pyinstaller
"""

import subprocess
import sys
import os
from pathlib import Path


def install_pyinstaller():
    """Instala PyInstaller se não estiver presente"""
    try:
        import PyInstaller
        print("✅ PyInstaller já está instalado")
        return True
    except ImportError:
        print("📦 Instalando PyInstaller...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
            print("✅ PyInstaller instalado com sucesso")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao instalar PyInstaller: {e}")
            return False


def create_exe():
    """Cria o arquivo .exe do atualizador"""
    print("🔨 Criando executável do atualizador...")
    
    # Comando PyInstaller
    cmd = [
        'pyinstaller',
        '--onefile',  # Arquivo único
        '--windowed', # Sem console no Windows
        '--name=AtualizadorIAAM', # Nome do executável
        '--icon=app/static/img/logo.ico' if Path('app/static/img/logo.ico').exists() else '--icon=NONE',
        'atualizador_autonomo.py'
    ]
    
    try:
        print(f"🚀 Executando: {' '.join(cmd)}")
        result = subprocess.run(cmd, text=True, capture_output=True)
        
        if result.returncode == 0:
            print("✅ Executável criado com sucesso!")
            
            # Verificar se foi criado
            exe_path = Path('dist/AtualizadorIAAM.exe')
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print(f"📁 Arquivo: {exe_path}")
                print(f"📏 Tamanho: {size_mb:.1f} MB")
                
                # Criar instruções
                create_instructions()
                
                return True
            else:
                print("❌ Executável não encontrado após criação")
                return False
        else:
            print(f"❌ Erro na criação: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Erro durante criação: {e}")
        return False


def create_instructions():
    """Cria arquivo de instruções"""
    instructions = """
INSTRUÇÕES DE USO - ATUALIZADOR IAAM
====================================

📁 Arquivos criados:
   • AtualizadorIAAM.exe (Executável principal)
   • atualizar_sistema.bat (Script alternativo)
   • atualizador_autonomo.py (Script Python original)

🚀 Como usar o AtualizadorIAAM.exe:

   1. Copie o AtualizadorIAAM.exe para o computador do sistema
   2. Coloque-o dentro da pasta do projeto IAAM
   3. Execute clicando duas vezes no arquivo
   4. O atualizador fará tudo automaticamente:
      ✓ Backup de segurança
      ✓ Verificação de atualizações
      ✓ Download das atualizações
      ✓ Atualização de dependências
      ✓ Log detalhado

🎯 Recursos:
   • Funciona offline (depois de conectado)
   • Backup automático antes da atualização
   • Verificação detalhada de atualizações
   • Atualização de dependências Python
   • Log completo das operações

💡 Dicas:
   • Execute como administrador no Windows para evitar problemas de permissão
   • Mantenha backup das configurações importantes
   • Teste sempre após atualização

📞 Suporte:
   • Verifique os logs em backup_YYYYMMDD_HHMMSS/update_log.txt
   • Em caso de problemas, restaure o backup manualmente
"""
    
    try:
        with open('INSTRUCOES_ATUALIZADOR.txt', 'w', encoding='utf-8') as f:
            f.write(instructions)
        print("📝 Instruções salvas em: INSTRUCOES_ATUALIZADOR.txt")
    except Exception as e:
        print(f"⚠️  Erro ao criar instruções: {e}")


def main():
    """Função principal"""
    print("🔧 Criador de Executável - Atualizador IAAM")
    print("=" * 50)
    
    # Verificar se está no diretório correto
    if not Path('atualizador_autonomo.py').exists():
        print("❌ Arquivo atualizador_autonomo.py não encontrado!")
        print("   Execute este script no diretório do projeto.")
        return False
    
    # Instalar PyInstaller
    if not install_pyinstaller():
        return False
    
    print("\n" + "=" * 50)
    
    # Criar executável
    if create_exe():
        print("\n" + "=" * 50)
        print("🎉 Executável criado com sucesso!")
        print("📦 Agora você pode distribuir apenas o AtualizadorIAAM.exe")
        return True
    else:
        print("\n❌ Falha ao criar executável")
        return False


if __name__ == '__main__':
    try:
        success = main()
        
        if not success:
            print("\n⚠️  Processo com problemas. Verifique os erros acima.")
        
        input("\n⏸️  Pressione Enter para finalizar...")
        
    except KeyboardInterrupt:
        print("\n⏹️  Cancelado pelo usuário")
    except Exception as e:
        print(f"\n💥 Erro: {e}")
        input("\n⏸️  Pressione Enter para finalizar...")
