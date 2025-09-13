# Métricas de Validação de CPF

Este documento descreve as métricas disponíveis para monitoramento do serviço de validação de CPF.

## Visão Geral

O sistema de validação de CPF expõe métricas em formato Prometheus que podem ser visualizadas no Grafana. Estas métricas ajudam a monitorar o desempenho, identificar problemas e tomar decisões baseadas em dados.

## Métricas Disponíveis

### `sila_cpf_validation_total`
- **Tipo**: Contador
- **Descrição**: Número total de validações de CPF realizadas
- **Labels**: `status` ("success" ou "error"), `source` (origem da validação)
- **Uso**: Monitorar volume de validações e taxa de erros

### `sila_cpf_validation_duration_seconds`
- **Tipo**: Histograma
- **Descrição**: Distribuição dos tempos de validação em segundos
- **Buckets**: [0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0]
- **Uso**: Identificar problemas de desempenho

### `sila_cpf_validation_cache_size`
- **Tipo**: Gauge
- **Descrição**: Número atual de itens no cache de CPF
- **Uso**: Monitorar uso de memória e eficiência do cache

### `sila_cpf_validation_cache_hits`
- **Tipo**: Contador
- **Descrição**: Número de acertos no cache
- **Uso**: Calcular taxa de acerto do cache

### `sila_cpf_validation_cache_misses`
- **Tipo**: Contador
- **Descrição**: Número de falhas no cache
- **Uso**: Calcular taxa de acerto do cache

## Métricas Derivadas Úteis

### Taxa de Acerto do Cache
```
(1 - (rate(sila_cpf_validation_cache_misses[5m]) / rate(sila_cpf_validation_total[5m]))) * 100
```

### Taxa de Erro
```
(rate(sila_cpf_validation_errors_total[5m]) / rate(sila_cpf_validation_total[5m])) * 100
```

### Taxa de Validações por Segundo
```
rate(sila_cpf_validation_total[5m])
```

## Alertas Configurados

| Nome | Condição | Severidade | Descrição |
|------|----------|------------|-----------|
| HighCPFValidationErrorRate | Taxa de erro > 5% por 5min | warning | Alta taxa de erros na validação |
| LowCPFCacheHitRate | Taxa de acerto < 70% por 15min | warning | Baixa eficiência do cache |
| HighCPFValidationLatency | P95 > 500ms por 10min | warning | Latência elevada nas validações |
| CPFCacheAlmostFull | Itens no cache > 900 por 5min | warning | Cache próximo da capacidade máxima |
| MetricsCollectionFailed | Endpoint inacessível por 1min | critical | Falha na coleta de métricas |

## Dashboard do Grafana

O dashboard "Monitoramento de Validação de CPF" está organizado nas seguintes seções:

1. **Visão Geral**
   - Taxa de acerto do cache
   - Total de validações
   - Taxa de erros
   - Tamanho do cache

2. **Desempenho**
   - Histórico de validações
   - Tempos de resposta (P50, P95, P99)

## Solução de Problemas Comuns

### Alta Taxa de Erros
1. Verifique os logs da aplicação para mensagens de erro detalhadas
2. Confira se o serviço de validação está acessível
3. Verifique a validade dos certificados (se aplicável)

### Baixo Desempenho
1. Aumente o tamanho do cache se a taxa de acerto estiver baixa
2. Verifique a carga do servidor de banco de dados
3. Considere escalar horizontalmente o serviço

### Alertas Falsos Positivos
1. Ajuste os limiares dos alertas conforme necessário
2. Verifique a configuração dos intervalos de avaliação

## Próximos Passos

- [ ] Configurar alertas adicionais conforme necessário
- [ ] Adicionar mais métricas de negócio
- [ ] Criar dashboards específicos por equipe
- [ ] Documentar procedimentos de escalação de incidentes

