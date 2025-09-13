import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { rest } from 'msw';
import { server } from '../../../../test-utils/mockApi';
import { CitizenRequestForm } from '../CitizenRequestForm';
import { mockCitizenRequest } from '../../../../test-utils/mockApi';

const mockOnSuccess = jest.fn();
const mockOnCancel = jest.fn();

describe('CitizenRequestForm', () => {
  beforeAll(() => server.listen());
  afterEach(() => {
    server.resetHandlers();
    jest.clearAllMocks();
  });
  afterAll(() => server.close());

  const renderForm = (initialData = {}) => {
    render(
      <MemoryRouter>
        <CitizenRequestForm
          initialData={initialData}
          onSuccess={mockOnSuccess}
          onCancel={mockOnCancel}
        />
      </MemoryRouter>
    );
  };

  it('renders the form with all fields', () => {
    renderForm();
    
    expect(screen.getByLabelText(/nome completo/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/nif/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/data de nascimento/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/gênero/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/rua/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/cidade/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/código postal/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/telefone/i)).toBeInTheDocument();
  });

  it('validates required fields', async () => {
    renderForm();
    
    fireEvent.click(screen.getByText(/submeter pedido/i));
    
    await waitFor(() => {
      expect(screen.getByText('Nome deve ter pelo menos 3 caracteres')).toBeInTheDocument();
      expect(screen.getByText('NIF deve ter 9 dígitos')).toBeInTheDocument();
      expect(screen.getByText('Data inválida')).toBeInTheDocument();
      expect(screen.getByText('Rua inválida')).toBeInTheDocument();
      expect(screen.getByText('Cidade inválida')).toBeInTheDocument();
      expect(screen.getByText('Código postal inválido')).toBeInTheDocument();
      expect(screen.getByText('Telefone inválido')).toBeInTheDocument();
    });
  });

  it('submits the form with valid data', async () => {
    renderForm();
    
    // Fill out the form
    fireEvent.change(screen.getByLabelText(/nome completo/i), { 
      target: { value: 'João Silva' } 
    });
    fireEvent.change(screen.getByLabelText(/nif/i), { 
      target: { value: '123456789' } 
    });
    fireEvent.change(screen.getByLabelText(/data de nascimento/i), { 
      target: { value: '1990-01-01' } 
    });
    fireEvent.change(screen.getByLabelText(/gênero/i), { 
      target: { value: 'M' } 
    });
    fireEvent.change(screen.getByLabelText(/rua/i), { 
      target: { value: 'Rua Exemplo' } 
    });
    fireEvent.change(screen.getByLabelText(/cidade/i), { 
      target: { value: 'Cidade' } 
    });
    fireEvent.change(screen.getByLabelText(/código postal/i), { 
      target: { value: '1234-567' } 
    });
    fireEvent.change(screen.getByLabelText(/email/i), { 
      target: { value: 'joao@example.com' } 
    });
    fireEvent.change(screen.getByLabelText(/telefone/i), { 
      target: { value: '912345678' } 
    });
    
    // Submit the form
    fireEvent.click(screen.getByText(/submeter pedido/i));
    
    // Check that the form was submitted successfully
    await waitFor(() => {
      expect(mockOnSuccess).toHaveBeenCalled();
    });
  });

  it('pre-fills the form when editing an existing request', () => {
    renderForm(mockCitizenRequest);
    
    expect(screen.getByLabelText(/nome completo/i)).toHaveValue(mockCitizenRequest.name);
    expect(screen.getByLabelText(/nif/i)).toHaveValue(mockCitizenRequest.nif);
    expect(screen.getByLabelText(/data de nascimento/i)).toHaveValue(mockCitizenRequest.birthDate);
    expect(screen.getByLabelText(/rua/i)).toHaveValue(mockCitizenRequest.address.street);
    expect(screen.getByLabelText(/cidade/i)).toHaveValue(mockCitizenRequest.address.city);
    expect(screen.getByLabelText(/código postal/i)).toHaveValue(mockCitizenRequest.address.postalCode);
    expect(screen.getByLabelText(/email/i)).toHaveValue(mockCitizenRequest.contact.email);
    expect(screen.getByLabelText(/telefone/i)).toHaveValue(mockCitizenRequest.contact.phone);
  });

  it('calls onCancel when the cancel button is clicked', () => {
    renderForm();
    fireEvent.click(screen.getByText(/cancelar/i));
    expect(mockOnCancel).toHaveBeenCalled();
  });

  it('shows an error message when form submission fails', async () => {
    // Mock a failed API response
    server.use(
      rest.post('http://localhost:8000/api/v1/citizenship/requests/', (req, res, ctx) => {
        return res(ctx.status(500), ctx.json({ message: 'Internal Server Error' }));
      })
    );

    renderForm();
    
    // Fill out required fields with minimal valid data
    fireEvent.change(screen.getByLabelText(/nome completo/i), { 
      target: { value: 'João Silva' } 
    });
    fireEvent.change(screen.getByLabelText(/nif/i), { 
      target: { value: '123456789' } 
    });
    fireEvent.change(screen.getByLabelText(/data de nascimento/i), { 
      target: { value: '1990-01-01' } 
    });
    fireEvent.change(screen.getByLabelText(/gênero/i), { 
      target: { value: 'M' } 
    });
    fireEvent.change(screen.getByLabelText(/rua/i), { 
      target: { value: 'Rua Exemplo' } 
    });
    fireEvent.change(screen.getByLabelText(/cidade/i), { 
      target: { value: 'Cidade' } 
    });
    fireEvent.change(screen.getByLabelText(/código postal/i), { 
      target: { value: '1234-567' } 
    });
    fireEvent.change(screen.getByLabelText(/telefone/i), { 
      target: { value: '912345678' } 
    });
    
    // Submit the form
    fireEvent.click(screen.getByText(/submeter pedido/i));
    
    // Check that the error message is displayed
    await waitFor(() => {
      expect(screen.getByText(/ocorreu um erro ao processar o pedido/i)).toBeInTheDocument();
    });
  });
});

