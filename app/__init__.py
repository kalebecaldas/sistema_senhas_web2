from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

app = None

def create_app():
    global app
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sistema.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
