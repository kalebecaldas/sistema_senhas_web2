"""
Configurações centralizadas do Sistema de Senhas
"""
import os
from datetime import timedelta

class Config:
    """Configurações base"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sua_chave_secreta_aqui'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///sistema.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurações de sessão
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
    SESSION_TIMEOUT = timedelta(hours=8)
    
    # Configurações de impressora
    IMPRESSORAS = {
        'principal': {
            'ip': '192.168.0.245',
            'porta': 9100,
            'timeout': 5
        },
        'secundaria': {
            'ip': '192.168.0.48',
            'porta': 9100,
            'timeout': 5
        }
    }
    
    # Configurações TTS
    TTS_AZURE_KEY = "1GrRULjTQvppqKpUK2GSKc6YRwmdNdlDW4YywGXMfL6LkpfPU004JQQJ99BDACZoyfiXJ3w3AAAYACOGsj0S"
    TTS_AZURE_ENDPOINT = "https://brazilsouth.tts.speech.microsoft.com"
    TTS_DEFAULT_VOICE = "pt-BR-FranciscaNeural"
    TTS_TIMEOUT = 10
    
    # Configurações de prioridade padrão
    PRIORIDADE_PADRAO = 'intercalamento'
    INTERCALAMENTO_PADRAO = 2
    PESO_NORMAL_PADRAO = 1
    PESO_PREFERENCIAL_PADRAO = 3
    TOLERANCIA_PADRAO = 5
    
    # Configurações de display
    DISPLAY_CORES_PADRAO = {
        'cor_fundo': '#000000',
        'cor_texto': '#FFFFFF',
        'cor_rodape': '#000000',
        'contorno_senha': '#000000',
        'linha_senha': 'red',
        'fundo_senha': 'rgba(255, 255, 255, 0.03)',
        'destaque_senha': 'red',
        'cor_bemvindo': 'white',
        'cor_hora': 'white'
    }
    
    DISPLAY_TEXTO_PADRAO = {
        'frase_bemvindo': 'BEM-VINDO AO IAAM',
        'logo_path': 'img/logo.png',
        'video_path': 'videos/fundo.mp4'
    }
    
    # Configurações de segurança
    MAX_LOGIN_ATTEMPTS = 5
    LOCKOUT_DURATION = timedelta(minutes=15)
    
    # Configurações de upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = 'app/static'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov'}
    
    # Configurações de cache
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Configurações de logging
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'sistema.log'
    
    @staticmethod
    def init_app(app):
        """Inicializa configurações específicas da aplicação"""
        pass

class DevelopmentConfig(Config):
    """Configurações para desenvolvimento"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Configurações para produção"""
    DEBUG = False
    LOG_LEVEL = 'WARNING'
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Configurações de produção
        import logging
        from logging.handlers import RotatingFileHandler
        
        if not app.debug and not app.testing:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler(
                'logs/sistema.log', 
                maxBytes=10240000, 
                backupCount=10
            )
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            ))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
            app.logger.setLevel(logging.INFO)
            app.logger.info('Sistema de Senhas iniciado')

class TestingConfig(Config):
    """Configurações para testes"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

# Dicionário de configurações
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 