from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    IntegerField,
    SelectField,
    SubmitField,
    BooleanField,
)
from wtforms.validators import DataRequired, Length, NumberRange


class RecipeForm(FlaskForm):
    titulo = StringField("Título", validators=[DataRequired(), Length(max=150)])
    descricao = TextAreaField("Descrição", validators=[DataRequired()])
    ingredientes = TextAreaField("Ingredientes", validators=[DataRequired()])
    instrucoes = TextAreaField("Instruções", validators=[DataRequired()])
    tempo_preparacao = IntegerField(
        "Tempo de preparação (min)", validators=[DataRequired(), NumberRange(min=1)]
    )
    dificuldade = SelectField(
        "Dificuldade",
        choices=[(1, "Fácil"), (2, "Médio"), (3, "Difícil")],
        coerce=int,
        validators=[DataRequired()],
    )
    tags = StringField("Tags", validators=[Length(max=150)])

    categoria_id = SelectField("Categoria", coerce=int, validators=[DataRequired()])
    publica = BooleanField("Quero partilhar esta receita com todos os utilizadores")

    submit = SubmitField("Submeter Receita")
