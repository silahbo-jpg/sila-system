# Validações Automatizadas do Projeto SILA

Este documento descreve as validações automatizadas configuradas para o projeto SILA, incluindo pre-commit hooks e integração contínua com GitHub Actions.

## 🚀 Visão Geral

Configuramos um sistema abrangente de validação que inclui:

1. **Pre-commit Hooks**: Validações locais antes de cada commit
2. **GitHub Actions**: Pipeline de CI/CD para validação contínua
3. **Validação de Módulos**: Verificação da estrutura e implementação dos módulos
4. **Análise de Segurança**: Verificação de vulnerabilidades de segurança
5. **Testes Automatizados**: Execução de testes unitários e de integração

## 🔧 Configuração Local

### Pré-requisitos

- Python 3.12+
- pip (gerenciador de pacotes Python)
- Git

### Instalação

1. Instale o pre-commit globalmente:
   ```bash
   pip install pre-commit
   ```

2. No diretório raiz do projeto, instale os hooks do pre-commit:
   ```bash
   pre-commit install
   pre-commit install --hook-type pre-push
   ```

3. Instale as dependências de desenvolvimento:
   ```bash
   pip install -r backend/requirements.txt
   pip install black flake8 isort bandit pytest pytest-cov
   ```

### Uso

- **Antes de cada commit**: Os hooks são executados automaticamente
- **Execução manual**:
  ```bash
  # Executar todos os hooks em todos os arquivos
  pre-commit run --all-files
  
  # Validar estrutura dos módulos
  python scripts/module_validator.py --format markdown
  
  # Executar testes
  cd backend
  pytest --cov=app
  ```

## 🤖 GitHub Actions

### Workflows Configurados

1. **CI - Validação de Código e Módulos**
   - Disparado em: push para main/develop ou pull requests
   - Tarefas:
     - Validação de formatação (Black, isort)
     - Análise estática (Flake8, Bandit)
     - Validação de módulos personalizada
     - Execução de testes com cobertura
     - Análise de segurança
     - Verificação de dependências

### Acessando Relatórios

1. **Code Coverage**: Relatório de cobertura de código disponível no Codecov
2. **Relatório de Segurança**: Artefato gerado no GitHub Actions
3. **Relatório de Validação**: Artefato gerado no GitHub Actions

## 🔍 Hooks de Pré-commit

| Hook | Descrição | Ferramenta |
|------|-----------|------------|
| trailing-whitespace | Remove espaços em branco no final das linhas | pre-commit-hooks |
| end-of-file-fixer | Garante que arquivos terminam com uma nova linha | pre-commit-hooks |
| check-yaml | Valida arquivos YAML | pre-commit-hooks |
| check-json | Valida arquivos JSON | pre-commit-hooks |
| black | Formatação de código Python | Black |
| isort | Ordenação de imports | isort |
| flake8 | Análise estática de código | flake8 |
| bandit | Análise de segurança | bandit |
| validate-modules | Validação personalizada dos módulos | scripts/module_validator.py |
| detect-secrets | Detecção de segredos no código | detect-secrets |

## 🛠️ Solução de Problemas

### Erros Comuns

1. **Falha no pre-commit**
   - Execute `pre-commit install` novamente
   - Verifique as mensagens de erro específicas

2. **Problemas de formatação**
   - Execute `black .` para formatar automaticamente
   - Execute `isort .` para organizar os imports

3. **Falha na validação de módulos**
   - Verifique o relatório gerado em `validation-report.md`
  
4. **Problemas com dependências**
   - Atualize as dependências com `pip install -r backend/requirements.txt --upgrade`

## 📊 Métricas de Qualidade

- **Cobertura de Testes**: Alvo mínimo de 80%
- **Issues Críticas**: Zero tolerância
- **Dependências**: Sem vulnerabilidades conhecidas

## 📅 Próximos Passos

- [ ] Configurar notificações para falhas de validação
- [ ] Adicionar mais testes automatizados
- [ ] Integrar com ferramentas adicionais de análise estática
- [ ] Configurar revisão automática de código

## 📚 Recursos Úteis

- [Documentação do pre-commit](https://pre-commit.com/)
- [Documentação do GitHub Actions](https://docs.github.com/en/actions)
- [Guia de Estilo Python](https://www.python.org/dev/peps/pep-0008/)

