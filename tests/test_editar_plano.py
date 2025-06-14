"""
test_editar_plano.py

Testa a edição de um plano semanal existente por um utilizador autenticado.
"""

import pytest
from datetime import date
from app.models.user import User
from app.models.meal_plan import MealPlan
from app import db


@pytest.fixture(autouse=True)
def setup_dados(client):
    """
    Cria utilizador, plano e faz login antes do teste.
    """
    with client.application.app_context():

        utilizador = User(nome="Utilizador Editor", email="editor@email.com", nivel=1)
        utilizador.set_password("senha123")
        db.session.add(utilizador)
        db.session.commit()

        plano = MealPlan(utilizador_id=utilizador.id, data_inicio=date.today())
        db.session.add(plano)
        db.session.commit()

        client.post(
            "/auth/login",
            data={"email": "editor@email.com", "password": "senha123"},
            follow_redirects=True,
        )


def test_editar_plano_valido(client):
    """
    Testa se um utilizador consegue editar um plano existente.
    """
    response = client.post(
        "/planos/editar/1",
        data={
            "data_inicio": date.today().strftime("%Y-%m-%d"),
            "segunda_pequeno_almoco": "Torradas",
            "segunda_almoço": "Feijoada",
            "segunda_jantar": "Sopa",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "Plano atualizado com sucesso" in response.get_data(as_text=True)
