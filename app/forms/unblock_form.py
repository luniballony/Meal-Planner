from flask_wtf import FlaskForm
from wtforms import SubmitField


class DesbloquearReceitaForm(FlaskForm):
    submit = SubmitField("Desbloquear")
