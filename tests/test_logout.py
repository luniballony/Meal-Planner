"""
test_logout.py

Testa se o logout limpa a sessão e redireciona corretamente.
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

        utilizador = User(
            nome="Utilizador Teste",
            email="teste@email.com",
            nivel=1,
        )
        utilizador.set_password("senha123")
        db.session.add(utilizador)
        db.session.commit()

    with app.test_client() as client:
        yield client


def test_logout(client):
    """
    Testa se o logout limpa a sessão e redireciona corretamente.
    """
    # Fazer login
    client.post(
        "/auth/login",
        data={"email": "teste@email.com", "password": "senha123"},
        follow_redirects=True,
    )

    # Fazer logout
    response = client.get("/auth/logout", follow_redirects=True)

    assert response.status_code == 200
    assert "Sessão terminada" in response.get_data(as_text=True)
