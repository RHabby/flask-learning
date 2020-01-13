import logging
import os
from logging.handlers import RotatingFileHandler, SMTPHandler

from flask import Flask, render_template
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from app.config import Config

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
moment = Moment()
login_manager = LoginManager()
login_manager.login_view = "user.login"

from app.collection.models import Collections
from app.user.models import User


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app=app, db=db)
    mail.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)

    from app.admin.views import blueprint as admin_blueprint
    app.register_blueprint(blueprint=admin_blueprint)

    from app.collection.views import blueprint as collection_blueprint
    app.register_blueprint(blueprint=collection_blueprint)

    from app.errors.views import blueprint as errors_blueprint
    app.register_blueprint(blueprint=errors_blueprint)

    from app.user.views import blueprint as user_blueprint
    app.register_blueprint(blueprint=user_blueprint)

    if not app.debug and not app.testing:
        if app.config["MAIL_SERVER"]:
            auth = None
            if app.config["MAIL_USERNAME"] or app.config["MAIL_PASSWORD"]:
                auth = (app.config["MAIL_USERNAME"],
                        app.config["MAIL_PASSWORD"])
            secure = None
            if app.config["MAIL_USE_TLS"]:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config["MAIL_SERVER"], app.config["MAIL_PORT"]),
                fromaddr="no-reply@" + app.config["MAIL_SERVER"],
                toaddrs=app.config["ADMINS"],
                subject="App Failure. Check the errors.",
                credentials=auth,
                secure=secure
            )
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

            if not os.path.exists("logs"):
                os.mkdir("logs")
                file_handler = RotatingFileHandler(
                    "logs/app.log", maxBytes=10240, backupCount=10)
                file_handler.setFormatter(logging.Formatter(
                    "%(asctime)s %(levelname)s: %(message)s [in %pathname]s:%(lineno)d"))
                file_handler.setLevel(logging.INFO)
                app.logger.addHandler(file_handler)

                app.logger.setLevel(logging.INFO)
                app.logger.info("App starts")

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)

    return app


