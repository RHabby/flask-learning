from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user

from app.db import db
from app.user.models import User
from app.user.forms import LoginForm, RegistrationForm

blueprint = Blueprint("user", __name__)


@blueprint.route("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("collection.index"))
    else:
        title = "Авторизация"
        login_form = LoginForm()
        return render_template("user/login.html", title=title, login_form=login_form)


@blueprint.route("/process-login", methods=["POST"])
def process_login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()

        if user and user.check_password(login_form.password.data):
            login_user(user, remember=login_form.remember_me.data)
            flash("Вы успешно авторизовались.")
            return redirect(url_for("collection.index"))

    flash("Логин или пароль неверны. Попробуйте снова")
    return redirect(url_for("user.login"))


@blueprint.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("user.login"))


@blueprint.route("/registration")
def registration():
    if current_user.is_authenticated:
        return redirect(url_for("collection.index"))
    else:
        title = "Регистрация"
        registration_form = RegistrationForm()
        return render_template("user/registration.html", title=title, registration_form=registration_form)


@blueprint.route("/process-registration", methods=["POST"])
def process_registration():
    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        new_user = User(username=registration_form.username.data,
                        first_name=registration_form.first_name.data,
                        last_name=registration_form.last_name.data,
                        email=registration_form.email.data,
                        role="user")
        new_user.set_password(registration_form.password.data)

        db.session.add(new_user)
        db.session.commit()
        flash("Вы успешно зарегистрировались.")
        return redirect(url_for("user.login"))

    else:
        for field, errors in registration_form.errors.items():
            for error in errors:
                flash(
                    f"Ошибка в поле <{getattr(registration_form, field).label.text}>: {error}")
        return redirect(url_for("user.registration"))


@blueprint.route("/")
def start_page():
    if current_user.is_authenticated:
        return redirect(url_for("collection.index"))
    else:
        login_title = "Авторизация"
        registration_title = "Регистрация"

        login_form = LoginForm()
        registration_form = RegistrationForm()
        return render_template(
            "user/start_page.html",
            login_title=login_title,
            registration_title=registration_title,
            login_form=login_form,
            registration_form=registration_form
        )
