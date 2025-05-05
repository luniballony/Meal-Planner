from flask_wtf import FlaskForm
from wtforms import SubmitField

class AdicionarFavoritoForm(FlaskForm):
    submit = SubmitField('Adicionar aos favoritos')
