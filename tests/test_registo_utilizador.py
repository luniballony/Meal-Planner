"""
test_registo_utilizador.py

Testa o processo de registo de utilizador:
✅ Registo com dados válidos
✅ Tentativa de registo com email já existente
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

        # Criar um utilizador pré-existente para testar email duplicado
        utilizador = User(
            nome="Utilizador Existente", email="existente@email.com", nivel=1
        )
        utilizador.set_password("senha123")
        db.session.add(utilizador)
        db.session.commit()

    with app.test_client() as client:
        yield client


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
            "confirmar_password": "senha123",  # <- nome corrigido
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
            "confirmar_password": "senha123",  # <- nome corrigido
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "Já existe uma conta com esse email" in response.get_data(as_text=True)
