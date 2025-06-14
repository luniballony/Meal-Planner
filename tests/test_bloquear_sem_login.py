"""
test_bloquear_sem_login.py

Testa se um utilizador não autenticado é impedido de bloquear/desbloquear/ver receitas bloqueadas.
"""

import pytest
from app.models.recipe import Recipe
from app.models.category import Category
from app import db


@pytest.fixture(autouse=True)
def setup_dados(client):
    """
    Cria categoria e receita (mas não faz login).
    """
    with client.application.app_context():

        categoria = Category(nome="Pratos")
        db.session.add(categoria)
        db.session.commit()

        receita = Recipe(
            titulo="Receita Bloqueada",
            descricao="Descrição da receita",
            ingredientes="ingredientes",
            instrucoes="instrucoes",
            tempo_preparacao=15,
            dificuldade=1,
            tags="teste",
            categoria_id=categoria.id,
            publicada=True,
            aprovada=True,
            fonte="utilizador",
            utilizador_id=1,
        )
        db.session.add(receita)
        db.session.commit()


def test_bloquear_receita_sem_login(client):
    """
    Testa a funcionalidade de bloqueio de receita SEM login.
    """
    # Supondo que a receita criada tem id=1
    response = client.post("/blocked/bloquear/1", follow_redirects=True)
    assert response.status_code == 200
    assert "Precisas de iniciar sessão para bloquear receitas." in response.get_data(
        as_text=True
    )

    # remover de bloqueadas
    response_remove = client.post("/blocked/desbloquear/1", follow_redirects=True)
    assert response_remove.status_code == 200
    assert (
        "Precisas de iniciar sessão para desbloquear receitas."
        in response_remove.get_data(as_text=True)
    )

    # ver receitas bloqueadas
    response_view_blocked = client.get("/blocked/bloqueadas", follow_redirects=True)
    assert response_view_blocked.status_code == 200
    assert (
        "Precisas de iniciar sessão para ver receitas bloqueadas."
        in response_view_blocked.get_data(as_text=True)
    )
