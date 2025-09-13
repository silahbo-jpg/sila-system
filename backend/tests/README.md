# Testes Automatizados

Este diretório contém os testes automatizados para o projeto SILA.

## Estrutura de Diretórios

```
tests/
├── __init__.py
├── conftest.py           # Configurações globais para testes
├── modules/              # Testes organizados por módulo
│   ├── auth/            # Testes de autenticação
│   ├── commercial/      # Testes do módulo comercial
│   ├── citizenship/     # Testes do módulo de cidadania
│   └── health/          # Testes de saúde da aplicação
└── utils/               # Utilitários para testes
    └── factories.py     # Fábricas para criação de objetos de teste
```

## Como Executar os Testes

### Pré-requisitos

Certifique-se de ter todas as dependências de desenvolvimento instaladas:

```bash
pip install -r requirements-test.txt
```

### Executando Todos os Testes

```bash
# Executa todos os testes com cobertura
./scripts/run_tests.sh

# Ou execute diretamente com pytest
pytest
```

### Executando Testes Específicos

```bash
# Testes de um módulo específico
pytest tests/modules/auth/

# Um arquivo de teste específico
pytest tests/modules/auth/test_login.py

# Uma função de teste específica
pytest tests/modules/auth/test_login.py::test_login_success

# Executar testes com cobertura detalhada
pytest --cov=app --cov-report=term-missing
```

### Geração de Relatórios

- **Relatório HTML**: Gera um relatório HTML em `htmlcov/`
  ```bash
  pytest --cov=app --cov-report=html
  ```

- **Relatório XML** (para integração com CI/CD)
  ```bash
  pytest --junitxml=test-results.xml --cov=app --cov-report=xml
  ```

## Convenções de Testes

- Nomes de arquivos de teste devem começar com `test_`
- Funções de teste devem começar com `test_`
- Use fixtures para código reutilizável
- Mantenha os testes isolados e independentes
- Teste casos de sucesso e falha

## Boas Práticas

1. **Fixtures**: Use fixtures para configurar o ambiente de teste
2. **Factories**: Use factories para criar objetos de teste
3. **Asserções**: Use asserções específicas
4. **Cobertura**: Mantenha a cobertura de código acima de 80%
5. **Testes de Integração**: Teste fluxos completos

## Dicas para Depuração

Para executar um teste em modo de depuração:

```bash
pytest -vvsx --pdb tests/modules/auth/test_login.py::test_login_failure
```

Isso irá:
- `-v`: Mostrar saída detalhada
- `-s`: Mostrar saída do print
- `-x`: Parar no primeiro erro
- `--pdb`: Iniciar o debugger em caso de falha

