from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class RegisterForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6, message="A password deve ter pelo menos 6 caracteres."),
        ],
    )
    confirmar_password = PasswordField(
        "Confirmar Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="As passwords não coincidem."),
        ],
    )
    submit = SubmitField("Criar Conta")
