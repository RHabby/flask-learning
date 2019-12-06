from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from app.user.models import User


class LoginForm(FlaskForm):
    username = StringField(
        "Логин", validators=[DataRequired()],
        render_kw={"class": "form-control"}
    )
    password = PasswordField(
        "Пароль",
        validators=[DataRequired()],
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
        validators=[DataRequired()],
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
