from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate

from app.db import db
from app.user.models import User
from app.user.views import blueprint as user_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")

    db.init_app(app)
    migrate = Migrate(app=app, db=db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "user.login"

    app.register_blueprint(blueprint=user_blueprint)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)

    @app.route("/")
    def hello():
        return render_template("base.html")

    return app