"""
test_protected_routes.py

Testa se rotas protegidas exigem autenticação.
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


def test_acesso_a_criar_plano_sem_login(client):
    """
    Tenta aceder à rota /planos/criar sem estar autenticado.
    Espera-se redireção para o login.
    """
    response = client.get("/planos/criar", follow_redirects=True)

    assert response.status_code == 200
    assert "Iniciar sessão" in response.get_data(
        as_text=True
    ) or "Login" in response.get_data(as_text=True)
