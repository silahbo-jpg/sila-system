# Guia de Testes do Módulo de Reclamações (Complaints)

## Visão Geral
Este documento descreve a estratégia de testes para o módulo de reclamações, incluindo limitações atuais e abordagens recomendadas para validação.

## Estrutura de Testes

### Testes Isolados (Recomendado)
Os testes isolados são a abordagem mais confiável atualmente, pois não dependem de configurações externas ou do banco de dados.

- **Localização**: `tests/modules/complaints/test_isolated.py`
- **Como executar**:
  ```bash
  python -m tests.modules.complaints.test_isolated
  ```
- **Cobertura**:
  - Testes de CRUD básico
  - Testes de validação de dados
  - Testes de regras de negócio

### Testes de Serviço (Limitado)
Testes de unidade para os serviços, mas com limitações devido às dependências do projeto.

- **Localização**: `tests/modules/complaints/test_service.py`
- **Status**: Requer ajustes no ambiente de teste para executar

### Testes de Integração (Limitado)
Testes de endpoints usando FastAPI TestClient.

- **Localização**: `tests/modules/complaints/test_endpoints.py`
- **Status**: Requer ajustes no ambiente de teste para executar

## Limitações Conhecidas

1. **Dependências Externas**:
   - O módulo depende de configurações globais do projeto
   - O `conftest.py` global é carregado automaticamente pelo pytest
   - Dependências como `app.db.prisma_client` não estão disponíveis no ambiente de teste

2. **Problemas com pytest**:
   - O pytest carrega automaticamente o `conftest.py` da raiz
   - Dificuldade em isolar os testes do módulo
   - Erros de importação devido a dependências não resolvidas

## Abordagem Recomendada

### 1. Testes Isolados
```python
# Exemplo de teste isolado
def test_create_complaint():
    # Configuração
    service = MockComplaintService()
    
    # Execução
    result = service.create_complaint(
        {"title": "Teste", "description": "Descrição"}, 
        user_id=1
    )
    
    # Verificação
    assert result["title"] == "Teste"
```

### 2. Testes de Contrato
```python
# Verifica se os endpoints retornam os schemas esperados
def test_complaint_schema():
    schema = ComplaintResponse.schema()
    assert "id" in schema["properties"]
    assert "title" in schema["properties"]
```

### 3. Testes de Integração com Mocks
```python
@patch('app.modules.complaints.services.ComplaintService')
async def test_endpoint_with_mock(mock_service, client):
    # Configura o mock
    mock_service.return_value.get_complaints.return_value = [...]
    
    # Chama o endpoint
    response = client.get("/api/complaints/")
    
    # Verificações
    assert response.status_code == 200
```

## Próximos Passos

1. **Refatoração para Injeção de Dependência**:
   - Modificar os serviços para receber dependências como parâmetros
   - Facilitar o mock de dependências em testes

2. **Ambiente de Teste Isolado**:
   - Criar um ambiente virtual dedicado para testes
   - Instalar apenas as dependências necessárias

3. **Docker para Testes**:
   - Usar containers para isolar o ambiente de teste
   - Garantir consistência entre ambientes

## Executando os Testes

### Testes Isolados
```bash
# Navegue até o diretório do projeto
cd /caminho/para/projeto

# Execute os testes isolados
python -m tests.modules.complaints.test_isolated
```

### Testes com Pytest (quando disponível)
```bash
# Execute apenas os testes do módulo complaints
pytest tests/modules/complaints/ -v
```

## Solução de Problemas

### Erro: Módulo não encontrado
Se encontrar erros de importação, verifique:
1. Se o PYTHONPATH está configurado corretamente
2. Se todas as dependências estão instaladas
3. Se o ambiente virtual está ativado

### Erro: Dependências não resolvidas
Para testes que dependem de serviços externos:
1. Use mocks para simular as dependências
2. Considere usar a injeção de dependência
3. Documente as dependências necessárias

## Conclusão
Embora existam limitações na execução de testes de integração e unitários tradicionais, a abordagem de testes isolados fornece uma maneira eficaz de validar a lógica principal do módulo de reclamações. Recomenda-se investir na refatoração do código para melhorar a testabilidade no futuro.

