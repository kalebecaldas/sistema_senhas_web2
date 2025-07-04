"""
Módulo de versionamento do Sistema de Senhas IAAM
"""

import os
import subprocess
import requests
import hashlib
import hmac
from datetime import datetime

class VersionManager:
    def __init__(self):
        self.version_file = 'VERSION'
        self.repo_url = 'https://github.com/kalebecaldas/sistema_senhas_web2.git'
        self.current_version = self.get_current_version()
        
        # Configurações de segurança
        self.allowed_branches = ['main', 'master']
        self.max_commits_ahead = 50  # Limite de commits para atualização
        self.environment = os.getenv('ENVIRONMENT', 'development')
        
    def get_current_version(self):
        """Obter versão atual do sistema"""
        try:
            with open(self.version_file, 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            return '1.0.0'
    
    def _is_official_repo(self):
        """Verificar se é o repositório oficial"""
        try:
            remote_url = subprocess.check_output(
                ['git', 'config', '--get', 'remote.origin.url'],
                stderr=subprocess.DEVNULL
            ).decode('utf-8').strip()
            
            return 'kalebecaldas/sistema_senhas_web2' in remote_url
        except:
            return False
    
    def _is_safe_to_update(self):
        """Verificar se é seguro fazer atualização"""
        # Verificar se é repositório oficial
        if not self._is_official_repo():
            return False, "Repositório não autorizado"
        
        # Verificar se não está em produção (opcional)
        if self.environment == 'production':
            return False, "Atualizações automáticas desabilitadas em produção"
        
        # Verificar permissões de escrita
        if not os.access('.', os.W_OK):
            return False, "Sem permissões de escrita no diretório"
        
        return True, "OK"
    
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
            # Verificar se é seguro
            is_safe, message = self._is_safe_to_update()
            if not is_safe:
                return {
                    'has_updates': False,
                    'commits_ahead': 0,
                    'commits_behind': 0,
                    'last_check': datetime.now().isoformat(),
                    'error': message
                }
            
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
            
            commits_ahead = int(ahead)
            
            return {
                'has_updates': commits_ahead > 0 and commits_ahead <= self.max_commits_ahead,
                'commits_ahead': commits_ahead,
                'commits_behind': int(behind),
                'last_check': datetime.now().isoformat(),
                'update_safe': commits_ahead <= self.max_commits_ahead
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
        """Atualizar o sistema com validações de segurança"""
        try:
            # Verificar se é seguro
            is_safe, message = self._is_safe_to_update()
            if not is_safe:
                return {
                    'success': False,
                    'message': 'Atualização bloqueada por segurança',
                    'error': message
                }
            
            # Verificar atualizações disponíveis
            update_info = self.check_for_updates()
            if not update_info.get('has_updates', False):
                return {
                    'success': False,
                    'message': 'Nenhuma atualização disponível',
                    'error': 'Sistema já está atualizado'
                }
            
            if not update_info.get('update_safe', False):
                return {
                    'success': False,
                    'message': 'Muitas atualizações pendentes',
                    'error': f'Mais de {self.max_commits_ahead} commits pendentes. Atualize manualmente.'
                }
            
            # Fazer backup das configurações
            backup_path = self._backup_config()
            
            # Pull das atualizações
            result = subprocess.run(
                ['git', 'pull', 'origin', 'main'],
                capture_output=True,
                text=True,
                timeout=300  # Timeout de 5 minutos
            )
            
            if result.returncode == 0:
                # Atualizar dependências se necessário
                dep_result = self._update_dependencies()
                
                return {
                    'success': True,
                    'message': 'Sistema atualizado com sucesso!',
                    'output': result.stdout,
                    'backup_path': backup_path,
                    'dependencies_updated': dep_result
                }
            else:
                return {
                    'success': False,
                    'message': 'Erro ao atualizar sistema',
                    'error': result.stderr
                }
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'message': 'Timeout durante atualização',
                'error': 'A operação demorou mais de 5 minutos'
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
            'VERSION',
            'requirements.txt'
        ]
        
        backed_up_files = []
        for file_path in important_files:
            if os.path.exists(file_path):
                try:
                    shutil.copy2(file_path, backup_dir)
                    backed_up_files.append(file_path)
                except Exception as e:
                    print(f"Erro ao fazer backup de {file_path}: {e}")
        
        return backup_dir if backed_up_files else None
    
    def _update_dependencies(self):
        """Atualizar dependências Python com validação"""
        try:
            # Verificar se requirements.txt foi modificado
            result = subprocess.run(
                ['git', 'diff', '--name-only', 'HEAD~1', 'HEAD'],
                capture_output=True,
                text=True
            )
            
            if 'requirements.txt' in result.stdout:
                # Atualizar dependências
                dep_result = subprocess.run(
                    ['pip', 'install', '-r', 'requirements.txt', '--upgrade'],
                    capture_output=True,
                    text=True,
                    timeout=600  # 10 minutos para instalação
                )
                return dep_result.returncode == 0
            else:
                return True  # Não precisa atualizar dependências
        except Exception:
            return False
    
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
                'uptime': self._get_uptime(),
                'environment': self.environment,
                'security': {
                    'official_repo': self._is_official_repo(),
                    'write_permissions': os.access('.', os.W_OK),
                    'update_safe': update_info.get('update_safe', False)
                }
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