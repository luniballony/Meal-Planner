"""
test_registo_utilizador.py

Testa o processo de registo de utilizador:
✅ Registo com dados válidos
✅ Tentativa de registo com email já existente
"""

import pytest
from app.models.user import User
from app import db


@pytest.fixture(autouse=True)
def setup_utilizador_existente(client):
    """
    Cria um utilizador pré-existente para testar o email duplicado.
    """
    with client.application.app_context():

        utilizador = User(
            nome="Utilizador Existente", email="existente@email.com", nivel=1
        )
        utilizador.set_password("senha123")
        db.session.add(utilizador)
        db.session.commit()


def test_registo_valido(client):
    """
    Testa o registo com dados válidos.
    """
    response = client.post(
        "/auth/register",
        data={
            "nome": "Novo Utilizador",
            "email": "novo@email.com",
            "password": "senha123",
            "confirmar_password": "senha123",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "Conta criada com sucesso" in response.get_data(as_text=True)


def test_registo_email_duplicado(client):
    """
    Testa o registo com email já existente.
    """
    response = client.post(
        "/auth/register",
        data={
            "nome": "Outro Utilizador",
            "email": "existente@email.com",
            "password": "senha123",
            "confirmar_password": "senha123",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "Já existe uma conta com esse email" in response.get_data(as_text=True)
