import re

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError


class UrlForm(FlaskForm):
    url = StringField(
        "Ссылка",
        validators=[DataRequired()],
        render_kw={"class": "form-control mb-2 mr-sm-2", "placeholder": "Вставьте ссылку здесь!", "id": "inlineFormInputName2"}
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
