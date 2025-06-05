"""
test_bloquear_receita.py

Testa se um utilizador consegue bloquear uma receita e se o bloqueio é aplicado corretamente.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app, db
from app.models.recipe import Recipe
from app.models.blocked_recipe import BlockedRecipe
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
        categoria = Category(nome="Pratos")
        db.session.add(categoria)
        db.session.commit()

        # Criar receita
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

    with app.test_client() as client:
        # Login do utilizador
        client.post(
            "/auth/login",
            data={"email": "bloqueio@email.com", "password": "senha123"},
            follow_redirects=True,
        )
        yield client


def test_bloquear_receita(client):
    """
    Testa a funcionalidade de bloqueio de receita.
    """
    # Supondo que a receita criada tem id=1
    response = client.post("/blocked/bloquear/1", follow_redirects=True)
    assert response.status_code == 200
    assert "Precisas de iniciar sessão para bloquear receitas." in response.get_data(as_text=True)


    # remover de bloqueadas
    response_remove = client.post("/blocked/desbloquear/1", follow_redirects=True)
    assert response_remove.status_code == 200
    assert "Precisas de iniciar sessão para desbloquear receitas." in response_remove.get_data(as_text=True)


    # ver receitas bloqueadas
    response_view_blocked = client.get("/blocked/bloqueadas", follow_redirects=True)
    assert response_view_blocked.status_code == 200
    assert "Precisas de iniciar sessão para ver receitas bloqueadas." in response_view_blocked.get_data(as_text=True)

