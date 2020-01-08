from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash
from wtforms import (BooleanField, PasswordField, StringField, SubmitField,
                     TextAreaField)
from wtforms.validators import (DataRequired, Email, EqualTo, Length,
                                ValidationError)

from app.user.models import User


class LoginForm(FlaskForm):
    username = StringField(
        "Логин", validators=[DataRequired()],
        render_kw={"class": "form-control"}
    )
    password = PasswordField(
        "Пароль",
        validators=[DataRequired(), Length(
            min=4, message="Пароль должен быть не короче четырех знаков")],
        render_kw={"class": "form-control"}
    )
    remember_me = BooleanField(
        "Запомнить меня",
        default=True,
        render_kw={"class": "form-check-input"}
    )
    submit = SubmitField(
        "Войти",
        render_kw={"class": "btn btn-primary btn-block"}
    )


class RegistrationForm(FlaskForm):
    username = StringField(
        "Логин",
        validators=[DataRequired()],
        render_kw={"class": "form-control"}
    )
    first_name = StringField(
        "Ваше имя",
        validators=[DataRequired()],
        render_kw={"class": "form-control"}
    )
    last_name = StringField(
        "Ваша фамилия",
        validators=[DataRequired()],
        render_kw={"class": "form-control"}
    )
    email = StringField(
        "Почта",
        validators=[DataRequired(), Email()],
        render_kw={"class": "form-control"}
    )
    password = PasswordField(
        "Придумайте пароль",
        validators=[DataRequired(), Length(
            min=4, message="Пароль должен быть не короче четырех знаков")],
        render_kw={"class": "form-control"}
    )
    submit_password = PasswordField(
        "Повторите пароль",
        validators=[DataRequired(), EqualTo("password")],
        render_kw={"class": "form-control"}
    )
    submit = SubmitField(
        "Зарегистрироваться",
        render_kw={"class": "btn btn-primary btn-block"}
    )

    def validate_username(self, username):
        user_count = User.query.filter_by(username=username.data).count()
        if user_count > 0:
            raise ValidationError(
                "Пользователь с таким логином уже существует")

    def validate_email(self, email):
        email_count = User.query.filter_by(email=email.data).count()
        if email_count > 0:
            raise ValidationError(
                "Пользователь с таким почтовым адресом уже существует")


class EditProfileForm(FlaskForm):
    username = StringField(
        "Логин",
        validators=[DataRequired()],
        render_kw={"class": "form-control"}
    )
    about_me = TextAreaField(
        "О себе",
        validators=[Length(min=0, max=160)],
        render_kw={"class": "form-control",
                   "placeholder": "Добавить сведения о себе"}
    )
    location = StringField(
        "Местоположение",
        render_kw={"class": "form-control",
                   "placeholder": "Добавить местоположение"}
    )
    web_site = StringField(
        "Веб-сайт",
        render_kw={"class": "form-control", "placeholder": "Добавить веб-сайт"}
    )
    old_password = PasswordField(
        "Старый пароль",
        render_kw={"class": "form-control"}
    )
    new_password = PasswordField(
        "Новый пароль",
        validators=[
            Length(min=4, message="Пароль должен быть не короче четырех знаков")],
        render_kw={"class": "form-control"}
    )
    submit_new_password = PasswordField(
        "Повторите новый пароль",
        validators=[EqualTo("new_password")],
        render_kw={"class": "form-control"}
    )
    submit = SubmitField(
        "Сохранить",
        render_kw={"class": "btn btn-primary"}
    )

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(
                    "Пользователь с таким ником уже зарегистрирован.")

    def validate_old_password(self, old_password):
        user = User.query.filter_by(username=self.original_username).first()
        if not check_password_hash(user.password, self.old_password.data):
            raise ValidationError("Вы ввели неправильный старый пароль.")

    def validate_new_password(self, new_password):
        user = User.query.filter_by(username=self.original_username).first()
        if check_password_hash(user.password, self.new_password.data):
            raise ValidationError("Старый и новый пароли не должны совпадать.")


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()],
        render_kw={"class": "form-control",
                   "placeholder": "Введите Email"}
    )
    submit = SubmitField(
        "Отправить",
        render_kw={"class": "btn btn-primary btn-block"}
    )


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        "Придумайте пароль",
        validators=[DataRequired()],
        render_kw={"class": "form-control"}
    )
    submit_password = PasswordField(
        "Повторите пароль",
        validators=[DataRequired(), EqualTo("password")],
        render_kw={"class": "form-control"}
    )
    submit = SubmitField(
        "Отправить",
        render_kw={"class": "btn btn-primary btn-block"}
    )
