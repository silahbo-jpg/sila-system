# Scripts de Validação e Manutenção do SILA

Este diretório contém ferramentas para validação, monitoramento e manutenção dos módulos do sistema SILA.

## Módulo Validator

O `module_validator.py` é uma ferramenta para validar a estrutura e implementação dos módulos do sistema.

### Funcionalidades

- Validação da estrutura de arquivos dos módulos
- Verificação de implementação de código
- Validação de rotas da API
- Verificação de testes
- Geração de relatórios em múltiplos formatos

### Como Usar

#### Validação de Todos os Módulos

```bash
# Validar todos os módulos e exibir relatório no terminal
python3 scripts/module_validator.py --path /caminho/para/o/projeto

# Especificar formato de saída (markdown, json ou csv)
python3 scripts/module_validator.py --format json

# Salvar relatório em um arquivo
python3 scripts/module_validator.py --output relatorio.md
```

#### Validação de um Módulo Específico

```bash
# Validar apenas o módulo 'citizenship'
python3 scripts/module_validator.py --module citizenship
```

### Saída do Relatório

O relatório inclui:

- Status de cada módulo (✅ aprovado ou ❌ com problemas)
- Lista de verificações realizadas
- Detalhes sobre problemas encontrados
- Sugestões de correção
- Resumo geral
### Integração com CI/CD

```yaml
# Exemplo de configuração no GitHub Actions
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
        python-version: '3.9'
    - name: Validar módulos
      run: python3 scripts/module_validator.py --format markdown --output validation_report.md
    - name: Upload relatório
      uses: actions/upload-artifact@v2
      with:
        name: validation-report
        path: validation_report.md
```

## Indexador de Scripts

O `generate_script_index.py` é uma ferramenta para gerar um índice técnico de todos os scripts Python do projeto, categorizando-os por tipo e módulo.

### Funcionalidades

- Identificação e classificação automática de scripts (testes, utilitários, validadores, etc.)
- Agrupamento por módulo do sistema
- Geração de estatísticas de distribuição
- Criação de um índice técnico em formato Markdown

### Como Usar

#### Geração do Índice Técnico

```bash
# Gerar o índice técnico usando Python diretamente
python scripts/generate_script_index.py

# Ou usando o script PowerShell (recomendado no Windows)
.\scripts\generate-script-index.ps1
```

### Saída do Índice

O índice técnico é gerado em `docs/INDICE_TECNICO.md` e inclui:

- Estatísticas de distribuição por tipo de script
- Lista de testes organizados por módulo
- Lista de scripts utilitários
- Organização de scripts por módulo do sistema

### Integração com Outros Scripts

O indexador de scripts pode ser integrado ao processo de validação para manter a documentação técnica sempre atualizada.

### Integração com CI/CD

Para integrar a validação ao seu pipeline de CI/CD, você pode usar o código de saída:

```yaml
# Exemplo para GitHub Actions
- name: Validar Módulos
  run: |
    python3 scripts/module_validator.py --format markdown --output validation-report.md
    # Falha no pipeline se algum módulo não passar na validação
    if grep -q "❌" validation-report.md; then
      echo "::error::Alguns módulos falharam na validação. Verifique o relatório."
      exit 1
    fi
```

### Verificações Realizadas

1. **Estrutura de Arquivos**
   - Presença de arquivos obrigatórios
   - Conteúdo não vazio

2. **Código Python**
   - Exportação adequada em `__init__.py`
   - Implementação de modelos em `models.py`
   - Definição de schemas em `schemas.py`
   - Funções CRUD em `crud.py`
   - Implementação de serviços em `services.py`
   - Definição de endpoints em `endpoints.py`

3. **API**
   - Registro do roteador no módulo principal da API

4. **Testes**
   - Presença de diretório de testes
   - Existência de arquivos de teste
   - Cobertura de testes (simulada)

### Personalização

Você pode estender o validador criando novas classes de validação em `validators/` e registrando-as no `ModuleValidator`.

