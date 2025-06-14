"""
test_criar_plano_sem_login.py

Garante que utilizadores não autenticados não conseguem aceder à rota de criação de plano semanal.
"""

import pytest
from app import db


def test_acesso_sem_login_redireciona_para_login(client):
    """
    Tenta aceder à rota /planos/criar sem autenticação.
    Espera-se um redirecionamento para a página de login.
    """
    response = client.get("/planos/criar", follow_redirects=True)

    assert response.status_code == 200
    assert (
        "iniciar sessão" in response.get_data(as_text=True).lower()
        or "login" in response.get_data(as_text=True).lower()
    )
