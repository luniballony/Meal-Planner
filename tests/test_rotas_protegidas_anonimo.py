"""
test_rotas_protegidas_anonimo.py

Testa se utilizadores não autenticados são redirecionados ao tentar aceder a rotas protegidas.
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


@pytest.mark.parametrize(
    "rota",
    [
        "/home",
        "/receitas/",
        "/receitas/submeter",
        "/favorites/ver",
        "/blocked/bloqueadas",
        "/categorias/",
        "/planos/criar",
        "/planos/meus",
    ],
)
def test_rotas_anonimo_redireciona_para_login(client, rota):
    """
    Garante que utilizadores não autenticados são redirecionados para /auth/login
    """
    response = client.get(rota, follow_redirects=True)
    assert (
        "iniciar sessão" in response.get_data(as_text=True).lower()
        or "login" in response.get_data(as_text=True).lower()
    )
