"""
test_favoritar_receita.py

Testa adicionar e remover uma receita dos favoritos de um utilizador autenticado.
"""

import pytest
from app.models.user import User
from app.models.recipe import Recipe
from app.models.category import Category
from app.models.favorites import Favorites
from app import db


@pytest.fixture(autouse=True)
def setup_dados(client):
    """
    Prepara utilizador, categoria, receita e faz login.
    """
    with client.application.app_context():

        utilizador = User(
            nome="Utilizador Favorito", email="favorito@email.com", nivel=1
        )
        utilizador.set_password("senha123")
        db.session.add(utilizador)

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
            utilizador_id=utilizador.id,
        )
        db.session.add(receita)
        db.session.commit()

        # Login
        client.post(
            "/auth/login",
            data={"email": "favorito@email.com", "password": "senha123"},
            follow_redirects=True,
        )


def test_adicionar_remover_favorito(client):
    """
    Testa adicionar e remover uma receita dos favoritos.
    """
    # Adicionar favorito
    response_add = client.post("/favorites/adicionar/1", follow_redirects=True)
    assert response_add.status_code == 200
    assert "Receita adicionada aos favoritos" in response_add.get_data(as_text=True)

    # Confirmar na BD
    with client.application.app_context():
        favorito = Favorites.query.filter_by(receita_id=1, utilizador_id=1).first()
        assert favorito is not None

    # Remover favorito
    response_remove = client.post("/favorites/remover/1", follow_redirects=True)
    assert response_remove.status_code == 200
    assert "Receita removida dos favoritos" in response_remove.get_data(as_text=True)

    # Confirmar remoção
    with client.application.app_context():
        favorito = Favorites.query.filter_by(receita_id=1, utilizador_id=1).first()
        assert favorito is None
