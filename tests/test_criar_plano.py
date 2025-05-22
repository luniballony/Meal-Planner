"""
test_criar_plano.py

Testa a funcionalidade de criação de planos semanais por utilizadores autenticados.
"""

import sys
import os
import pytest
from datetime import date

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

        utilizador = User(nome="Utilizador Plano", email="plano@email.com", nivel=1)
        utilizador.set_password("senha123")
        db.session.add(utilizador)
        db.session.commit()

    with app.test_client() as client:
        # Fazer login antes do teste
        client.post(
            "/auth/login",
            data={"email": "plano@email.com", "password": "senha123"},
            follow_redirects=True,
        )
        yield client


def test_criar_plano_valido(client):
    """
    Testa a criação de um plano semanal válido com data e pelo menos uma refeição.
    """
    response = client.post(
        "/planos/criar",
        data={
            "data_inicio": date.today().strftime("%Y-%m-%d"),
            "segunda_pequeno_almoço": "",  # pode estar em branco
            "segunda_almoço": "",  # pode estar em branco
            "segunda_jantar": "",  # pode estar em branco
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "Plano criado com sucesso" in response.get_data(as_text=True)
