"""
test_submeter_receita_sem_login.py

Garante que a rota de submissão de receitas está protegida contra utilizadores não autenticados.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app, db


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["WTF_CSRF_ENABLED"] = False

    with app.app_context():
        db.drop_all()
        db.create_all()

    with app.test_client() as client:
        yield client


def test_submeter_receita_sem_login(client):
    """
    Testa se o utilizador não autenticado é redirecionado ao tentar submeter uma receita.
    """
    response = client.get("/receitas/submeter", follow_redirects=True)

    assert response.status_code == 200
    assert (
        "iniciar sessão" in response.get_data(as_text=True).lower()
        or "login" in response.get_data(as_text=True).lower()
    )
