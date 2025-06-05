"""
test_bloquear_receita.py

Testa se um utilizador consegue bloquear uma receita e se o bloqueio é aplicado corretamente.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app, db
from app.models.user import User
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

        # Criar utilizador
        utilizador = User(
            nome="Utilizador Bloqueio", email="bloqueio@email.com", nivel=1
        )
        utilizador.set_password("senha123")
        db.session.add(utilizador)

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
            utilizador_id=utilizador.id,
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
    # Supomos que a receita criada tem id=1
    response = client.post("/blocked/bloquear/1", follow_redirects=True)

    assert response.status_code == 200
    assert "Receita bloqueada com sucesso" in response.get_data(as_text=True)

    # Verificar se o bloqueio foi gravado na BD
    bloqueio = BlockedRecipe.query.filter_by(receita_id=1, utilizador_id=1).first()
    assert bloqueio is not None

    # remover de bloqueadas
    response_remove = client.post("/blocked/desbloquear/1", follow_redirects=True)
    assert response_remove.status_code == 200
    assert "Receita desbloqueada com sucesso!" in response_remove.get_data(as_text=True)

    # Verificar se o bloqueio foi removido na BD
    bloqueio = BlockedRecipe.query.filter_by(receita_id=1, utilizador_id=1).first()
    assert bloqueio is None
