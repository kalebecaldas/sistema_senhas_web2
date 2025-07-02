from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

from .config import config

db = SQLAlchemy()
login_manager = LoginManager()

app = None

def create_app(config_name=None):
    global app
    
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG') or 'default'
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    # ✅ Mova os imports para cá (depois da criação do app)
    from .routes import bp as main_blueprint
    from .tts_routes import bp_tts

    app.register_blueprint(main_blueprint)
    app.register_blueprint(bp_tts)

    @app.errorhandler(403)
    def proibido(e):
        return render_template("403.html"), 403

    return app
