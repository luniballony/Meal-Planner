"""
test_submeter_receita_sem_login.py

Garante que a rota de submissão de receitas está protegida contra utilizadores não autenticados.
"""

from app import db


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
