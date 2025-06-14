"""
test_submeter_receita.py

Testa a submissão de uma nova receita válida por um utilizador autenticado.
"""

import pytest
from app.models.user import User
from app.models.category import Category
from app import db


@pytest.fixture(autouse=True)
def setup_utilizador_categoria(client):
    """
    Cria utilizador, categoria e faz login antes do teste.
    """
    with client.application.app_context():

        # Criar utilizador
        utilizador = User(nome="Utilizador Receita", email="receita@email.com", nivel=1)
        utilizador.set_password("senha123")
        db.session.add(utilizador)

        # Criar categoria necessária
        categoria = Category(nome="Sobremesas")
        db.session.add(categoria)
        db.session.commit()

        # Fazer login
        client.post(
            "/auth/login",
            data={"email": "receita@email.com", "password": "senha123"},
            follow_redirects=True,
        )


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
