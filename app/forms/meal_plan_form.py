from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField
from wtforms.validators import DataRequired


class MealPlanForm(FlaskForm):
    data_inicio = DateField("Data de Início", validators=[DataRequired()])
    submit = SubmitField("Criar Plano")
