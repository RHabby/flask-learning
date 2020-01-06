from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse

from app.db import db
from app.user.email import send_password_reset_email
from app.user.forms import (EditProfileForm, LoginForm, RegistrationForm,
                            ResetPasswordForm, ResetPasswordRequestForm)
from app.user.models import User
from app.utils import get_url_target

blueprint = Blueprint("user", __name__)


@blueprint.route("/login")
def login():
    if current_user.is_authenticated:
        # flash("Вы уже авторизованы!")
        return redirect(url_for("collection.index", username=current_user.username))
    else:
        title = "Авторизация"
        login_form = LoginForm()
        return render_template("user/login.html", title=title, login_form=login_form)


@blueprint.route("/process-login", methods=["POST"])
def process_login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(
            username=login_form.username.data).first_or_404()

        if user and user.check_password(login_form.password.data):
            login_user(user, remember=login_form.remember_me.data)
            flash("Вы успешно авторизовались.")

            return redirect(get_url_target())

    flash("Логин или пароль неверны. Попробуйте снова")
    return redirect(url_for("user.login"))


@blueprint.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("user.login"))


@blueprint.route("/registration")
def registration():
    if current_user.is_authenticated:
        flash("Вы авторизованы. Чтобы зарегистрировать еще один аккаунт выйдите из своего профиля.")
        return redirect(url_for("collection.index", username=current_user.username))
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
        return redirect(url_for("collection.index", username=current_user.username))
    else:
        title = "Вход"
        login_title = "Авторизация"
        registration_title = "Регистрация"

        login_form = LoginForm()
        registration_form = RegistrationForm()

        return render_template(
            "user/start_page.html",
            title=title,
            login_title=login_title,
            registration_title=registration_title,
            login_form=login_form,
            registration_form=registration_form
        )


@blueprint.route("/profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    title = "Изменить профиль"
    edit_form = EditProfileForm(current_user.username)
    if edit_form.validate_on_submit():
        current_user.username = edit_form.username.data
        current_user.about_me = edit_form.about_me.data
        current_user.location = edit_form.location.data
        current_user.web_site = edit_form.web_site.data
        db.session.commit()
        flash("Сделано!")

    elif request.method == "GET":
        edit_form.username.data = current_user.username
        edit_form.about_me.data = current_user.about_me
        edit_form.location.data = current_user.location
        edit_form.web_site.data = current_user.web_site

    else:
        for field, errors in edit_form.errors.items():
            for error in errors:
                flash(
                    f"Ошибка в поле <{getattr(edit_form, field).label.text}>: {error}")
        return redirect(url_for("user.edit_profile"))

    return render_template("user/edit_profile.html", user=current_user, edit_form=edit_form, title=title)


@blueprint.route("/follow/<string:username>")
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(f"User {username} not found.")
        return redirect(url_for("collection.index", username=current_user.username))
    if user == current_user:
        flash("You can`t follow yourself.")
        return redirect(url_for("collection.index", username=current_user.username))
    current_user.follow(user)
    db.session.commit()
    return redirect(url_for("collection.index", username=username))


@blueprint.route("/unfollow/<string:username>")
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(f"User {username} not found.")
        return redirect(url_for("collection.index", username=current_user.username))
    if user == current_user:
        flash("You can`t unfollow yourself.")
        return redirect(url_for("collection.index", username=current_user.username))
    current_user.unfollow(user)
    db.session.commit()
    return redirect(url_for("collection.index", username=username))


@blueprint.route("/user/<string:username>/followers")
def get_followers(username):
    user = User.query.filter_by(username=username).first()
    followers = user.followers.all()
    title = f"Люди, которые читают {user.first_name} {user.last_name} | Полка"
    return render_template("user/followers.html", user=user, followers=followers, title=title)


@blueprint.route("/user/<string:username>/following")
def get_following(username):
    user = User.query.filter_by(username=username).first()
    followed_users = user.followed.all()
    title = f"Люди, которыx читаeт {user.first_name} {user.last_name} | Полка"
    return render_template("user/followed.html", user=user, following=followed_users, title=title)


@blueprint.route("/forgot", methods=["GET", "POST"])
def reset_password_request():
    title = "Сбросить пароль"
    if current_user.is_authenticated:
        return redirect(url_for("collection.index", username=current_user.username))
    reset_form = ResetPasswordRequestForm()
    if reset_form.validate_on_submit():
        user = User.query.filter_by(email=reset_form.email.data).first()
        # print(user)
        if user:
            send_password_reset_email(user)
        flash("Ссылка для восстановления пароля была отправлена вам на email")
        return redirect(url_for("user.login"))
    return render_template("user/reset_password_request.html", title=title, reset_form=reset_form)


@blueprint.route("/reset-password/<string:token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("collection.index", username=current_user.username))
    user = User.verify_reset_password_token(token)

    if not user:
        return redirect(url_for("user.registration"))
    reset_form = ResetPasswordForm()
    if reset_form.validate_on_submit():
        user.set_password(reset_form.password.data)
        db.session.commit()
        flash("Ваш пароль был восстановлен")
        return redirect(url_for("user.login"))
    return render_template("user/reset_password.html", reset_form=reset_form)
