# Módulo de Cidadania

Este módulo é responsável por gerenciar os pedidos de cidadania no sistema SILA.

## Estrutura do Módulo

```
citizenship/
├── api/                    # Chamadas de API
│   └── citizenshipApi.ts   # Funções de API para cidadania
├── components/             # Componentes reutilizáveis
│   └── CitizenRequestForm.tsx  # Formulário de pedido
├── pages/                  # Páginas do módulo
│   └── CitizenRequestsPage.tsx # Lista e gerencia pedidos
└── types/                  # Tipos TypeScript
    └── index.ts            # Exportação de tipos
```

## Funcionalidades

- Criação de novos pedidos de cidadania
- Visualização e edição de pedidos existentes
- Submissão de documentos
- Acompanhamento do status do pedido
- Aprovação/Reprovação de pedidos (para administradores)

## Como Usar

### Importando o módulo

```tsx
import { CitizenRequestsPage } from './features/citizenship/pages/CitizenRequestsPage';
```

### Rotas

Adicione a rota no seu arquivo de rotas principal:

```tsx
{
  path: '/cidadania/pedidos',
  element: <CitizenRequestsPage />,
}
```

## Configuração

Certifique-se de que as seguintes variáveis de ambiente estejam configuradas:

```env
VITE_API_BASE_URL=http://localhost:8000
```

## Testes

Para executar os testes deste módulo:

```bash
npm test src/features/citizenship/**/*.test.{ts,tsx}
```

## Dependências

- `react-hook-form` - Gerenciamento de formulários
- `zod` - Validação de dados
- `@hookform/resolvers` - Integração do Zod com React Hook Form
- `axios` - Requisições HTTP

## Padrões de Código

- Use TypeScript para tipagem forte
- Siga o padrão de pastas por funcionalidade
- Componentes devem ser funcionais e sem estado sempre que possível
- Use hooks personalizados para lógica reutilizável

