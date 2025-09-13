# Changelog Técnico

## [v2025.08.11] - Correções de Sintaxe e Validação Automatizada

### Correções de Sintaxe
- Renomeado `nnnotification_service.py` → `notification_service.py`
- Corrigido docstring e nomes de campos malformados
- Tornado método `check_and_notify_password_expiration` assíncrono
- Todos os arquivos passaram na validação com `python -m py_compile`

### Melhorias de Infraestrutura
- Adicionado script `validate_py_compile.py` para validação completa de sintaxe Python
- Adicionado script PowerShell `validate-py-compile.ps1` para execução fácil da validação
- Integrado validador de sintaxe ao script `fix-all.ps1`
- Implementado suporte para validação seletiva de arquivos específicos
- Adicionada capacidade de ignorar diretórios problemáticos durante a validação
- Implementada geração de relatório de validação em formato .txt com estatísticas detalhadas
- Criado checklist de validação para onboarding em `VALIDATION_CHECKLIST.md`
- Adicionada medição de tempo de execução para análise de performance
- Implementado script `generate_script_index.py` para indexação automática de scripts Python
- Criado índice técnico em `docs/INDICE_TECNICO.md` com categorização por tipo e módulo
