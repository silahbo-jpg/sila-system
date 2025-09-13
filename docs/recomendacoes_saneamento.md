# Recomendações para Saneamento do Projeto SILA

## Introdução

Este documento apresenta recomendações para o saneamento do projeto SILA, com foco na resolução de problemas de portabilidade entre WSL2 (Linux) e Windows 10, bem como na melhoria da organização e estrutura do projeto.

## Problemas Críticos de Portabilidade (WSL2 → Windows 10)

### Problema: Presença de arquivos compilados específicos para Linux

**Evidência:**
- Arquivos `.pyc` (bytecode Python)
- Arquivos `.so` (bibliotecas compartilhadas Linux)
- Diretórios `__pycache__`

**Risco:** Esses arquivos foram gerados no ambiente Linux (WSL2) e não funcionam no Windows. São binários e bytecode compilados para uma arquitetura e sistema diferente.

**Recomendações:**
1. Execute o script `scripts/clean_python_cache.ps1` para remover esses arquivos
2. Reinstale todas as dependências Python no ambiente Windows:
   ```powershell
   pip install --force-reinstall -r requirements.txt
   ```
3. Verifique se o arquivo `.gitignore` contém as entradas necessárias para evitar o versionamento desses arquivos

## Estrutura de Projeto Desorganizada / Híbrida

### Problema: Mistura de frontend, backend, testes, scripts e dependências

**Evidência:**
- `package.json`, `package-lock.json` → frontend ou Node.js
- `pip.conf`, `.env.example`, `Makefile` → backend Python/Django
- `cypress/` → testes E2E
- `prisma/` → Prisma ORM (Node.js)
- `migrate_to_postgres.sh` → script de migração (Linux)

**Recomendações:**
1. Organize o projeto em subprojetos claros:
   ```
   projeto-sila/
   ├── backend/          # Django, Python, requirements.txt
   ├── frontend/         # React, package.json, cypress/
   ├── mobileapp/        # App.tsx → React Native?
   ├── docs/
   ├── scripts/          # Scripts de utilidade
   └── .gitignore
   ```

2. Valide o uso do Prisma com Django:
   - Prisma é feito para Node.js/TypeScript. Não é compatível diretamente com Django.
   - Se estiver usando Prisma apenas no frontend, ok.
   - Se estiver tentando usá-lo como ORM no backend Python, é um erro arquitetural grave.

## Scripts e Compatibilidade com Windows

### Problema: Scripts .sh não funcionam nativamente no Windows

**Evidência:**
- `migrate_to_postgres.sh`
- `Makefile` (comandos Linux)

**Recomendações:**
1. Execute o script `scripts/convert_shell_to_powershell.ps1` para converter scripts .sh para PowerShell (.ps1)
2. Substitua Makefile por scripts Python ou pyinvoke

## Duplicidade e Arquivos de Backup no Versionamento

### Problema: Arquivos de backup no controle de versão

**Evidência:**
- Arquivos `.db` (bancos de dados SQLite)
- Arquivos `.sql` (dumps de banco de dados)
- Arquivos `.csv` (exportações de dados)

**Recomendações:**
1. Mova arquivos de banco de dados para o diretório `backups/` (use o script `scripts/clean_project.py`)
2. Atualize o `.gitignore` para excluir esses arquivos do versionamento

## Inconsistências nos Módulos

### Problema: Duplicidade de módulos e estrutura inconsistente

**Evidência:**
- Módulos `saude` e `health` existem simultaneamente
- Alguns módulos não seguem a estrutura padrão

**Recomendações:**
1. Execute o script `scripts/fix_module_structure.ps1` para verificar e corrigir a estrutura dos módulos
2. Padronize a nomenclatura dos módulos (escolha entre `saude` e `health`)

## Ações Recomendadas

### Imediatas

1. **Limpeza de arquivos compilados:**
   ```powershell
   # Execute o script de limpeza
   ./scripts/clean_python_cache.ps1
   ```

2. **Reinstalação de dependências:**
   ```powershell
   # Reinstale dependências Python
   pip install --force-reinstall -r requirements.txt
   
   # Reinstale dependências Node.js
   npm ci
   ```

3. **Conversão de scripts shell:**
   ```powershell
   # Execute o script de conversão
   ./scripts/convert_shell_to_powershell.ps1
   ```

4. **Correção da estrutura de módulos:**
   ```powershell
   # Execute o script de correção
   ./scripts/fix_module_structure.ps1
   ```

### Médio Prazo

1. **Reorganização da estrutura do projeto:**
   - Separe claramente frontend e backend
   - Padronize a estrutura de diretórios

2. **Revisão da arquitetura:**
   - Valide o uso do Prisma com Django
   - Padronize o ORM utilizado

3. **Documentação:**
   - Atualize a documentação com as novas estruturas
   - Documente o processo de desenvolvimento no Windows

## Conclusão

A migração de um projeto do WSL2 (Linux) para Windows 10 requer atenção especial aos arquivos compilados, scripts e estrutura do projeto. As recomendações acima visam garantir a portabilidade, manutenibilidade e estabilidade do projeto SILA no ambiente Windows.

Os scripts fornecidos no diretório `scripts/` automatizam grande parte do processo de saneamento, mas é importante revisar manualmente as alterações e garantir que tudo esteja funcionando corretamente após as modificações.
