# Testes de Performance - Módulo Citizenship

Este diretório contém os testes de performance e carga para o módulo Citizenship da aplicação Sila System.

## Configuração

1. **Pré-requisitos**
   - Python 3.8+
   - pip
   - Servidor da aplicação em execução

2. **Instalação das dependências**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configuração do ambiente**
   Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
   ```
   ADMIN_EMAIL=seu_email@postgres.com
   ADMIN_PASSWORD=sua_senha
   API_BASE_URL=http://localhost:8000
   ```

## Executando os Testes

### Opção 1: Interface Web (Recomendado para testes iniciais)
```bash
locust -f citizenship_load_test.py --host=http://localhost:8000
```
Acesse `http://localhost:8089` no navegador para ver a interface do Locust.

### Opção 2: Linha de Comando (Para CI/CD)
```bash
./run_tests.sh
```

## Tipos de Usuários de Teste

1. **CitizenTestUser**
   - Testa operações básicas de CRUD de cidadãos
   - Peso: 60% do tráfego
   - Comportamento: 1-5 segundos entre requisições

2. **AtestadoTestUser**
   - Testa operações relacionadas a atestados
   - Peso: 30% do tráfego
   - Comportamento: 2-10 segundos entre requisições

3. **ReportTestUser**
   - Testa geração de relatórios e PDFs
   - Peso: 10% do tráfego
   - Comportamento: 5-15 segundos entre requisições

## Análise dos Resultados

Após a execução, os seguintes arquivos serão gerados no diretório `reports/`:

- `performance_report_<timestamp>.html`: Relatório HTML interativo
- `performance_<timestamp>_stats.csv`: Estatísticas agregadas
- `performance_<timestamp>_failures.csv`: Falhas ocorridas
- `performance_<timestamp>_exceptions.csv`: Exceções capturadas

### Métricas Importantes

1. **Tempo de Resposta**
   - Média: Deve estar abaixo dos limiares definidos em `config.py`
   - Percentil 95: 95% das requisições devem estar abaixo deste valor
   - Máximo: Identifica outliers problemáticos

2. **Taxa de Erros**
   - Deve ser inferior a 1% para produção
   - Verificar erros em `performance_<timestamp>_failures.csv`

3. **Requisições por Segundo (RPS)**
   - Indica a capacidade de processamento da API

## Otimizações Recomendadas

1. **Se o tempo de resposta estiver alto:**
   - Implementar cache para consultas frequentes
   - Otimizar consultas ao banco de dados
   - Considerar paginação em endpoints de listagem

2. **Se houver muitas falhas:**
   - Verificar logs do servidor
   - Ajustar timeouts se necessário
   - Validar autenticação/autorização

3. **Se a taxa de erros for alta:**
   - Revisar validações de entrada
   - Verificar disponibilidade de serviços dependentes
   - Implementar circuit breakers

## Próximos Passos

1. Integrar ao pipeline de CI/CD
2. Configurar monitoramento contínuo em produção
3. Estabelecer SLAs baseados nos resultados dos testes

