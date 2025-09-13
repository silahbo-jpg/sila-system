import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { act } from 'react-dom/test-utils';
import RegistroMunicipe from '../pages/RegistroMunicipe';
import { api } from '../api/axios';

// Mock do axios
jest.mock('../api/axios');
const mockedApi = api as jest.Mocked<typeof api>;

// Mock do FileReader
class MockFileReader {
  readAsDataURL = jest.fn();
  result = '';
  onload: ((this: FileReader, ev: ProgressEvent<FileReader>) => any) | null = null;
  onerror: ((this: FileReader, ev: ProgressEvent<FileReader>) => any) | null = null;
  
  constructor() {
    this.onload = jest.fn();
    this.onerror = jest.fn();
  }
}

global.FileReader = MockFileReader as any;

describe('RegistroMunicipe Form', () => {
  // Dados de teste
  const mockFile = new File(['test'], 'test.png', { type: 'image/png' });
  const mockPdf = new File(['test'], 'test.pdf', { type: 'application/pdf' });
  
  // Mock da resposta da API
  const mockApiResponse = {
    data: { success: true },
    status: 200,
  };

  beforeEach(() => {
    // Limpar mocks antes de cada teste
    jest.clearAllMocks();
    
    // Configurar o mock da API
    mockedApi.post.mockResolvedValue(mockApiResponse);
    
    // Mock do URL.createObjectURL para o preview de imagem
    global.URL.createObjectURL = jest.fn(() => 'mock-url');
  });

  test('renderiza o formulário corretamente', () => {
    render(
  <MemoryRouter>
    <RegistroMunicipe />
  </MemoryRouter>
);
    
    // Verifica se os campos obrigatórios estão presentes
    expect(screen.getByLabelText(/Nome Completo/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Número do BI/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Foto do Rosto/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Anexo do BI/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Registrar/i })).toBeInTheDocument();
  });

  test('exibe erros de validação quando o formulário é enviado vazio', async () => {
    render(
  <MemoryRouter>
    <RegistroMunicipe />
  </MemoryRouter>
);
    
    // Submeter o formulário vazio
    fireEvent.click(screen.getByRole('button', { name: /Registrar/i }));
    
    // Verificar mensagens de erro
    await waitFor(() => {
      expect(screen.getByText(/O nome deve ter pelo menos 3 caracteres/i)).toBeInTheDocument();
      expect(screen.getByText(/Formato de BI inválido/i)).toBeInTheDocument();
    });
    
    // Verificar se a API não foi chamada
    expect(mockedApi.post).not.toHaveBeenCalled();
  });

  test('envia o formulário com sucesso quando preenchido corretamente', async () => {
    render(
  <MemoryRouter>
    <RegistroMunicipe />
  </MemoryRouter>
);
    
    // Preencher campos do formulário
    fireEvent.change(screen.getByLabelText(/Nome Completo/i), {
      target: { value: 'João da Silva' },
    });
    
    fireEvent.change(screen.getByLabelText(/Número do BI/i), {
      target: { value: '123456789LA042' },
    });
    
    // Simular upload de arquivos
    const fotoInput = screen.getByLabelText(/Foto do Rosto/i) as HTMLInputElement;
    const biAnexoInput = screen.getByLabelText(/Anexo do BI/i) as HTMLInputElement;
    
    await act(async () => {
      fireEvent.change(fotoInput, {
        target: { files: [mockFile] },
      });
      
      fireEvent.change(biAnexoInput, {
        target: { files: [mockPdf] },
      });
    });
    
    // Simular leitura do arquivo (FileReader)
    await act(async () => {
      const fileReaderInstance = (FileReader as any).mock.instances[0];
      fileReaderInstance.onload({ target: { result: 'data:image/png;base64,mock' } });
    });
    
    // Submeter o formulário
    await act(async () => {
      fireEvent.click(screen.getByRole('button', { name: /Registrar/i }));
    });
    
    // Verificar se a API foi chamada com os dados corretos
    await waitFor(() => {
      expect(mockedApi.post).toHaveBeenCalledWith(
        '/municipe',
        expect.any(FormData),
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );
    });
    
    // Verificar se o formulário foi resetado após o envio
    expect(screen.getByLabelText(/Nome Completo/i)).toHaveValue('');
  });

  test('exibe mensagem de erro quando o envio falha', async () => {
    // Configurar o mock para rejeitar a requisição
    mockedApi.post.mockRejectedValueOnce(new Error('Erro na API'));
    
    // Mock do console.error para evitar erros no console durante o teste
    const originalError = console.error;
    console.error = jest.fn();
    
    render(
  <MemoryRouter>
    <RegistroMunicipe />
  </MemoryRouter>
);
    
    // Preencher campos obrigatórios
    fireEvent.change(screen.getByLabelText(/Nome Completo/i), {
      target: { value: 'João da Silva' },
    });
    
    fireEvent.change(screen.getByLabelText(/Número do BI/i), {
      target: { value: '123456789LA042' },
    });
    
    // Submeter o formulário
    await act(async () => {
      fireEvent.click(screen.getByRole('button', { name: /Registrar/i }));
    });
    
    // Verificar se a mensagem de erro é exibida
    await waitFor(() => {
      expect(screen.getByText(/Ocorreu um erro ao registrar o munícipe/i)).toBeInTheDocument();
    });
    
    // Restaurar console.error
    console.error = originalError;
  });

  test('formata o número do BI enquanto o usuário digita', async () => {
    render(
  <MemoryRouter>
    <RegistroMunicipe />
  </MemoryRouter>
);
    
    const biInput = screen.getByLabelText(/Número do BI/i) as HTMLInputElement;
    
    // Simular digitação
    fireEvent.change(biInput, { target: { value: '123456789' } });
    expect(biInput.value).toBe('123456789');
    
    // Continuar digitando para completar o formato do BI
    fireEvent.change(biInput, { target: { value: '123456789LA' } });
    expect(biInput.value).toBe('123456789LA');
    
    // Completar o formato do BI
    fireEvent.change(biInput, { target: { value: '123456789LA042' } });
    expect(biInput.value).toBe('123456789LA042');
  });
});

