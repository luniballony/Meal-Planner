"""
test_protected_routes.py

Testa se rotas protegidas exigem autenticação.
"""

from app import db
import pytest


def test_acesso_a_criar_plano_sem_login(client):
    """
    Tenta aceder à rota /planos/criar sem estar autenticado.
    Espera-se redireção para o login.
    """
    response = client.get("/planos/criar", follow_redirects=True)

    assert response.status_code == 200
    assert (
        "iniciar sessão" in response.get_data(as_text=True).lower()
        or "login" in response.get_data(as_text=True).lower()
    )
