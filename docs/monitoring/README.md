# Monitoramento e Métricas

Este documento descreve o sistema de monitoramento implementado no SILA, incluindo como usar as métricas, configurar alertas e estender o monitoramento.

## Visão Geral

O sistema de monitoramento do SILA é composto por:

1. **Frontend**: Rastreamento de erros, métricas de desempenho e análise de uso.
2. **Backend**: Coleta de métricas, rastreamento de erros e verificação de integridade.
3. **Infraestrutura**: Monitoramento de recursos e alertas.

## Configuração

### Frontend

O frontend usa as seguintes variáveis de ambiente para configurar o monitoramento:

```env
# .env.development ou .env.production
VITE_API_BASE_URL=http://localhost:8000
VITE_ENABLE_LOGGING=true
VITE_SENTRY_DSN=seu-dsn-do-sentry
VITE_GOOGLE_ANALYTICS_ID=seu-ga-id
VITE_APP_VERSION=1.0.0
```

### Backend

O backend usa as seguintes configurações:

```env
# .env
ENABLE_MONITORING=true
SENTRY_DSN=seu-dsn-do-sentry
ENVIRONMENT=development|staging|production
```

## Uso

### Frontend

#### Rastreamento de Erros

```typescript
import { captureError } from '@/services/monitoring/analytics';

try {
  // Código que pode lançar um erro
} catch (error) {
  captureError(error, { 
    context: 'NomeDoComponente',
    user: currentUser.id,
    // Outros metadados úteis
  });
}
```

#### Rastreamento de Eventos

```typescript
import { trackEvent } from '@/services/monitoring/analytics';

// Rastreia um evento de clique no botão
const handleClick = () => {
  trackEvent('button_click', { 
    button_id: 'submit_form',
    form_name: 'user_registration'
  });
};
```

#### Rastreamento de Desempenho

```typescript
import { trackMetric } from '@/services/monitoring/analytics';

// Início da operação
const startTime = performance.now();

// Operação que queremos medir
await fetchData();

// Fim da operação
const duration = performance.now() - startTime;
trackMetric('data_fetch_duration', duration, { 
  data_type: 'user_profile'
});
```

### Backend

#### Endpoints de Monitoramento

- `GET /api/monitoring/metrics`: Retorna métricas da aplicação
- `GET /api/monitoring/health`: Verifica a saúde da aplicação
- `GET /api/monitoring/status`: Retorna o status e métricas do sistema

#### Rastreamento de Erros

```python
from app.services.monitoring import monitoring

try:
    # Código que pode lançar uma exceção
    result = some_operation()
except Exception as e:
    # Captura a exceção para rastreamento
    monitoring.capture_exception(e, {
        'context': 'NomeDaFuncao',
        'user_id': current_user.id if current_user else None,
        'data': {'key': 'value'}
    })
    raise
```

#### Métricas Personalizadas

```python
from app.services.monitoring import monitoring

# Incrementa um contador
monitoring.increment_counter('user_login', {'status': 'success'})

# Registra um valor em um histograma
monitoring.record_histogram('request_processing_time', 0.150)  # segundos
```

#### Medição de Tempo de Operação

```python
from app.services.monitoring import monitoring

# Usando como decorador
@monitoring.time_operation('user_import', {'source': 'csv'})
async def import_users_from_csv(file_path: str):
    # Código para importar usuários
    pass

# Ou usando como gerenciador de contexto
with monitoring.time_operation('process_data_batch', {'batch_size': len(data)}):
    process_large_dataset(data)
```

## Alertas

### Configuração de Alertas

Os alertas podem ser configurados nos seguintes níveis:

1. **Erros não tratados**: Capturados automaticamente pelo Sentry
2. **Métricas de negócio**: Configuradas no painel do Google Analytics
3. **Monitoramento de saúde**: Verificações de saúde personalizadas

### Exemplo de Alerta para Erros

```python
# No serviço de monitoramento do backend
try:
    # Operação que pode falhar
    result = some_operation()
except Exception as e:
    monitoring.capture_exception(e, {
        'context': 'process_payment',
        'user_id': user_id,
        'amount': amount
    })
    
    # Envia um alerta para o canal de monitoramento
    monitoring.capture_message(
        'Falha ao processar pagamento',
        level='error',
        extra_data={
            'user_id': user_id,
            'amount': amount,
            'error': str(e)
        }
    )
    raise
```

## Monitoramento de Desempenho

### Frontend

O frontend rastreia automaticamente:
- Tempo de carregamento da página
- Chamadas de API
- Erros de JavaScript

### Backend

O backend rastreia automaticamente:
- Tempo de resposta das requisições HTTP
- Uso de CPU e memória
- Erros de servidor

## Personalização

### Adicionando Novas Métricas

1. **Frontend**: Adicione novas funções em `src/services/monitoring/analytics.ts`
2. **Backend**: Use os métodos existentes em `app/services/monitoring.py`

### Configuração Adicional

Para configurações avançadas, consulte a documentação do [Sentry](https://docs.sentry.io/) e [Google Analytics](https://developers.google.com/analytics).

## Solução de Problemas

### Erros Comuns

1. **Métricas não aparecendo**:
   - Verifique se o monitoramento está habilitado (`ENABLE_MONITORING=true`)
   - Verifique os logs do servidor para erros

2. **Erros de autenticação no Sentry/GA**:
   - Verifique se as chaves de API estão corretas
   - Verifique as permissões do serviço

3. **Alta latência**:
   - Verifique se as chamadas de monitoramento estão afetando o desempenho
   - Considere usar processamento em lote para métricas não críticas

## Próximos Passos

1. Implementar painéis de monitoramento personalizados
2. Adicionar mais métricas de negócio
3. Configurar alertas proativos para problemas de desempenho
4. Implementar rastreamento de usuários anônimos
5. Adicionar suporte a mais ferramentas de monitoramento

