"""
test_logout.py

Testa se o logout limpa a sessão e redireciona corretamente.
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
