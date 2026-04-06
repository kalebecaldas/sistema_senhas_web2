#!/usr/bin/env python3
"""
Atualizador Autônomo do Sistema de Senhas IAAM
=============================================

Este script pode ser executado independentemente para atualizar o sistema.
Pode ser convertido em .exe usando PyInstaller para execução no Windows.

Uso:
    python atualizador_autonomo.py
    # ou após conversão em .exe:
    atualizador_autonomo.exe

Autor: Sistema IAAM
Data: 2025
"""

import os
import sys
import subprocess
import json
import shutil
import time
from datetime import datetime
from pathlib import Path
import argparse


class AutoUpdater:
    """Classe para atualização automática do sistema"""
    
    def __init__(self, repo_url="https://github.com/kalebecaldas/sistema_senhas_web2.git"):
        self.repo_url = repo_url
        self.project_dir = Path.cwd()
        self.backup_dir = None
        self.is_windows = os.name == 'nt'
        
        # Configurações específicas do Windows/Mac
        self.python_cmd = self._get_python_cmd()
        self.pip_cmd = f"{self.python_cmd} -m pip"
        
        print("🚀 Atualizador Autônomo IAAM")
        print("=" * 40)
        print(f"📂 Diretório: {self.project_dir}")
        print(f"🖥️  Sistema: {'Windows' if self.is_windows else 'macOS/Linux'}")
        print(f"🐍 Python: {self.python_cmd}")
        print(f"📦 Pip: {self.pip_cmd}")
        print("=" * 40)
    
    def _get_python_cmd(self):
        """Determina o comando Python correto baseado no sistema"""
        if self.is_windows:
            # Tenta python, depois python3, depois py
            for cmd in ['python', 'python3', 'py']:
                try:
                    result = subprocess.run([cmd, '--version'], 
                                          capture_output=True, text=True)
                    if result.returncode == 0:
                        return cmd
                except FileNotFoundError:
                    continue
        else:
            # Para Unix-like systems
            for cmd in ['python3', 'python']:
                try:
                    result = subprocess.run([cmd, '--version'], 
                                          capture_output=True, text=True)
                    if result.returncode == 0:
                        return cmd
                except FileNotFoundError:
                    continue
        
        raise RuntimeError("❌ Python não encontrado no sistema")
    
    def check_git_repo(self):
        """Verifica se estamos em um repositório Git válido"""
        print("🔍 Verificando repositório Git...")
        
        try:
            result = subprocess.run(['git', 'status'], 
                                  cwd=self.project_dir,
                                  capture_output=True, text=True)
            if result.returncode != 0:
                print("❌ Este diretório não é um repositório Git válido!")
                return False
            
            # Verificar remote origin
            result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                                  cwd=self.project_dir,
                                  capture_output=True, text=True)
            
            current_remote = result.stdout.strip()
            if current_remote != self.repo_url:
                print(f"⚠️  Remote atual: {current_remote}")
                print(f"⚠️  Esperado: {self.repo_url}")
                print("⚠️  Verificando se é compatível...")
                
                # Permitir variações (com ou sem .git no final)
                expected_base = "kalebecaldas/sistema_senhas_web2"
                if expected_base not in current_remote:
                    print("❌ Repositório não autorizado!")
                    return False
                else:
                    print("✅ Repositório compatível detectado")
            
            print("✅ Repositório Git válido")
            return True
            
        except FileNotFoundError:
            print("❌ Git não encontrado no sistema!")
            return False
    
    def create_backup(self):
        """Cria backup dos arquivos importantes"""
        print("💾 Criando backup de segurança...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_dir = self.project_dir / f"backup_{timestamp}"
        
        try:
            self.backup_dir.mkdir(exist_ok=True)
            
            # Arquivos importantes para backup
            important_files = [
                'instance/sistema.db',
                'app/config.py', 
                'VERSION',
                'requirements.txt',
                'run.py'
            ]
            
            backed_up = []
            for file_path in important_files:
                source = self.project_dir / file_path
                if source.exists():
                    dest = self.backup_dir / source.name
                    shutil.copy2(source, dest)
                    backed_up.append(file_path)
            
            print(f"✅ Backup criado em: {self.backup_dir}")
            print(f"📋 Arquivos salvos: {', '.join(backed_up)}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao criar backup: {e}")
            return False
    
    def check_updates(self):
        """Verifica se há atualizações disponíveis"""
        print("🔍 Verificando atualizações disponíveis...")
        
        try:
            # Fetch remoto
            result = subprocess.run(['git', 'fetch', 'origin'], 
                                  cwd=self.project_dir,
                                  capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"⚠️  Falha no fetch: {result.stderr}")
                return 0
            
            # Contar commits à frente
            result = subprocess.run(['git', 'rev-list', 'HEAD..origin/main', '--count'], 
                                  cwd=self.project_dir,
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                commits_ahead = int(result.stdout.strip() or '0')
                
                if commits_ahead > 0:
                    print(f"📥 Encontradas {commits_ahead} atualizações disponíveis")
                    
                    # Mostrar commits pendentes
                    self._show_pending_commits()
                else:
                    print("✅ Sistema já está atualizado!")
                
                return commits_ahead
            else:
                print(f"❌ Erro ao verificar commits: {result.stderr}")
                return 0
                
        except Exception as e:
            print(f"❌ Erro ao verificar atualizações: {e}")
            return 0
    
    def _show_pending_commits(self):
        """Mostra os commits pendentes"""
        try:
            result = subprocess.run(['git', 'log', 'HEAD..origin/main', '--oneline'], 
                                  cwd=self.project_dir,
                                  capture_output=True, text=True)
            
            if result.returncode == 0 and result.stdout.strip():
                print("📋 Commits pendentes:")
                lines = result.stdout.strip().split('\n')[:5]  # Últimos 5
                for line in lines:
                    print(f"   • {line}")
        except Exception:
            pass
    
    def update_system(self):
        """Executa a atualização do sistema"""
        print("⬇️  Atualizando sistema...")
        
        try:
            # Verificar se há mudanças locais
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  cwd=self.project_dir,
                                  capture_output=True, text=True)
            
            if result.stdout.strip():
                print("📝 Mudanças locais detectadas, fazendo stash...")
                stash_result = subprocess.run(['git', 'stash'], 
                                            cwd=self.project_dir,
                                            capture_output=True, text=True)
                
                if stash_result.returncode == 0:
                    print("✅ Mudanças locais salvas em stash")
                else:
                    print(f"⚠️  Aviso no stash: {stash_result.stderr}")
            
            # Git pull
            result = subprocess.run(['git', 'pull', 'origin', 'main'], 
                                  cwd=self.project_dir,
                                  capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"❌ Falha na atualização: {result.stderr}")
                print(f"📄 Saída: {result.stdout}")
                
                # Tentar aplicar stash novamente se deu erro
                pop_result = subprocess.run(['git', 'stash', 'pop'], 
                                           cwd=self.project_dir,
                                           capture_output=True, text=True)
                return False
            
            print("✅ Código atualizado com sucesso!")
            print(f"📄 Saída Git: {result.stdout}")
            
            # Aplicar stash novamente se havia mudanças
            if stash_result.returncode == 0:
                print("🔄 Restaurando mudanças locais...")
                subprocess.run(['git', 'stash', 'pop'], 
                             cwd=self.project_dir,
                             capture_output=True, text=True)
            
            return True
            
        except Exception as e:
            print(f"❌ Erro durante atualização: {e}")
            return False
    
    def update_dependencies(self):
        """Atualiza dependências Python"""
        print("📦 Atualizando dependências Python...")
        
        try:
            # Verificar se existe requirements.txt
            req_file = self.project_dir / 'requirements.txt'
            if not req_file.exists():
                print("⚠️  requirements.txt não encontrado")
                return False
            
            # Atualizar dependências
            cmd = f"{self.pip_cmd} install -r requirements.txt --upgrade"
            result = subprocess.run(cmd.split(), 
                                  cwd=self.project_dir,
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Dependências atualizadas!")
                return True
            else:
                print(f"❌ Erro ao atualizar dependências: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao atualizar dependências: {e}")
            return False
    
    def save_update_log(self):
        """Salva log da atualização na pasta backup"""
        if not self.backup_dir:
            return
        
        try:
            log_file = self.backup_dir / 'update_log.txt'
            timestamp = datetime.now().isoformat()
            
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write(f"Log de Atualização IAAM\n")
                f.write(f"Data: {timestamp}\n")
                f.write(f"Repositório: {self.repo_url}\n")
                f.write(f"Sistema: {'Windows' if self.is_windows else 'Unix'}\n")
                f.write(f"Python: {sys.version}\n")
                f.write("=" * 50 + "\n")
            
            print(f"📝 Log salvo em: {log_file}")
            
        except Exception as e:
            print(f"⚠️  Erro ao salvar log: {e}")
    
    def main(self, auto_confirm=False):
        """Função principal do atualizador"""
        start_time = datetime.now()
        
        try:
            # 1. Verificar repositório Git
            if not self.check_git_repo():
                return False
            
            # 2. Verificar atualizações
            commits_ahead = self.check_updates()
            
            if commits_ahead == 0:
                print("🎯 Sistema está atualizado!")
                return True
            
            # 3. Confirmar atualização
            if not auto_confirm:
                response = input(f"\n❓ Deseja atualizar {commits_ahead} commit(s)? (S/N): ").strip().lower()
                if response not in ['s', 'sim', 'y', 'yes']:
                    print("⏹️  Atualização cancelada pelo usuário")
                    return False
            
            print("\n🚀 Iniciando processo de atualização...")
            
            # 4. Criar backup
            if not self.create_backup():
                print("⚠️  Continuando sem backup...")
            
            # 5. Atualizar sistema
            if not self.update_system():
                return False
            
            # 6. Atualizar dependências
            self.update_dependencies()
            
            # 7. Salvar log
            self.save_update_log()
            
            # Resultado
            end_time = datetime.now()
            duration = end_time - start_time
            
            print("\n" + "=" * 50)
            print("🎉 ATUALIZAÇÃO CONCLUÍDA COM SUCESSO!")
            print("=" * 50)
            print(f"⏱️  Duração: {duration.total_seconds():.1f} segundos")
            print(f"📁 Backup salvo em: {self.backup_dir}")
            print(f"📊 Commits atualizados: {commits_ahead}")
            print("\n💡 Próximos passos:")
            print("   1. Reinicie o sistema de senhas")
            print("   2. Verifique se tudo está funcionando")
            print("   3. Em caso de problemas, restaure o backup")
            
            return True
            
        except KeyboardInterrupt:
            print("\n⏹️  Atualização interrompida pelo usuário")
            return False
        except Exception as e:
            print(f"\n❌ Erro fatal: {e}")
            return False


def main():
    """Função principal do script"""
    parser = argparse.ArgumentParser(description='Atualizador Autônomo IAAM')
    parser.add_argument('--auto', action='store_true', 
                       help='Atualização automática sem confirmação')
    parser.add_argument('--repo', default='https://github.com/kalebecaldas/sistema_senhas_web2.git',
                       help='URL do repositório Git')
    
    args = parser.parse_args()
    
    try:
        updater = AutoUpdater(args.repo)
        success = updater.main(auto_confirm=args.auto)
        
        if not args.auto:
            input("\n⏸️  Pressione Enter para finalizar...")
        
        sys.exit(0 if success else 1)
        
    except Exception as e:
        print(f"💥 Erro crítico: {e}")
        input("\n⏸️  Pressione Enter para finalizar...")
        sys.exit(1)


if __name__ == '__main__':
    main()
