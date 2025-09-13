# Checklist de Validação para Onboarding

Este documento contém o checklist de validação para o processo de onboarding de novos desenvolvedores e para garantir a qualidade do código no projeto.

## Checklist de Validação de Código

- [x] Sintaxe validada com py_compile
- [x] BOM removido de arquivos __init__.py
- [x] Strings não terminadas corrigidas
- [x] Scripts de validação integrados ao fix-all.ps1
- [x] Documentação atualizada
- [x] Validação de integridade de módulos
- [x] Verificação de padrões proibidos (SQLAlchemy)

## Processo de Validação

### 1. Validação de Sintaxe Python

A validação de sintaxe é realizada através do script `validate_py_compile.py`, que utiliza o módulo `py_compile` para verificar se todos os arquivos Python do projeto estão com a sintaxe correta.

```powershell
# Executar validação completa
.\scripts\validate-py-compile.ps1

# Validar diretórios específicos
.\scripts\validate-py-compile.ps1 backend/app
```

### 2. Remoção de BOM em Arquivos __init__.py

O script `fix-corrupted-content.py` remove o BOM (Byte Order Mark) dos arquivos __init__.py, que pode causar problemas de importação em Python.

### 3. Correção de Strings Não Terminadas

O script `fix_unterminated_strings.py` corrige strings não terminadas em arquivos Python, que são um erro comum de sintaxe.

### 4. Integração com fix-all.ps1

Todos os scripts de validação estão integrados ao script `fix-all.ps1`, que pode ser executado para realizar todas as correções e validações de uma só vez.

```powershell
.\scripts\fix-all.ps1
```

### 5. Atualização da Documentação

A documentação técnica é mantida atualizada no arquivo `CHANGELOG_TECNICO.md`, que registra todas as alterações realizadas no projeto.

## Relatórios de Validação

O script `validate_py_compile.py` gera relatórios de validação em formato .txt com as seguintes informações:

- Total de arquivos validados
- Quantos arquivos passaram / falharam
- Tempo total de execução
- Lista de arquivos com erro (se houver)

Os relatórios são salvos no diretório `reports/` na raiz do projeto.

## Integração com CI/CD

Os scripts de validação podem ser integrados ao pipeline de CI/CD para garantir que nenhum código com erro de sintaxe seja mesclado ao branch principal.

## Validação de Integridade de Módulos

A validação de integridade dos módulos é realizada através dos scripts `validate-module-integrity.py` e `validate-module-integrity.ps1`, que verificam:

- Estrutura dos módulos (arquivos obrigatórios)
- Presença de arquivos __init__.py em todos os diretórios necessários
- Padrões proibidos (referências ao SQLAlchemy)
- Sintaxe Python usando py_compile

```powershell
# Executar validação de integridade de módulos (Python)
python scripts/validate-module-integrity.py --verbose

# Executar validação de integridade de módulos (PowerShell)
.\scripts\validate-module-integrity.ps1
```

Os relatórios de validação são gerados em formato Markdown e salvos no diretório `reports/`.

Para mais detalhes, consulte o arquivo `README-module-validation.md`.

## Próximos Passos

- [ ] Integrar o validate_py_compile.py como hook de pré-commit do Git
- [ ] Integrar o validate-module-integrity.py como hook de pré-commit do Git
- [ ] Adicionar validação de estilo de código (PEP 8)
- [ ] Implementar testes automatizados para os scripts de validação
- [ ] Adicionar métricas de qualidade de código ao relatório de validação
