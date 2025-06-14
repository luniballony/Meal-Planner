"""
test_apagar_plano.py

Testa se um utilizador autenticado consegue apagar um plano existente.
"""

from datetime import date
from app.models.user import User
from app.models.meal_plan import MealPlan
from app import db


import pytest


@pytest.fixture(autouse=True)
def setup_dados(client):
    """
    Adiciona utilizador e plano de teste à base de dados antes de cada teste.
    """
    with client.application.app_context():
        utilizador = User(nome="Utilizador Apagar", email="apagar@email.com", nivel=1)
        utilizador.set_password("senha123")
        db.session.add(utilizador)
        db.session.commit()

        plano = MealPlan(utilizador_id=utilizador.id, data_inicio=date.today())
        db.session.add(plano)
        db.session.commit()

        # Login antes dos testes (simula sessão)
        client.post(
            "/auth/login",
            data={"email": "apagar@email.com", "password": "senha123"},
            follow_redirects=True,
        )


def test_apagar_plano_valido(client):
    """
    Testa se um plano pode ser apagado com sucesso.
    """
    response = client.post("/planos/apagar/1", follow_redirects=True)
    assert response.status_code == 200
    assert "Plano eliminado com sucesso" in response.get_data(as_text=True)
