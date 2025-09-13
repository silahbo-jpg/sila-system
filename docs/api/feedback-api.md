# API de Feedback

A API de Feedback permite que os usuários enviem sugestões, relatem problemas, tirem dúvidas ou enviem elogios sobre o sistema. Os administradores podem gerenciar esses feedbacks, atualizando seus status e fornecendo respostas.

## Visão Geral

- **URL Base**: `/api/citizenship/feedback`
- **Autenticação**: Necessária para todas as rotas, exceto envio anônimo (configurável)
- **Formato**: JSON

## Modelo de Dados

### Feedback

| Campo          | Tipo     | Obrigatório | Descrição                                                                 |
|----------------|----------|-------------|---------------------------------------------------------------------------|
| id             | UUID     | Não         | Identificador único do feedback (gerado automaticamente)                 |
| tipo           | String   | Sim         | Tipo do feedback (sugestao, problema, duvida, elogio, outro)             |
| titulo         | String   | Sim         | Título descritivo do feedback (máx. 200 caracteres)                      |
| descricao      | String   | Sim         | Descrição detalhada do feedback                                           |
| classificacao | Integer  | Não         | Classificação de 1 a 5 estrelas (opcional)                               |
| status        | String   | Não         | Status atual do feedback (pendente, em_analise, resolvido, arquivado)    |
| resposta      | String   | Não         | Resposta da equipe ao feedback                                            |
| usuario_id    | UUID     | Não         | ID do usuário que enviou o feedback (nulo para anônimos)                 |
| cidadao_id    | UUID     | Não         | ID do cidadão relacionado ao feedback (opcional)                         |
| ip_address    | String   | Não         | Endereço IP do remetente (preenchido automaticamente)                    |
| user_agent    | String   | Não         | User-Agent do navegador (preenchido automaticamente)                     |
| criado_em     | DateTime | Não         | Data e hora de criação (preenchido automaticamente)                      |
| atualizado_em | DateTime | Não         | Data e hora da última atualização (preenchido automaticamente)           |

## Endpoints

### 1. Enviar Feedback

Envia um novo feedback para o sistema. Pode ser feito de forma anônima ou autenticada.

- **Método**: `POST /api/citizenship/feedback/`
- **Autenticação**: Opcional
- **Permissões**: Nenhuma

**Exemplo de Requisição**:

```http
POST /api/citizenship/feedback/
Content-Type: application/json
Authorization: Bearer <token>

{
  "tipo": "sugestao",
  "titulo": "Melhoria na interface",
  "descricao": "Sugiro adicionar um campo de busca avançada na lista de cidadãos.",
  "classificacao": 4,
  "cidadao_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Respostas**:

- `201 Created`: Feedback criado com sucesso
  ```json
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "tipo": "sugestao",
    "titulo": "Melhoria na interface",
    "descricao": "Sugiro adicionar um campo de busca avançada na lista de cidadãos.",
    "classificacao": 4,
    "status": "pendente",
    "resposta": null,
    "usuario_id": "550e8400-e29b-41d4-a716-446655440000",
    "cidadao_id": "550e8400-e29b-41d4-a716-446655440000",
    "criado_em": "2023-06-15T10:30:00Z",
    "atualizado_em": "2023-06-15T10:30:00Z"
  }
  ```

- `400 Bad Request`: Dados inválidos fornecidos
- `401 Unauthorized`: Token inválido ou expirado (se autenticação for necessária)

### 2. Listar Feedbacks (Admin)

Lista os feedbacks com filtros e paginação. Apenas para administradores.

- **Método**: `GET /api/citizenship/feedback/`
- **Autenticação**: Obrigatória
- **Permissões**: `is_superuser = True`

**Parâmetros de Consulta**:

| Parâmetro  | Tipo    | Obrigatório | Descrição                                           |
|------------|---------|-------------|---------------------------------------------------|
| status     | String  | Não         | Filtrar por status (pendente, em_analise, etc.)   |
| tipo       | String  | Não         | Filtrar por tipo (sugestao, problema, etc.)       |
| cidadao_id | UUID    | Não         | Filtrar por ID do cidadão relacionado             |
| skip       | Integer | Não         | Número de registros para pular (padrão: 0)        |
| limit      | Integer | Não         | Número máximo de registros por página (padrão: 100) |

**Exemplo de Requisição**:

```http
GET /api/citizenship/feedback/?status=pendente&limit=10&skip=0
Authorization: Bearer <admin_token>
```

**Respostas**:

- `200 OK`: Lista de feedbacks
  ```json
  {
    "items": [
      {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "tipo": "sugestao",
        "titulo": "Melhoria na interface",
        "status": "pendente",
        "criado_em": "2023-06-15T10:30:00Z",
        "usuario_id": "550e8400-e29b-41d4-a716-446655440000"
      }
    ],
    "total": 1,
    "page": 1,
    "pages": 1,
    "per_page": 10,
    "has_next": false,
    "has_prev": false
  }
  ```

### 3. Obter Feedback por ID

Obtém os detalhes de um feedback específico.

- **Método**: `GET /api/citizenship/feedback/{feedback_id}`
- **Autenticação**: Obrigatória
- **Permissões**: Proprietário do feedback ou Admin

**Exemplo de Requisição**:

```http
GET /api/citizenship/feedback/123e4567-e89b-12d3-a456-426614174000
Authorization: Bearer <token>
```

**Respostas**:

- `200 OK`: Detalhes do feedback
  ```json
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "tipo": "sugestao",
    "titulo": "Melhoria na interface",
    "descricao": "Sugiro adicionar um campo de busca avançada na lista de cidadãos.",
    "classificacao": 4,
    "status": "pendente",
    "resposta": null,
    "usuario_id": "550e8400-e29b-41d4-a716-446655440000",
    "cidadao_id": "550e8400-e29b-41d4-a716-446655440000",
    "criado_em": "2023-06-15T10:30:00Z",
    "atualizado_em": "2023-06-15T10:30:00Z"
  }
  ```

- `403 Forbidden`: Acesso negado (não é o proprietário nem admin)
- `404 Not Found`: Feedback não encontrado

### 4. Atualizar Feedback (Admin)

Atualiza o status ou a resposta de um feedback. Apenas para administradores.

- **Método**: `PATCH /api/citizenship/feedback/{feedback_id}`
- **Autenticação**: Obrigatória
- **Permissões**: `is_superuser = True`

**Exemplo de Requisição**:

```http
PATCH /api/citizenship/feedback/123e4567-e89b-12d3-a456-426614174000
Content-Type: application/json
Authorization: Bearer <admin_token>

{
  "status": "resolvido",
  "resposta": "Obrigado pela sugestão! Implementaremos na próxima atualização."
}
```

**Respostas**:

- `200 OK`: Feedback atualizado
  ```json
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "status": "resolvido",
    "resposta": "Obrigado pela sugestão! Implementaremos na próxima atualização.",
    "atualizado_em": "2023-06-15T11:45:00Z"
  }
  ```

- `400 Bad Request`: Dados inválidos fornecidos
- `403 Forbidden`: Acesso negado (não é admin)
- `404 Not Found`: Feedback não encontrado

### 5. Excluir Feedback (Admin)

Remove permanentemente um feedback do sistema. Apenas para administradores.

- **Método**: `DELETE /api/citizenship/feedback/{feedback_id}`
- **Autenticação**: Obrigatória
- **Permissões**: `is_superuser = True`

**Exemplo de Requisição**:

```http
DELETE /api/citizenship/feedback/123e4567-e89b-12d3-a456-426614174000
Authorization: Bearer <admin_token>
```

**Respostas**:

- `204 No Content`: Feedback excluído com sucesso
- `403 Forbidden`: Acesso negado (não é admin)
- `404 Not Found`: Feedback não encontrado

## Exemplos de Uso

### Enviando um feedback anônimo

```http
POST /api/citizenship/feedback/
Content-Type: application/json

{
  "tipo": "problema",
  "titulo": "Erro ao salvar formulário",
  "descricao": "Ao tentar salvar o formulário de cadastro, recebo um erro 500.",
  "classificacao": 2
}
```

### Atualizando o status de um feedback (admin)

```http
PATCH /api/citizenship/feedback/123e4567-e89b-12d3-a456-426614174000
Content-Type: application/json
Authorization: Bearer <admin_token>

{
  "status": "em_analise",
  "resposta": "Estamos analisando o problema relatado."
}
```

### Filtrando feedbacks (admin)

```http
GET /api/citizenship/feedback/?tipo=problema&status=pendente&limit=5&skip=0
Authorization: Bearer <admin_token>
```

## Considerações de Segurança

1. **Dados Pessoais**: Endereços IP e User-Agents são registrados para fins de auditoria, mas não são expostos nas respostas da API.
2. **Acesso a Dados**: Apenas administradores podem visualizar todos os feedbacks. Usuários comuns só veem seus próprios feedbacks.
3. **Validação**: Todos os dados de entrada são validados quanto a tipo, formato e obrigatoriedade.
4. **Rate Limiting**: Recomenda-se implementar limitação de taxa para evitar abuso do endpoint de envio de feedback.

## Melhorias Futuras

1. **Notificações por E-mail**: Enviar notificações quando um feedback for respondido.
2. **Categorização**: Adicionar categorias mais específicas para os feedbacks.
3. **Anexos**: Permitir o envio de imagens ou documentos junto com o feedback.
4. **Pesquisa de Satisfação**: Adicionar pesquisa de satisfação periódica para os usuários.

