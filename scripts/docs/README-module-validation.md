# Validação de Integridade de Módulos

Este diretório contém scripts para validar a integridade dos módulos do sistema SILA. Os scripts verificam a estrutura dos módulos, a sintaxe do código Python, a presença de arquivos `__init__.py` e a existência de padrões proibidos (como referências ao SQLAlchemy).

## Scripts Disponíveis

### validate-module-integrity.py

Script Python que realiza uma validação completa dos módulos do sistema.

**Funcionalidades:**
- Verificação de sintaxe Python usando `py_compile`
- Detecção de padrões proibidos (SQLAlchemy, etc.)
- Verificação da presença de arquivos `__init__.py`
- Validação da estrutura dos módulos
- Geração de relatórios detalhados em formato Markdown

**Uso:**
```bash
python scripts/validate-module-integrity.py [--path CAMINHO] [--report CAMINHO_RELATORIO] [--verbose] [--quiet]
```

**Opções:**
- `--path`: Caminho para validar (padrão: diretório do projeto)
- `--report`: Caminho para salvar o relatório (padrão: reports/module_integrity_TIMESTAMP.md)
- `--verbose`: Exibir informações detalhadas durante a execução
- `--quiet`: Exibir apenas erros e avisos

### validate-module-integrity.ps1

Versão PowerShell do script de validação, com as mesmas funcionalidades do script Python.

**Uso:**
```powershell
.\scripts\validate-module-integrity.ps1
```

## Relatórios

Os scripts geram relatórios detalhados em formato Markdown, que incluem:

- Resumo da validação
- Verificação de arquivos `__init__.py`
- Verificação de padrões proibidos
- Detalhes por módulo
- Próximos passos recomendados

Os relatórios são salvos no diretório `reports/` com um timestamp no nome do arquivo.

## Integração com CI/CD

Os scripts de validação podem ser integrados ao pipeline de CI/CD para garantir que todos os módulos estejam íntegros antes do deploy.

**Exemplo de integração com GitHub Actions:**

```yaml
name: Validação de Módulos

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
    - name: Validate modules
      run: |
        python scripts/validate-module-integrity.py --verbose
    - name: Upload validation report
      uses: actions/upload-artifact@v2
      with:
        name: validation-report
        path: reports/module_integrity_*.md
```

## Próximos Passos

- Adicionar validação de estilo de código (PEP 8)
- Implementar como hook de pre-commit
- Adicionar testes unitários para os scripts de validação
- Expandir para validar outros aspectos do sistema
