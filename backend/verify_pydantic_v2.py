"""
Verify Pydantic V2 compatibility by directly testing schema validation.
Run this script with: python verify_pydantic_v2.py
"""
import sys
import json
from datetime import date

# Add the project root to the Python path
sys.path.insert(0, '.')

# Import the schemas we want to test
from app.modules.citizenship.schemas.atualizacao_b_i import AtualizacaoBIBase
from app.modules.citizenship.schemas.emissao_b_i import EmissaoBIBase
from app.modules.citizenship.schemas.emissao_passaporte import EmissaoPassaporteBase

def test_atualizacao_bi():
    """Test AtualizacaoBIBase schema."""
    print("\nTesting AtualizacaoBIBase...")
    data = {
        "nome_completo": "Test User",
        "nome_pai": "Father Name",
        "nome_mae": "Mother Name",
        "data_nascimento": "2000-01-01",
        "local_nascimento": "Test Location",
        "estado_civil": "Solteiro",
        "genero": "M",
        "altura": "1.75",
        "residencia": "Test Address",
        "distrito": "Test District",
        "posto_administrativo": "Test Post",
        "localidade": "Test Locality",
        "bairro": "Test Neighborhood",
        "telefone": "123456789",
        "email": "test@example.com",
        "documento_identificacao": "123456789LA123",
        "comprovativo_residencia": "residence_proof.pdf",
        "fotografia": "photo.jpg"
    }
    
    try:
        model = AtualizacaoBIBase(**data)
        print("✅ AtualizacaoBIBase validation successful!")
        print(f"  - nome_completo: {model.nome_completo}")
        print(f"  - data_nascimento: {model.data_nascimento}")
        return True
    except Exception as e:
        print(f"❌ AtualizacaoBIBase validation failed: {e}")
        return False

def test_emissao_bi():
    """Test EmissaoBIBase schema."""
    print("\nTesting EmissaoBIBase...")
    data = {
        "nome_completo": "Test User",
        "nome_pai": "Father Name",
        "nome_mae": "Mother Name",
        "data_nascimento": "2000-01-01",
        "local_nascimento": "Test Location",
        "estado_civil": "Solteiro",
        "genero": "M",
        "altura": "1.75",
        "residencia": "Test Address",
        "distrito": "Test District",
        "posto_administrativo": "Test Post",
        "localidade": "Test Locality",
        "bairro": "Test Neighborhood",
        "telefone": "123456789",
        "email": "test@example.com",
        "documento_identificacao": "123456789LA123",
        "comprovativo_residencia": "residence_proof.pdf",
        "fotografia": "photo.jpg"
    }
    
    try:
        model = EmissaoBIBase(**data)
        print("✅ EmissaoBIBase validation successful!")
        print(f"  - nome_completo: {model.nome_completo}")
        print(f"  - data_nascimento: {model.data_nascimento}")
        return True
    except Exception as e:
        print(f"❌ EmissaoBIBase validation failed: {e}")
        return False

def test_emissao_passaporte():
    """Test EmissaoPassaporteBase schema."""
    print("\nTesting EmissaoPassaporteBase...")
    data = {
        "numero_bi": "123456789LA123",
        "nome_completo": "Test User",
        "data_nascimento": "2000-01-01",
        "local_nascimento": "Test Location",
        "nome_pai": "Father Name",
        "nome_mae": "Mother Name",
        "estado_civil": "Solteiro",
        "genero": "M",
        "altura": "1.75",
        "residencia": "Test Address",
        "telefone": "123456789",
        "email": "test@example.com",
        "motivo_viagem": "Turismo",
        "pais_destino": "Portugal",
        "data_prevista_viagem": "2023-12-31",
        "documento_identificacao": "123456789LA123",
        "comprovativo_residencia": "residence_proof.pdf",
        "fotografia": "photo.jpg"
    }
    
    try:
        model = EmissaoPassaporteBase(**data)
        print("✅ EmissaoPassaporteBase validation successful!")
        print(f"  - nome_completo: {model.nome_completo}")
        print(f"  - data_nascimento: {model.data_nascimento}")
        return True
    except Exception as e:
        print(f"❌ EmissaoPassaporteBase validation failed: {e}")
        return False

if __name__ == "__main__":
    print("\n🔍 Verifying Pydantic V2 Compatibility\n" + "="*50)
    
    results = {
        "AtualizacaoBIBase": test_atualizacao_bi(),
        "EmissaoBIBase": test_emissao_bi(),
        "EmissaoPassaporteBase": test_emissao_passaporte()
    }
    
    print("\n" + "="*50)
    print("\n📊 Test Results:")
    for name, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status} - {name}")
    
    all_passed = all(results.values())
    if all_passed:
        print("\n🎉 All Pydantic V2 compatibility tests passed!")
    else:
        failed = [name for name, success in results.items() if not success]
        print(f"\n❌ Some tests failed: {', '.join(failed)}")
    
    sys.exit(0 if all_passed else 1)
