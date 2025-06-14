"""
test_favoritar_sem_login.py

Testa adicionar e remover uma receita dos favoritos sem login efetuado.
"""

import pytest
from app.models.recipe import Recipe
from app.models.category import Category
from app import db


@pytest.fixture(autouse=True)
def setup_dados(client):
    """
    Cria categoria e receita (sem login).
    """
    with client.application.app_context():

        categoria = Category(nome="Sopas")
        db.session.add(categoria)
        db.session.commit()

        receita = Recipe(
            titulo="Sopa Teste",
            descricao="Deliciosa sopa de teste",
            ingredientes="água, legumes",
            instrucoes="cozinhar tudo",
            tempo_preparacao=15,
            dificuldade=1,
            tags="sopa,teste",
            categoria_id=categoria.id,
            publicada=True,
            aprovada=True,
            fonte="utilizador",
            utilizador_id=1,
        )
        db.session.add(receita)
        db.session.commit()


def test_adicionar_remover_ver_favorito_sem_login(client):
    """
    Testa adicionar e remover/ver favoritos sem autenticação.
    """
    # Adicionar favorito
    response_add = client.post("/favorites/adicionar/1", follow_redirects=True)
    assert response_add.status_code == 200
    assert (
        "Precisas de iniciar sessão para adicionar favoritos."
        in response_add.get_data(as_text=True)
    )

    # Remover favorito
    response_remove = client.post("/favorites/remover/1", follow_redirects=True)
    assert response_remove.status_code == 200
    assert (
        "Precisas de iniciar sessão para remover favoritos."
        in response_remove.get_data(as_text=True)
    )

    # Ver favoritos
    response_view = client.get("/favorites/ver", follow_redirects=True)
    assert response_view.status_code == 200
    assert (
        "Precisas de iniciar sessão para ver os favoritos."
        in response_view.get_data(as_text=True)
    )
