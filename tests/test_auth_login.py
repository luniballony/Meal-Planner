"""
test_auth_login.py

Testes à funcionalidade de login:
✅ Verifica se um utilizador com credenciais válidas consegue autenticar-se.
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
        utilizador = User(
            nome="Utilizador Teste",
            email="teste@email.com",
            nivel=1,
        )
        utilizador.set_password("senha123")
        db.session.add(utilizador)
        db.session.commit()


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
    # Ajusta o texto abaixo conforme a mensagem de boas-vindas do teu projeto
    assert b"Dashboard" in response.data or b"Bem-vindo" in response.data
