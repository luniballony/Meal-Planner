"""
test_rotas_admin.py

Testa se um utilizador comum (nível 1) é impedido de aceder às rotas de administração.
"""

import pytest
from app.models.user import User
from app import db


@pytest.fixture(autouse=True)
def setup_utilizador_normal(client):
    """
    Cria utilizador comum e faz login antes dos testes.
    """
    with client.application.app_context():

        utilizador = User(nome="Utilizador Normal", email="normal@email.com", nivel=1)
        utilizador.set_password("senha123")
        db.session.add(utilizador)
        db.session.commit()

        # Login antes dos testes
        client.post(
            "/auth/login",
            data={"email": "normal@email.com", "password": "senha123"},
            follow_redirects=True,
        )


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
