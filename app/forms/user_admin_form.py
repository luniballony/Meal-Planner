from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, HiddenField
from wtforms.validators import DataRequired, Email, Length


class EditarUserForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    nivel = SelectField(
        "Nível de Acesso",
        choices=[("1", "Comum"), ("2", "Premium"), ("3", "Administrador")],
        validators=[DataRequired()],
    )
    submit = SubmitField("Atualizar Utilizador")


class ConfirmarAcaoForm(FlaskForm):
    utilizador_id = HiddenField("ID do Utilizador")
    submit = SubmitField("Confirmar")
