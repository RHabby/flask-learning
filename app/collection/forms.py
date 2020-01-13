import re

from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError

from app.collection.models import Collections


class UrlForm(FlaskForm):
    url = StringField(
        "Ссылка",
        validators=[DataRequired()],
        render_kw={"class": "form-control mb-2 mr-sm-2",
                   "placeholder": "Вставьте ссылку здесь!", "id": "inlineFormInputName2"}
    )
    submit = SubmitField(
        "Сохранить",
        render_kw={"class": "btn btn-primary mb-2"}
    )

    def validate_url(self, url):
        pattern = re.compile(
            r"^(https?:\/\/){0,1}([a-zA-Zа-яА-Я0-9.-]+\.)+([a-zа-я]{2,6})(\/[a-zа-яA-ZА-Я0-9.&?=#-_]*)*(\/|)$")
        result = pattern.match(url.data)
        if not result:
            raise ValidationError("Не похоже, что вы хотите сохранить ссылку")


class CommentForm(FlaskForm):
    collections_id = HiddenField("ID закладки", validators=[DataRequired()])
    comment_text = TextAreaField(
        "Написать комментарий", 
        validators=[DataRequired(), Length(min=2, max=360)], 
        render_kw={"class": "form-control", "placeholder": "Добавить комментарий"}
    )
    submit = SubmitField("Готово", render_kw={"class": "btn btn-primary"})

    def validate_news_id(self, collections_id):
        if not Collections.query.get(collections_id.data):
            raise ValidationError("Новости с таким ID не существует.")


class EditBookmarkForm(FlaskForm):
    title = StringField(
        "Название",
        validators=[DataRequired()],
        render_kw={"class": "form-control", 
                   "placeholder": "Добавить название"}
    )
    description = TextAreaField(
        "Описание",
        validators=[Length(min=0, max=200)],
        render_kw={"class": "form-control",
                   "placeholder": "Добавить описание"}
    )
    submit = SubmitField(
        "Сохранить",
        render_kw={"class": "btn btn-primary"}
    )
