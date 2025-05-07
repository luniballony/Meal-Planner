from flask_wtf import FlaskForm
from wtforms import SubmitField


class RemoverFavoritoForm(FlaskForm):
    submit = SubmitField("Remover")
