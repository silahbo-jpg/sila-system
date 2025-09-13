"""
Test Pydantic models for compatibility with Pydantic V2.
Run this script with: python test_pydantic_models.py
"""
import sys
import json
from datetime import date, datetime
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, '.')

# Import the schemas we want to test
from app.modules.citizenship.schemas.atualizacao_b_i import (
    DocumentType, EstadoCivil, Genero,
    AtualizacaoBICreate, AtualizacaoBIRead, AtualizacaoBIUpdate, AtualizacaoBIList
)

def test_atualizacao_bi_create():
    """Test AtualizacaoBICreate model."""
    print("\nTesting AtualizacaoBICreate...")
    
    # Valid data
    data = {
        "numero_documento": "123456789LA123",
        "tipo_documento": "Bilhete de Identidade",
        "nome_completo": "Test User",
        "nome_mae": "Mother Name",
        "nome_pai": "Father Name",
        "data_nascimento": "2000-01-01",
        "naturalidade": "Luanda",
        "nacionalidade": "Angolana",
        "estado_civil": "Solteiro(a)",
        "genero": "Masculino",
        "altura": 1.75,
        "morada": "Rua Teste, 123",
        "codigo_postal": "1234-567",
        "localidade": "Luanda",
        "telefone": "923456789",
        "email": "test@example.com",
        "motivo_atualizacao": "Perda do documento"
    }
    
    # Test model creation
    try:
        model = AtualizacaoBICreate(**data)
        print("✅ AtualizacaoBICreate validation successful!")
        print(f"  - nome_completo: {model.nome_completo}")
        print(f"  - data_nascimento: {model.data_nascimento}")
        print(f"  - estado_civil: {model.estado_civil}")
        print(f"  - genero: {model.genero}")
        return True
    except Exception as e:
        print(f"❌ AtualizacaoBICreate validation failed: {e}")
        return False

def test_atualizacao_bi_read():
    """Test AtualizacaoBIRead model."""
    print("\nTesting AtualizacaoBIRead...")
    
    # Create a base model first
    create_data = {
        "numero_documento": "123456789LA123",
        "tipo_documento": "Bilhete de Identidade",
        "nome_completo": "Test User",
        "nome_mae": "Mother Name",
        "nome_pai": "Father Name",
        "data_nascimento": "2000-01-01",
        "naturalidade": "Luanda",
        "nacionalidade": "Angolana",
        "estado_civil": "Solteiro(a)",
        "genero": "Masculino",
        "altura": 1.75,
        "morada": "Rua Teste, 123",
        "codigo_postal": "1234-567",
        "localidade": "Luanda",
        "telefone": "923456789",
        "email": "test@example.com",
        "motivo_atualizacao": "Perda do documento"
    }
    
    # Add read-specific fields
    read_data = {
        **create_data,
        "id": 1,
        "data_submissao": "2023-09-07T10:00:00",
        "estado": "Pendente",
        "numero_processo": "AT/2023/12345"
    }
    
    # Test model creation
    try:
        model = AtualizacaoBIRead(**read_data)
        print("✅ AtualizacaoBIRead validation successful!")
        print(f"  - id: {model.id}")
        print(f"  - numero_processo: {model.numero_processo}")
        print(f"  - data_submissao: {model.data_submissao}")
        return True
    except Exception as e:
        print(f"❌ AtualizacaoBIRead validation failed: {e}")
        return False

def test_atualizacao_bi_update():
    """Test AtualizacaoBIUpdate model."""
    print("\nTesting AtualizacaoBIUpdate...")
    
    # Test data
    update_data = {
        "estado": "Em processamento",
        "numero_processo": "AT/2023/12345",
        "observacoes": "Documentação em análise"
    }
    
    # Test model creation
    try:
        model = AtualizacaoBIUpdate(**update_data)
        print("✅ AtualizacaoBIUpdate validation successful!")
        print(f"  - estado: {model.estado}")
        print(f"  - numero_processo: {model.numero_processo}")
        print(f"  - observacoes: {model.observacoes}")
        return True
    except Exception as e:
        print(f"❌ AtualizacaoBIUpdate validation failed: {e}")
        return False

def test_atualizacao_bi_list():
    """Test AtualizacaoBIList model."""
    print("\nTesting AtualizacaoBIList...")
    
    # Create a read model first
    read_data = {
        "id": 1,
        "numero_documento": "123456789LA123",
        "tipo_documento": "Bilhete de Identidade",
        "nome_completo": "Test User",
        "nome_mae": "Mother Name",
        "nome_pai": "Father Name",
        "data_nascimento": "2000-01-01",
        "naturalidade": "Luanda",
        "nacionalidade": "Angolana",
        "estado_civil": "Solteiro(a)",
        "genero": "Masculino",
        "altura": 1.75,
        "morada": "Rua Teste, 123",
        "codigo_postal": "1234-567",
        "localidade": "Luanda",
        "telefone": "923456789",
        "email": "test@example.com",
        "motivo_atualizacao": "Perda do documento",
        "data_submissao": "2023-09-07T10:00:00",
        "estado": "Pendente",
        "numero_processo": "AT/2023/12345"
    }
    
    # Create list data
    list_data = {
        "items": [read_data, {**read_data, "id": 2}],
        "total": 2
    }
    
    # Test model creation
    try:
        model = AtualizacaoBIList(**list_data)
        print("✅ AtualizacaoBIList validation successful!")
        print(f"  - total: {model.total}")
        print(f"  - items count: {len(model.items)}")
        print(f"  - first item id: {model.items[0].id}")
        return True
    except Exception as e:
        print(f"❌ AtualizacaoBIList validation failed: {e}")
        return False

if __name__ == "__main__":
    print("\n🔍 Testing Pydantic Models for Atualização de BI\n" + "="*70)
    
    results = {
        "AtualizacaoBICreate": test_atualizacao_bi_create(),
        "AtualizacaoBIRead": test_atualizacao_bi_read(),
        "AtualizacaoBIUpdate": test_atualizacao_bi_update(),
        "AtualizacaoBIList": test_atualizacao_bi_list()
    }
    
    print("\n" + "="*70)
    print("\n📊 Test Results:")
    for name, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status} - {name}")
    
    all_passed = all(results.values())
    if all_passed:
        print("\n🎉 All Pydantic model tests passed!")
    else:
        failed = [name for name, success in results.items() if not success]
        print(f"\n❌ Some tests failed: {', '.join(failed)}")
    
    # Write results to a file
    with open("pydantic_test_results.txt", "w") as f:
        f.write("Pydantic Model Test Results\n")
        f.write("=" * 50 + "\n\n")
        for name, success in results.items():
            status = "PASSED" if success else "FAILED"
            f.write(f"{name}: {status}\n")
        
        if all_passed:
            f.write("\n✅ All tests passed!")
        else:
            f.write(f"\n❌ Failed tests: {', '.join(failed)}")
    
    print("\n📝 Results written to: pydantic_test_results.txt")
    sys.exit(0 if all_passed else 1)
