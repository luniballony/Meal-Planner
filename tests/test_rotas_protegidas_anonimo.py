"""
test_rotas_protegidas_anonimo.py

Testa se utilizadores não autenticados são redirecionados ao tentar aceder a rotas protegidas.
"""

import pytest
from app import db


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
