"""
test_homepage.py

Teste simples à página principal do Meal Planner:
✅ Verifica se a página '/' está acessível (retorna HTTP 200)
"""


def test_home_page(client):
    """
    Testa se a página principal (rota '/') responde com sucesso.
    """
    response = client.get("/")
    assert response.status_code == 200
