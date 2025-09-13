# Guia do Gateway de Integração

## Introdução

O Gateway de Integração é um componente central do SILA que permite a comunicação entre diferentes módulos do sistema através de eventos. Ele implementa o padrão de comunicação baseado em eventos (Event-Driven Architecture), permitindo que os módulos publiquem eventos e se inscrevam para receber notificações de eventos específicos.

## Conceitos Básicos

### Eventos

Um evento representa algo que aconteceu no sistema. Cada evento tem:

- **Tipo**: Identificador do evento (ex: `document.issued`, `address.changed`)
- **Payload**: Dados associados ao evento
- **Módulo de origem**: Módulo que gerou o evento
- **Timestamp**: Data e hora em que o evento foi gerado

### Publicação (Publish)

Quando um módulo realiza uma ação significativa, ele pode publicar um evento para notificar outros módulos interessados.

### Assinatura (Subscribe)

Módulos podem se inscrever para receber notificações quando eventos específicos ocorrerem.

## Como Usar

### Importando o Gateway

```python
from app.modules.integration.integration_gateway import integration_gateway
```

### Publicando Eventos

```python
await integration_gateway.publish(
    event_type="document.issued",
    payload={
        "document_id": "DOC123456",
        "citizen_id": "CIT789012",
        "document_type": "ID_CARD",
        "issue_date": "2023-07-20T14:30:00",
    },
    source_module="documents"
)
```

### Assinando Eventos

```python
async def handle_document_issued(event, payload):
    """Handler para eventos de documento emitido."""
    citizen_id = payload.get("citizen_id")
    document_type = payload.get("document_type")
    print(f"Documento {document_type} emitido para o cidadão {citizen_id}")

# Registrar o handler
integration_gateway.subscribe(
    module="my_module",
    event_type="document.issued",
    callback=handle_document_issued
)
```

### Cancelando Assinaturas

```python
integration_gateway.unsubscribe(
    module="my_module",
    event_type="document.issued",
    callback=handle_document_issued
)
```

### Usando Wildcards

Você pode usar o caractere `*` como wildcard para assinar todos os eventos de um tipo específico:

```python
# Assinar todos os eventos relacionados a documentos
integration_gateway.subscribe(
    module="my_module",
    event_type="document.*",
    callback=handle_document_events
)

# Assinar todos os eventos do sistema
integration_gateway.subscribe(
    module="logging_module",
    event_type="*",
    callback=log_all_events
)
```

## Boas Práticas

### Nomenclatura de Eventos

Use a convenção `domínio.ação` para nomear eventos:

- `document.issued`: Um documento foi emitido
- `address.changed`: Um endereço foi alterado
- `citizen.registered`: Um cidadão foi registrado

### Estrutura do Payload

- Mantenha o payload simples e focado nos dados relevantes para o evento
- Inclua IDs para permitir que os handlers busquem mais informações se necessário
- Use tipos de dados serializáveis (strings, números, booleanos, listas, dicionários)
- Evite incluir objetos complexos ou referências a objetos do banco de dados

### Tratamento de Erros

- Os handlers devem capturar e tratar suas próprias exceções para evitar que afetem outros handlers
- O gateway não propaga exceções dos handlers para o publicador do evento
- Use logging para registrar erros nos handlers

```python
async def handle_event(event, payload):
    try:
        # Processar o evento
        process_event(event, payload)
    except Exception as e:
        logger.error(f"Erro ao processar evento {event.event_type}: {str(e)}")
```

### Desempenho

- Mantenha os handlers leves e rápidos
- Para processamento pesado, considere usar tarefas em segundo plano
- Evite operações bloqueantes nos handlers

## Endpoints da API

O gateway de integração expõe os seguintes endpoints REST:

- `GET /api/integration/events`: Listar eventos com filtros opcionais
- `GET /api/integration/events/{event_id}`: Obter um evento específico
- `POST /api/integration/events`: Criar um novo evento
- `GET /api/integration/events/module/{module_name}`: Listar eventos de um módulo específico
- `GET /api/integration/events/type/{event_type}`: Listar eventos de um tipo específico

## Exemplo Completo

Veja um exemplo completo em `backend/app/modules/integration/examples/integration_example.py`.

## Solução de Problemas

### Evento não está sendo recebido

1. Verifique se o handler está registrado corretamente
2. Verifique se o tipo de evento está correto (incluindo maiúsculas/minúsculas)
3. Verifique se o módulo está registrado corretamente
4. Verifique se não há exceções no handler

### Erro ao publicar evento

1. Verifique se o payload contém apenas tipos serializáveis
2. Verifique se o tipo de evento e o módulo de origem estão definidos corretamente

## Referência da API

### IntegrationGateway

#### `publish(event_type, payload, source_module)`

Publica um evento no gateway.

- `event_type`: Tipo do evento (string)
- `payload`: Dados do evento (dict)
- `source_module`: Módulo que está publicando o evento (string)

#### `subscribe(module, event_type, callback)`

Registra um handler para receber eventos.

- `module`: Nome do módulo que está se inscrevendo (string)
- `event_type`: Tipo de evento a ser recebido (string, pode incluir wildcards)
- `callback`: Função assíncrona que será chamada quando o evento ocorrer

#### `unsubscribe(module, event_type, callback)`

Cancela o registro de um handler.

- `module`: Nome do módulo que está cancelando a inscrição (string)
- `event_type`: Tipo de evento (string)
- `callback`: Função handler a ser removida

#### `get_event_history()`

Retorna o histórico de eventos publicados.

- Retorna: Lista de objetos `IntegrationEvent`
