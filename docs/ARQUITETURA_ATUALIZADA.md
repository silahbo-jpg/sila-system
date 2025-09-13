# Arquitetura Atualizada do Sistema SILA

## Visão Geral

O Sistema Integrado de Licenciamento e Atendimento (SILA) foi reestruturado para adotar uma arquitetura modular, escalável e institucionalmente robusta. Esta documentação descreve a nova estrutura do sistema após a implementação dos cinco pilares estratégicos.

## Pilares Estratégicos

### 1. Módulo Registry (Cadastro Único)

**Função Estratégica**: Centralização do cadastro de munícipes, servindo como fonte única de verdade para informações dos cidadãos.

**Componentes Principais**:
- `models/citizen.py`: Modelo de dados para cadastro de cidadãos
- Serviços de validação e deduplicação de registros
- APIs para consulta e atualização de dados cadastrais

### 2. Módulo Governance (Governança)

**Função Estratégica**: Gestão institucional, auditoria e compliance do sistema.

**Componentes Principais**:
- `models/audit_log.py`: Registro de todas as operações críticas do sistema
- Sistema de permissões e controle de acesso
- Relatórios de governança e compliance

### 3. Módulo Finance (Finanças)

**Função Estratégica**: Gestão de receitas públicas e integração bancária.

**Componentes Principais**:
- `models/payment.py`: Registro de pagamentos de taxas e serviços
- `models/transaction.py`: Transações financeiras com instituições bancárias
- `services/payment.py`: Serviços para processamento de pagamentos

### 4. Módulo Integration (Integração)

**Função Estratégica**: Hub de APIs externas e conectividade com sistemas parceiros.

**Componentes Principais**:
- `adapters/bna_adapter.py`: Adaptador para integração com o Banco Nacional de Angola
- Conectores para sistemas governamentais
- Serviços de transformação e normalização de dados

### 5. Módulo Health (Saúde)

**Função Estratégica**: Gestão de saúde municipal (padronizado após mesclagem).

**Componentes Principais**:
- Gestão de unidades de saúde
- Agendamento de consultas
- Registro de atendimentos

## Diagrama de Arquitetura Modular

```
+-------------------+       +-------------------+       +-------------------+
|                   |       |                   |       |                   |
|     Frontend      |------>|     Backend       |------>|     Databases     |
|                   |       |                   |       |                   |
+-------------------+       +-------------------+       +-------------------+
         |                           |
         |                           |
         v                           v
+-------------------+       +-------------------+
|                   |       |                   |
|  External APIs    |<----->|  Integration Hub  |
|                   |       |                   |
+-------------------+       +-------------------+
```

## Fluxo de Dados Entre Módulos

### Fluxo de Registro e Pagamento

1. O cidadão é registrado no módulo **Registry**
2. Seus dados são utilizados para serviços no módulo **Health**
3. Pagamentos de taxas são processados pelo módulo **Finance**
4. Transações bancárias são realizadas via módulo **Integration**
5. Todas as operações são auditadas pelo módulo **Governance**

## Estratégia de Integração

### Integração com BNA (Banco Nacional de Angola)

A integração com o BNA é realizada através do adaptador `bna_adapter.py` no módulo Integration, que oferece:

- Consulta de taxas de câmbio
- Validação de contas bancárias
- Processamento de transações interbancárias

### Integração com SIMPLIFICA 2.0

A integração com o sistema SIMPLIFICA 2.0 permitirá:

- Sincronização de cadastros de cidadãos
- Compartilhamento de informações sobre licenciamentos
- Validação cruzada de documentos

## Padronização de Módulos

Todos os módulos seguem uma estrutura padronizada:

```
modulo/
  ├── models/
  │   └── __init__.py
  ├── routes/
  │   └── __init__.py
  ├── services/
  │   └── __init__.py
  ├── tests/
  │   └── __init__.py
  ├── schemas/
  │   └── __init__.py
  ├── utils/
  │   └── __init__.py
  ├── __init__.py
  └── README.md
```

## Próximos Passos

1. **Desenvolvimento de Conteúdo Inicial**:
   - Implementação de modelos e serviços básicos para cada módulo
   - Criação de APIs RESTful para acesso aos recursos

2. **Integração Frontend**:
   - Desenvolvimento de interfaces para os novos módulos
   - Implementação de fluxos de trabalho integrados

3. **Testes e Validação**:
   - Criação de testes unitários e de integração
   - Validação de fluxos de dados entre módulos

4. **Documentação Detalhada**:
   - Documentação técnica de APIs
   - Manuais de usuário para novos módulos

## Conclusão

A nova arquitetura modular do SILA proporciona maior escalabilidade, manutenibilidade e robustez ao sistema. A clara separação de responsabilidades entre os módulos facilita o desenvolvimento paralelo e a evolução independente de cada componente, garantindo que o sistema possa crescer de forma sustentável para atender às necessidades futuras da administração municipal.
