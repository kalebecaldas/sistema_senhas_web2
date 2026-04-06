# app/models.py
from enum import Enum
from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager

# Enum para tipos de usuário
class Papel(str, Enum):
    ADMIN = "admin"
    USUARIO = "usuario"

# Modelo de usuário
class Usuario(UserMixin, db.Model):
    id     = db.Column(db.Integer, primary_key=True)
    nome   = db.Column(db.String(150), nullable=False)
    email  = db.Column(db.String(150), unique=True, nullable=False)
    senha  = db.Column(db.String(150), nullable=False)
    tipo   = db.Column(db.Enum(Papel), default=Papel.USUARIO, nullable=False)

    @property
    def is_admin(self):
        return self.tipo == Papel.ADMIN

# Callback para carregar o usuário no login
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Modelo de senha para a fila
class Senha(db.Model):
    __tablename__ = 'senha'
    
    id             = db.Column(db.Integer, primary_key=True)
    numero         = db.Column(db.Integer, nullable=False)
    sigla          = db.Column(db.String(5), nullable=False)
    tipo_paciente  = db.Column(db.String(20), nullable=False)  # 'preferencial' ou 'normal'
    primeira_vez   = db.Column(db.Boolean, nullable=False)
    gerado_em      = db.Column(db.DateTime, default=datetime.utcnow, index=True)  # Índice para ordenação
    chamado        = db.Column(db.Boolean, default=False, index=True)  # Índice para filtros
    chamado_por    = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    chamado_em     = db.Column(db.DateTime, index=True)  # Índice para ordenação por chamada
    guiche         = db.Column(db.String(10))  # novo campo para armazenar o guichê

    usuario_chamador = db.relationship('Usuario', foreign_keys=[chamado_por])
    
    # Índice composto para queries mais rápidas
    __table_args__ = (
        db.Index('idx_chamado_chamado_em', 'chamado', 'chamado_em'),
        db.Index('idx_tipo_chamado', 'tipo_paciente', 'chamado'),
    )

# Modelo de vídeo na playlist
class VideoPlaylist(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    filename    = db.Column(db.String(255), nullable=False)
    path        = db.Column(db.String(255), nullable=False)
    duration    = db.Column(db.Integer)  # duração em segundos
    ordem       = db.Column(db.Integer, default=0)  # ordem na playlist
    ativo       = db.Column(db.Boolean, default=True)
    criado_em   = db.Column(db.DateTime, default=datetime.utcnow)

# Modelo de configurações do sistema (para display e logo)
class ConfiguracaoSistema(db.Model):
    id                = db.Column(db.Integer, primary_key=True)
    cor_fundo         = db.Column(db.String(7), default="#000000")
    cor_texto         = db.Column(db.String(7), default="#FFFFFF")
    cor_rodape        = db.Column(db.String(7), default="#000000")
    logo_path         = db.Column(db.String(255), default="img/logo.png")
    video_path        = db.Column(db.String(255), default="videos/fundo.mp4")
    contorno_senha    = db.Column(db.String(20), default="#000000")
    linha_senha       = db.Column(db.String(20), default="red")
    fundo_senha       = db.Column(db.String(50), default="rgba(255, 255, 255, 0.03)")
    destaque_senha    = db.Column(db.String(20), default="red")
    cor_bemvindo      = db.Column(db.String(20), default="white")
    frase_bemvindo    = db.Column(db.String(100), default="BEM-VINDO AO IAAM")
    cor_hora          = db.Column(db.String(20), default="white")
    voz_azure         = db.Column(db.String(100), default="pt-BR-FranciscaNeural")
    
    # Configurações de prioridade
    tipo_prioridade     = db.Column(db.String(20), default='intercalamento')  # intercalamento, peso ou alternancia
    intercalamento_valor = db.Column(db.Integer, default=2)
    peso_normal         = db.Column(db.Integer, default=1)
    peso_preferencial   = db.Column(db.Integer, default=3)
    tolerancia_minutos  = db.Column(db.Integer, default=5)
    
    # Configurações de Playlist de Vídeos
    playlist_enabled      = db.Column(db.Boolean, default=False)  # Ativar playlist
    transition_type       = db.Column(db.String(20), default='fade')  # fade, slide, dissolve
    transition_duration   = db.Column(db.Float, default=1.0)  # duração da transição em segundos
    play_order            = db.Column(db.String(20), default='sequential')  # sequential, random
    
    # Configurações de TV
    tv_enabled            = db.Column(db.Boolean, default=False)  # Ativar TV
    tv_channel_id         = db.Column(db.String(100))  # ID do canal Pluto TV
    videos_before_tv      = db.Column(db.Integer, default=3)  # Quantos vídeos antes de mostrar TV
    tv_duration_minutes   = db.Column(db.Integer, default=10)  # Tempo de TV em minutos
    
    # Configurações de Impressoras Térmicas
    impressora_principal_ip   = db.Column(db.String(15), default='192.168.0.245')  # IP da impressora principal
    impressora_principal_porta = db.Column(db.Integer, default=9100)  # Porta da impressora principal
    impressora_secundaria_ip  = db.Column(db.String(15), default='192.168.0.48')  # IP da impressora secundária
    impressora_secundaria_porta = db.Column(db.Integer, default=9100)  # Porta da impressora secundária

    # Som de chamada do display
    som_chamada = db.Column(db.String(30), default='sino_suave')


