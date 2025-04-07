from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class CategoriaForm(FlaskForm):
    nome = StringField(
        "Nome da Categoria",
        validators=[
            DataRequired(message="O nome é obrigatório."),
            Length(min=2, max=100),
        ],
    )
    submit = SubmitField("Criar Categoria")
