"""
test_rotas_admin.py

Testa se um utilizador comum (nível 1) é impedido de aceder às rotas de administração.
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

        utilizador = User(nome="Utilizador Normal", email="normal@email.com", nivel=1)
        utilizador.set_password("senha123")
        db.session.add(utilizador)
        db.session.commit()

    with app.test_client() as client:
        # Login antes dos testes
        client.post(
            "/auth/login",
            data={"email": "normal@email.com", "password": "senha123"},
            follow_redirects=True,
        )
        yield client


@pytest.mark.parametrize(
    "rota",
    [
        "/admin/utilizadores",
        "/admin/categorias",
        "/admin/aprovar_receitas",
        "/admin/receitas",
    ],
)
def test_acesso_admin_bloqueado_para_utilizador_comum(client, rota):
    """
    Garante que utilizadores comuns não conseguem aceder a rotas de administrador.
    """
    response = client.get(rota, follow_redirects=True)
    assert response.status_code == 200
    assert "acesso restrito" in response.get_data(as_text=True).lower()
