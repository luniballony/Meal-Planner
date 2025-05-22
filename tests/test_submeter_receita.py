"""
test_submeter_receita.py

Testa a submissão de uma nova receita válida por um utilizador autenticado.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app, db
from app.models.user import User
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
        utilizador = User(nome="Utilizador Receita", email="receita@email.com", nivel=1)
        utilizador.set_password("senha123")
        db.session.add(utilizador)

        # Criar categoria necessária
        categoria = Category(nome="Sobremesas")
        db.session.add(categoria)
        db.session.commit()

    with app.test_client() as client:
        # Fazer login
        client.post(
            "/auth/login",
            data={"email": "receita@email.com", "password": "senha123"},
            follow_redirects=True,
        )
        yield client


def test_submeter_receita_valida(client):
    """
    Submete uma receita com dados válidos e verifica a resposta.
    """
    response = client.post(
        "/receitas/submeter",
        data={
            "titulo": "Bolo de Teste",
            "descricao": "Um bolo incrível de teste",
            "ingredientes": "- 2 ovos\n- 200g de açúcar",
            "instrucoes": "1. Misture tudo\n2. Leve ao forno",
            "tempo_preparacao": 30,
            "dificuldade": 2,
            "tags": "doce,bolo",
            "categoria_id": 1,
            "publica": True,
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "Receita submetida com sucesso" in response.get_data(as_text=True)
