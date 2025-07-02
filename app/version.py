"""
Módulo de versionamento do Sistema de Senhas IAAM
"""

import os
import subprocess
import requests
from datetime import datetime

class VersionManager:
    def __init__(self):
        self.version_file = 'VERSION'
        self.repo_url = 'https://github.com/seu-usuario/sistema_senhas_web2.git'  # Atualizar com o repositório real
        self.current_version = self.get_current_version()
    
    def get_current_version(self):
        """Obter versão atual do sistema"""
        try:
            with open(self.version_file, 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            return '1.0.0'
    
    def get_git_info(self):
        """Obter informações do Git"""
        try:
            # Hash do commit atual
            commit_hash = subprocess.check_output(
                ['git', 'rev-parse', '--short', 'HEAD'], 
                stderr=subprocess.DEVNULL
            ).decode('utf-8').strip()
            
            # Data do último commit
            commit_date = subprocess.check_output(
                ['git', 'log', '-1', '--format=%cd', '--date=short'], 
                stderr=subprocess.DEVNULL
            ).decode('utf-8').strip()
            
            # Branch atual
            branch = subprocess.check_output(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'], 
                stderr=subprocess.DEVNULL
            ).decode('utf-8').strip()
            
            return {
                'commit_hash': commit_hash,
                'commit_date': commit_date,
                'branch': branch,
                'is_git_repo': True
            }
        except (subprocess.CalledProcessError, FileNotFoundError):
            return {
                'commit_hash': 'N/A',
                'commit_date': 'N/A',
                'branch': 'N/A',
                'is_git_repo': False
            }
    
    def check_for_updates(self):
        """Verificar se há atualizações disponíveis"""
        try:
            # Buscar informações do repositório remoto
            subprocess.run(['git', 'fetch', 'origin'], 
                         stderr=subprocess.DEVNULL, 
                         stdout=subprocess.DEVNULL)
            
            # Verificar se há commits à frente
            ahead = subprocess.check_output(
                ['git', 'rev-list', 'HEAD..origin/main', '--count'], 
                stderr=subprocess.DEVNULL
            ).decode('utf-8').strip()
            
            # Verificar se há commits atrás
            behind = subprocess.check_output(
                ['git', 'rev-list', 'origin/main..HEAD', '--count'], 
                stderr=subprocess.DEVNULL
            ).decode('utf-8').strip()
            
            return {
                'has_updates': int(ahead) > 0,
                'commits_ahead': int(ahead),
                'commits_behind': int(behind),
                'last_check': datetime.now().isoformat()
            }
        except (subprocess.CalledProcessError, FileNotFoundError):
            return {
                'has_updates': False,
                'commits_ahead': 0,
                'commits_behind': 0,
                'last_check': datetime.now().isoformat(),
                'error': 'Não foi possível verificar atualizações'
            }
    
    def update_system(self):
        """Atualizar o sistema"""
        try:
            # Fazer backup das configurações
            self._backup_config()
            
            # Pull das atualizações
            result = subprocess.run(
                ['git', 'pull', 'origin', 'main'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                # Atualizar dependências se necessário
                self._update_dependencies()
                
                return {
                    'success': True,
                    'message': 'Sistema atualizado com sucesso!',
                    'output': result.stdout
                }
            else:
                return {
                    'success': False,
                    'message': 'Erro ao atualizar sistema',
                    'error': result.stderr
                }
        except Exception as e:
            return {
                'success': False,
                'message': 'Erro durante atualização',
                'error': str(e)
            }
    
    def _backup_config(self):
        """Fazer backup das configurações importantes"""
        import shutil
        from datetime import datetime
        
        backup_dir = f'backups/config_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
        os.makedirs(backup_dir, exist_ok=True)
        
        # Arquivos importantes para backup
        important_files = [
            'instance/sistema.db',
            'app/config.py',
            'VERSION'
        ]
        
        for file_path in important_files:
            if os.path.exists(file_path):
                shutil.copy2(file_path, backup_dir)
    
    def _update_dependencies(self):
        """Atualizar dependências Python"""
        try:
            subprocess.run(['pip', 'install', '-r', 'requirements.txt', '--upgrade'])
        except Exception:
            pass  # Ignorar erros de dependências
    
    def get_system_info(self):
        """Obter informações completas do sistema"""
        git_info = self.get_git_info()
        update_info = self.check_for_updates()
        
        return {
            'version': self.current_version,
            'git_info': git_info,
            'update_info': update_info,
            'system_info': {
                'python_version': self._get_python_version(),
                'platform': self._get_platform(),
                'uptime': self._get_uptime()
            }
        }
    
    def _get_python_version(self):
        """Obter versão do Python"""
        import sys
        return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    
    def _get_platform(self):
        """Obter informações da plataforma"""
        import platform
        return {
            'system': platform.system(),
            'release': platform.release(),
            'machine': platform.machine()
        }
    
    def _get_uptime(self):
        """Obter tempo de atividade do sistema"""
        try:
            import psutil
            uptime = psutil.boot_time()
            return datetime.fromtimestamp(uptime).isoformat()
        except ImportError:
            return 'N/A'

# Instância global
version_manager = VersionManager() 