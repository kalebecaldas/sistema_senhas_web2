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
    id             = db.Column(db.Integer, primary_key=True)
    numero         = db.Column(db.Integer, nullable=False)
    sigla          = db.Column(db.String(5), nullable=False)
    tipo_paciente  = db.Column(db.String(20), nullable=False)  # 'preferencial' ou 'normal'
    primeira_vez   = db.Column(db.Boolean, nullable=False)
    gerado_em      = db.Column(db.DateTime, default=datetime.utcnow)
    chamado        = db.Column(db.Boolean, default=False)
    chamado_por    = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    chamado_em     = db.Column(db.DateTime)
    guiche = db.Column(db.String(10))  # novo campo para armazenar o guichê


    usuario_chamador = db.relationship('Usuario', foreign_keys=[chamado_por])

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


