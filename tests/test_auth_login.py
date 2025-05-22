"""
test_auth_login.py

Testes à funcionalidade de login:
✅ Verifica se um utilizador com credenciais válidas consegue autenticar-se.
"""

import sys
import os
import pytest
from werkzeug.security import generate_password_hash

# Adiciona o caminho da app ao sys.path
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

        if not User.query.filter_by(email="teste@email.com").first():
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


def test_login_credenciais_validas(client):
    """
    Testa o login com credenciais corretas.
    """
    response = client.post(
        "/auth/login",
        data={"email": "teste@email.com", "password": "senha123"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Dashboard" in response.data or b"Bem-vindo" in response.data
