"""
test_bloquear_receita.py

Testa se um utilizador consegue bloquear uma receita e se o bloqueio é aplicado corretamente.
"""

import pytest
from app.models.user import User
from app.models.recipe import Recipe
from app.models.blocked_recipe import BlockedRecipe
from app.models.category import Category
from app import db


@pytest.fixture(autouse=True)
def setup_dados(client):
    """
    Prepara utilizador, categoria e receita antes de cada teste. Faz login.
    """
    with client.application.app_context():

        utilizador = User(
            nome="Utilizador Bloqueio", email="bloqueio@email.com", nivel=1
        )
        utilizador.set_password("senha123")
        db.session.add(utilizador)

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
            utilizador_id=utilizador.id,
        )
        db.session.add(receita)
        db.session.commit()

        # Login do utilizador (simula sessão)
        client.post(
            "/auth/login",
            data={"email": "bloqueio@email.com", "password": "senha123"},
            follow_redirects=True,
        )


def test_bloquear_receita(client):
    """
    Testa a funcionalidade de bloqueio de receita.
    """
    # Supomos que a receita criada tem id=1
    response = client.post("/blocked/bloquear/1", follow_redirects=True)

    assert response.status_code == 200
    assert "Receita bloqueada com sucesso" in response.get_data(as_text=True)

    # Verificar se o bloqueio foi gravado na BD
    with client.application.app_context():
        bloqueio = BlockedRecipe.query.filter_by(receita_id=1, utilizador_id=1).first()
        assert bloqueio is not None

    # Remover de bloqueadas
    response_remove = client.post("/blocked/desbloquear/1", follow_redirects=True)
    assert response_remove.status_code == 200
    assert "Receita desbloqueada com sucesso!" in response_remove.get_data(as_text=True)

    # Verificar se o bloqueio foi removido na BD
    with client.application.app_context():
        bloqueio = BlockedRecipe.query.filter_by(receita_id=1, utilizador_id=1).first()
        assert bloqueio is None
