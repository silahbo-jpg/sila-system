"""
Script para criar um arquivo de teste de exemplo.
"""

def create_test_file():
    """Cria um arquivo de teste de exemplo."""
    test_content = '''from fastapi.testclient import TestClient
from app.main import app

def test_example():
    """Teste de exemplo."""
    client = TestClient(app)
    response = client.get("/api/healthcheck")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
'''
    with open("tests/test_example.py", "w", encoding="utf-8") as f:
        f.write(test_content)
    print("Arquivo de teste criado com sucesso em 'tests/test_example.py'")

if __name__ == "__main__":
    create_test_file()

