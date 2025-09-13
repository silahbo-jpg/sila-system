import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import { Input } from '../components/ui';

describe('Input Component', () => {
  const mockRegister = {
    name: 'testInput',
    onChange: jest.fn(),
    onBlur: jest.fn(),
    ref: jest.fn(),
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renderiza corretamente com props padrão', () => {
    render(
      <Input
        id="test-input"
        label="Nome Completo"
        register={mockRegister}
      />
    );

    const input = screen.getByLabelText(/nome completo/i);
    expect(input).toBeInTheDocument();
    expect(input).toHaveAttribute('type', 'text');
    expect(input).not.toBeRequired();
    expect(input).toBeEnabled();
  });

  test('exibe corretamente o placeholder', () => {
    const placeholderText = 'Digite seu nome';
    render(
      <Input
        id="test-input"
        label="Nome"
        placeholder={placeholderText}
        register={mockRegister}
      />
    );

    expect(screen.getByPlaceholderText(placeholderText)).toBeInTheDocument();
  });

  test('marca como obrigatório quando a prop required é true', () => {
    render(
      <Input
        id="required-input"
        label="Campo Obrigatório"
        register={mockRegister}
        required
      />
    );

    const input = screen.getByLabelText(/campo obrigatório/i);
    const requiredMark = screen.getByText('*');
    
    expect(input).toBeRequired();
    expect(requiredMark).toBeInTheDocument();
    expect(requiredMark).toHaveClass('text-red-500');
  });

  test('exibe mensagem de erro quando houver erro', () => {
    const errorMessage = 'Campo obrigatório';
    render(
      <Input
        id="error-input"
        label="Com Erro"
        register={mockRegister}
        error={{ message: errorMessage }}
      />
    );

    const errorElement = screen.getByText(`Erro: ${errorMessage}`);
    const input = screen.getByLabelText(/com erro/i);
    
    expect(errorElement).toBeInTheDocument();
    expect(input).toHaveClass('border-red-500', 'bg-red-50');
    expect(input).not.toHaveClass('border-gray-300', 'hover:border-gray-400');
  });

  test('desabilita o input quando disabled é true', () => {
    render(
      <Input
        id="disabled-input"
        label="Campo Desabilitado"
        register={mockRegister}
        disabled
      />
    );

    const input = screen.getByLabelText(/campo desabilitado/i);
    expect(input).toBeDisabled();
    expect(input).toHaveClass('bg-gray-100', 'cursor-not-allowed');
  });

  test('permite a digitação e chama a função register.onChange', () => {
    const testValue = 'Teste de digitação';
    render(
      <Input
        id="typing-input"
        label="Digite algo"
        register={mockRegister}
      />
    );

    const input = screen.getByLabelText(/digite algo/i);
    fireEvent.change(input, { target: { value: testValue } });

    expect(mockRegister.onChange).toHaveBeenCalledTimes(1);
    expect(mockRegister.onChange).toHaveBeenCalledWith(
      expect.objectContaining({
        target: expect.objectContaining({
          value: testValue,
        }),
      })
    );
  });

  test('aplica classes personalizadas através da prop className', () => {
    const customClass = 'custom-class';
    render(
      <Input
        id="custom-class-input"
        label="Com Classe Personalizada"
        register={mockRegister}
        className={customClass}
      />
    );

    const container = screen.getByText(/com classe personalizada/i).parentElement;
    expect(container).toHaveClass(customClass);
  });

  test('aplica autoComplete corretamente', () => {
    const autoCompleteValue = 'username';
    render(
      <Input
        id="autocomplete-input"
        label="Usuário"
        register={mockRegister}
        autoComplete={autoCompleteValue}
      />
    );

    const input = screen.getByLabelText(/usuário/i);
    expect(input).toHaveAttribute('autocomplete', autoCompleteValue);
  });

  test('aplica tipo de input correto', () => {
    const inputType = 'email';
    render(
      <Input
        id="email-input"
        label="E-mail"
        type={inputType}
        register={mockRegister}
      />
    );

    const input = screen.getByLabelText(/e-mail/i);
    expect(input).toHaveAttribute('type', inputType);
  });
});

