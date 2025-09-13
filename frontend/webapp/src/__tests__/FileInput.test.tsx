import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import { FileInput } from '../components/ui';

describe('FileInput Component', () => {
  const mockRegister = {
    name: 'testFile',
    onChange: jest.fn(),
    onBlur: jest.fn(),
    ref: jest.fn(),
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renderiza corretamente com label e helperText', () => {
    render(
      <FileInput
        id="test-file"
        label="Arquivo de Teste"
        register={mockRegister}
        helperText="Apenas arquivos PDF"
      />
    );

    expect(screen.getByLabelText(/Arquivo de Teste/i)).toBeInTheDocument();
    expect(screen.getByText(/Apenas arquivos PDF/i)).toBeInTheDocument();
  });

  test('exibe mensagem de erro quando houver erro', () => {
    const errorMessage = 'Arquivo obrigatório';
    render(
      <FileInput
        id="test-file"
        label="Arquivo de Teste"
        register={mockRegister}
        error={{ message: errorMessage }}
      />
    );

    expect(screen.getByText(`Erro: ${errorMessage}`)).toBeInTheDocument();
  });

  test('permite seleção de arquivo e chama a função register.onChange', () => {
    const file = new File(['test'], 'test.pdf', { type: 'application/pdf' });
    
    render(
      <FileInput
        id="test-file"
        label="Selecionar Arquivo"
        register={mockRegister}
        accept="application/pdf"
      />
    );

    const input = screen.getByLabelText(/Selecionar Arquivo/i) as HTMLInputElement;
    fireEvent.change(input, { target: { files: [file] } });

    expect(mockRegister.onChange).toHaveBeenCalledTimes(1);
  });

  test('exibe preview quando fornecido', () => {
    const previewContent = <div data-testid="preview">Pré-visualização</div>;
    
    render(
      <FileInput
        id="test-file"
        label="Arquivo com Preview"
        register={mockRegister}
        preview={previewContent}
      />
    );

    expect(screen.getByTestId('preview')).toBeInTheDocument();
  });

  test('respeita a propriedade required', () => {
    render(
      <FileInput
        id="required-file"
        label="Arquivo Obrigatório"
        register={mockRegister}
        required={true}
      />
    );

    const input = screen.getByLabelText(/Arquivo Obrigatório/i);
    expect(input).toBeRequired();
  });

  test('respeita a propriedade disabled', () => {
    render(
      <FileInput
        id="disabled-file"
        label="Arquivo Desabilitado"
        register={mockRegister}
        disabled={true}
      />
    );

    const input = screen.getByLabelText(/Arquivo Desabilitado/i);
    expect(input).toBeDisabled();
  });
});

