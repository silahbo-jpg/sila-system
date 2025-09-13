"""Test script to verify FastAPI app setup."""
import sys
from fastapi.testclient import TestClient

# Add backend to Python path
sys.path.insert(0, '.')

try:
    from app.main import app
    print("✅ Successfully imported app")
    
    client = TestClient(app)
    
    # Test health endpoint
    response = client.get("/health/")
    print(f"Health endpoint status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test creating a health record
    test_data = {
        "tipo_consulta": "Teste de integração",
        "data_consulta": "2025-08-16T10:00:00",
        "diagnostico": "Teste",
        "tratamento": "Nenhum",
        "observacoes": "Teste de integração",
        "cidadao_id": "00000000-0000-0000-0000-000000000000"
    }
    
    response = client.post("/health/", json=test_data)
    print(f"\nCreate record status: {response.status_code}")
    print(f"Response: {response.json()}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

