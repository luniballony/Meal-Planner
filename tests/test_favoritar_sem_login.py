"""
test_favoritar_sem_login.py

Testa adicionar e remover uma receita dos favoritos sem login efetuado.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app, db
from app.models.recipe import Recipe
from app.models.category import Category


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["WTF_CSRF_ENABLED"] = False

    with app.app_context():
        db.drop_all()
        db.create_all()

        # Criar categoria
        categoria = Category(nome="Sopas")
        db.session.add(categoria)
        db.session.commit()

        # Criar receita
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

    with app.test_client() as client:
        yield client


def test_adicionar_remover_ver_favorito_sem_login(client):
    """
    Testa adicionar e remover uma receita dos favoritos.
    """
    # Adicionar favorito
    response_add = client.post("/favorites/adicionar/1", follow_redirects=True)
    assert response_add.status_code == 200
    assert "Precisas de iniciar sessão para adicionar favoritos." in response_add.get_data(as_text=True)

    # Remover favorito
    response_remove = client.post("/favorites/remover/1", follow_redirects=True)
    assert response_remove.status_code == 200
    assert "Precisas de iniciar sessão para remover favoritos." in response_remove.get_data(as_text=True)

    # ver favoritos
    response_view = client.get("/favorites/ver", follow_redirects=True)
    assert response_view.status_code == 200
    assert "Precisas de iniciar sessão para ver os favoritos." in response_view.get_data(as_text=True)
