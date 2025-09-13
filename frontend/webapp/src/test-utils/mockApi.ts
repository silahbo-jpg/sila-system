import { rest } from 'msw';
import { setupServer } from 'msw/node';

// Mock data
const mockCitizenRequest = {
  id: '1',
  name: 'João Silva',
  nif: '123456789',
  birthDate: '1990-01-01',
  gender: 'M',
  status: 'draft',
  address: {
    street: 'Rua Exemplo',
    city: 'Cidade',
    postalCode: '1234-567',
  },
  contact: {
    email: 'joao@example.com',
    phone: '912345678',
  },
  createdAt: '2025-07-26T10:00:00Z',
};

const mockRequestsList = {
  count: 2,
  next: null,
  previous: null,
  results: [
    mockCitizenRequest,
    {
      ...mockCitizenRequest,
      id: '2',
      name: 'Maria Santos',
      nif: '987654321',
      status: 'submitted',
    },
  ],
};

// Setup request handlers
const handlers = [
  // List requests
  rest.get('http://localhost:8000/api/v1/citizenship/requests/', (req, res, ctx) => {
    return res(ctx.json(mockRequestsList));
  }),
  
  // Get single request
  rest.get('http://localhost:8000/api/v1/citizenship/requests/:id', (req, res, ctx) => {
    return res(ctx.json(mockCitizenRequest));
  }),
  
  // Create request
  rest.post('http://localhost:8000/api/v1/citizenship/requests/', (req, res, ctx) => {
    return res(ctx.json({
      ...mockCitizenRequest,
      ...(req.body as object),
      id: 'new-request-id',
    }));
  }),
  
  // Update request
  rest.patch('http://localhost:8000/api/v1/citizenship/requests/:id', (req, res, ctx) => {
    return res(ctx.json({
      ...mockCitizenRequest,
      ...(req.body as object),
    }));
  }),
  
  // Submit request
  rest.post('http://localhost:8000/api/v1/citizenship/requests/:id/submit/', (req, res, ctx) => {
    return res(ctx.json({
      ...mockCitizenRequest,
      status: 'submitted',
    }));
  }),
  
  // Delete request
  rest.delete('http://localhost:8000/api/v1/citizenship/requests/:id', (req, res, ctx) => {
    return res(ctx.status(204));
  }),
];

// Create server with the request handlers
export const server = setupServer(...handlers);

// Export mock data for use in tests
export { mockCitizenRequest, mockRequestsList };

