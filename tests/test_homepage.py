"""
test_homepage.py

Teste simples à página principal do Meal Planner:
✅ Verifica se a página '/' está acessível (retorna HTTP 200)
"""

import sys
import os
import pytest

# Adiciona o caminho da raiz do projeto ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home_page(client):
    """
    Testa se a página principal (rota '/') responde com sucesso.
    """
    response = client.get("/")
    assert response.status_code == 200
