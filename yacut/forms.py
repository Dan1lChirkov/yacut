from flask_wtf import FlaskForm
from wtforms import StringField, URLField, SubmitField
from wtforms.validators import DataRequired, Optional, Length


class UrlMapForm(FlaskForm):
    original_link = URLField(
        'Поле для оригинальной длинной ссылки',
        validators=[DataRequired(message='Обязательное поле')]
    )
    custom_id = StringField(
        'Вариант короткой ссылки',
        validators=[
            Optional(),
            Length(1, 16)
        ]
    )
    submit = SubmitField('Добавить')