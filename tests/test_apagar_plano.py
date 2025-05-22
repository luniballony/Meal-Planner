"""
test_apagar_plano.py

Testa se um utilizador autenticado consegue apagar um plano existente.
"""

import sys
import os
import pytest
from datetime import date

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app, db
from app.models.user import User
from app.models.meal_plan import MealPlan


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["WTF_CSRF_ENABLED"] = False

    with app.app_context():
        db.drop_all()
        db.create_all()

        utilizador = User(nome="Utilizador Apagar", email="apagar@email.com", nivel=1)
        utilizador.set_password("senha123")
        db.session.add(utilizador)
        db.session.commit()

        plano = MealPlan(utilizador_id=utilizador.id, data_inicio=date.today())
        db.session.add(plano)
        db.session.commit()

    with app.test_client() as client:
        # Login
        client.post(
            "/auth/login",
            data={"email": "apagar@email.com", "password": "senha123"},
            follow_redirects=True,
        )
        yield client


def test_apagar_plano_valido(client):
    """
    Testa se um plano pode ser apagado com sucesso.
    """
    response = client.post("/planos/apagar/1", follow_redirects=True)

    assert response.status_code == 200
    assert "Plano eliminado com sucesso" in response.get_data(as_text=True)
