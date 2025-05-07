from flask_wtf import FlaskForm
from wtforms import SubmitField


class BloquearReceitaForm(FlaskForm):
    submit = SubmitField("Bloquear receita")
