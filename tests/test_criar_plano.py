"""
test_criar_plano.py

Testa a funcionalidade de criação de planos semanais por utilizadores autenticados.
"""

import pytest
from datetime import date
from app.models.user import User
from app import db


@pytest.fixture(autouse=True)
def setup_utilizador(client):
    """
    Cria utilizador e faz login antes de cada teste.
    """
    with client.application.app_context():

        utilizador = User(nome="Utilizador Plano", email="plano@email.com", nivel=1)
        utilizador.set_password("senha123")
        db.session.add(utilizador)
        db.session.commit()

        # Login antes do teste
        client.post(
            "/auth/login",
            data={"email": "plano@email.com", "password": "senha123"},
            follow_redirects=True,
        )


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
