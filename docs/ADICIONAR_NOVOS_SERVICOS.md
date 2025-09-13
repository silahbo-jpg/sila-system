# Guia para Adicionar Novos Serviços ao SILA

## Introdução

Este documento descreve o processo para adicionar novos serviços ao Sistema Integrado Local de Administração (SILA), utilizando a nova arquitetura baseada em serviços.

## Visão Geral

O SILA agora utiliza uma arquitetura baseada em serviços, onde cada módulo pode registrar seus serviços no `service_hub`. Isso permite:

1. Centralização do catálogo de serviços
2. Padronização da interface de serviços
3. Descoberta automática de serviços
4. Integração simplificada entre módulos

## Pré-requisitos

- Entendimento básico da estrutura de módulos do SILA
- Conhecimento de Python e FastAPI
- Acesso ao código-fonte do SILA

## Processo para Adicionar um Novo Serviço

### 1. Usando o Decorator `@register_service`

A maneira mais simples de adicionar um novo serviço é usando o decorator `@register_service` em uma função handler:

```python
from app.modules.service_hub.services import register_service

@register_service(
    slug="nome-do-servico",  # Identificador único do serviço
    nome="Nome do Serviço",  # Nome amigável do serviço
    descricao="Descrição detalhada do serviço",
    departamento="nome_do_modulo",  # Módulo responsável pelo serviço
    categoria="categoria_do_servico",  # Categoria para agrupamento
    sla_horas=24,  # Tempo estimado para conclusão do serviço
    requer_autenticacao=True,  # Se requer autenticação do usuário
    requer_documentos=["doc1", "doc2"],  # Documentos necessários
    dependencias=["outro-servico"],  # Serviços que este depende
    eventos=["evento1", "evento2"]  # Eventos que este serviço pode emitir
)
def handler_do_servico(data: Dict[str, Any]):
    # Implementação do serviço
    return {"status": "success", "message": "Serviço executado com sucesso"}
```

### 2. Criando um Novo Módulo para o Serviço

Se o serviço requer um novo módulo, você pode usar o script `add_new_service.py`:

```bash
python scripts/add_new_service.py NomeDoModulo --title "Título do Módulo" --description "Descrição do módulo"
```

Este script criará a estrutura básica do módulo com todos os arquivos necessários.

### 3. Gerando Serviços Específicos em Módulos Existentes

Para adicionar um novo serviço a um módulo existente, você pode usar o script `generate_service.py`:

```bash
python scripts/generate_service.py nome_do_modulo NomeDoServico
```

Por exemplo:

```bash
python scripts/generate_service.py health AgendamentoTeleconsulta
```

Este script irá:
- Criar os arquivos models, schemas e routes para o serviço
- Registrar o serviço no service_hub usando o decorator
- Adicionar as rotas necessárias no módulo

### 4. Gerando Múltiplos Serviços em Lote

Para gerar vários serviços de uma vez, você pode usar o script `batch_generate_services.py`:

```bash
# Usar a lista padrão de serviços
python scripts/batch_generate_services.py --default

# Usar um arquivo CSV personalizado
python scripts/batch_generate_services.py --csv caminho/para/servicos.csv

# Criar um arquivo CSV de exemplo
python scripts/batch_generate_services.py --create-csv caminho/para/novo.csv
```

O sistema já inclui um catálogo de serviços em `scripts/service_catalog.csv` com mais de 100 serviços pré-definidos que podem ser gerados.

### 5. Implementando a Lógica do Serviço

Após registrar o serviço, implemente a lógica de negócio no handler:

1. Valide os dados de entrada
2. Execute a lógica de negócio
3. Retorne o resultado apropriado

### 6. Testando o Serviço

Para testar o serviço:

1. Inicie o servidor SILA
2. Acesse o endpoint `/service_hub/all` para verificar se o serviço está registrado
3. Teste o serviço através da interface apropriada

## Exemplos

### Exemplo 1: Serviço de Emissão de Certidão

```python
from app.modules.service_hub.services import register_service

@register_service(
    slug="emitir-certidao",
    nome="Emissão de Certidão",
    descricao="Serviço para emissão de certidões",
    departamento="citizenship",
    categoria="documentos",
    sla_horas=72
)
async def emitir_certidao_handler(data: Dict[str, Any]):
    tipo_certidao = data.get("tipo_certidao")
    # Lógica para emissão de certidão
    return {"status": "success", "message": f"Certidão de {tipo_certidao} solicitada com sucesso"}
```

### Exemplo 2: Serviço de Agendamento de Consulta

```python
from app.modules.service_hub.services import register_service

@register_service(
    slug="consulta-medica",
    nome="Agendamento de Consulta Médica",
    descricao="Serviço para agendamento de consultas médicas",
    departamento="health",
    categoria="atendimento",
    sla_horas=24
)
async def agendar_consulta_handler(data: Dict[str, Any]):
    # Implementação do serviço
    return {"status": "success", "message": "Consulta agendada com sucesso"}
```

## Melhores Práticas

1. **Nomes de Serviços**: Use slugs descritivos e únicos para identificar serviços
2. **Documentação**: Forneça descrições claras e detalhadas dos serviços
3. **Validação**: Valide todos os dados de entrada antes de processar
4. **Tratamento de Erros**: Implemente tratamento adequado de erros e exceções
5. **Dependências**: Declare explicitamente as dependências entre serviços
6. **Testes**: Crie testes automatizados para seus serviços

## Solução de Problemas

### Serviço não aparece no catálogo

- Verifique se o módulo que contém o serviço está sendo importado corretamente
- Certifique-se de que o decorator `@register_service` está sendo aplicado corretamente
- Verifique se o servidor foi reiniciado após adicionar o serviço

### Erros ao chamar o serviço

- Verifique os logs do servidor para mensagens de erro detalhadas
- Certifique-se de que todos os parâmetros necessários estão sendo fornecidos
- Verifique se as dependências do serviço estão disponíveis

## Conclusão

A nova arquitetura baseada em serviços do SILA facilita a adição e integração de novos serviços. Seguindo este guia, você poderá adicionar novos serviços de forma padronizada e eficiente.
