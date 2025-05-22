"""
test_recusar_receita_admin.py

Testa se um administrador consegue recusar (eliminar) uma receita pendente.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app, db
from app.models.user import User
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

        # Criar admin
        admin = User(nome="Admin", email="admin@email.com", nivel=3)
        admin.set_password("admin123")
        db.session.add(admin)

        # Criar categoria
        categoria = Category(nome="Massas")
        db.session.add(categoria)
        db.session.commit()

        # Criar receita pendente
        receita = Recipe(
            titulo="Lasanha",
            descricao="Camadas de massa e carne",
            ingredientes="massa, carne, queijo",
            instrucoes="1. Montar\n2. Forno",
            tempo_preparacao=45,
            dificuldade=2,
            tags="massa",
            categoria_id=categoria.id,
            publicada=False,
            aprovada=False,
            fonte="utilizador",
            utilizador_id=admin.id,
        )
        db.session.add(receita)
        db.session.commit()

    with app.test_client() as client:
        # Login como admin
        client.post(
            "/auth/login",
            data={"email": "admin@email.com", "password": "admin123"},
            follow_redirects=True,
        )
        yield client


def test_recusar_receita(client):
    """
    Testa a recusa (eliminação) da receita.
    """
    response = client.get("/admin/recusar_receita/1", follow_redirects=True)

    assert response.status_code == 200
    assert "Receita recusada (eliminada) com sucesso" in response.get_data(as_text=True)

    # Confirmar que a receita foi removida da BD
    from app.models.recipe import Recipe

    receita = db.session.get(Recipe, 1)
    assert receita is None
