"""
test_auth_login_invalid.py

Testa se o sistema reage corretamente ao login com credenciais erradas.
"""

import pytest
from app.models.user import User
from app import db


@pytest.fixture(autouse=True)
def setup_utilizador(client):
    """
    Cria utilizador válido na base de dados de teste antes de cada teste.
    """
    with client.application.app_context():
        utilizador = User(nome="Utilizador Teste", email="teste@email.com", nivel=1)
        utilizador.set_password("senha123")
        db.session.add(utilizador)
        db.session.commit()


def test_login_credenciais_invalidas(client):
    """
    Testa o login com password errada.
    """
    response = client.post(
        "/auth/login",
        data={"email": "teste@email.com", "password": "senhaErrada"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert (
        b"Credenciais inv" in response.data
    )  # Assume que a flash diz "Credenciais inválidas."
