"""
test_auth_login_invalid.py

Testa se o sistema reage corretamente ao login com credenciais erradas.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app, db
from app.models.user import User


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["WTF_CSRF_ENABLED"] = False

    with app.app_context():
        db.drop_all()
        db.create_all()
        utilizador = User(nome="Utilizador Teste", email="teste@email.com", nivel=1)
        utilizador.set_password("senha123")
        db.session.add(utilizador)
        db.session.commit()

    with app.test_client() as client:
        yield client


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
