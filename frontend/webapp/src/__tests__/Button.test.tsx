import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import { Button } from '../components/ui';

describe('Button Component', () => {
  test('renderiza corretamente com props padrão', () => {
    render(<Button>Clique aqui</Button>);
    
    const button = screen.getByRole('button', { name: /clique aqui/i });
    
    expect(button).toBeInTheDocument();
    expect(button).toHaveAttribute('type', 'button');
    expect(button).toHaveClass('bg-blue-600'); // Cor primária por padrão
    expect(button).toHaveClass('px-4'); // Tamanho médio por padrão
    expect(button).not.toBeDisabled();
  });

  test('renderiza com variante secundária', () => {
    render(<Button variant="secondary">Secundário</Button>);
    
    const button = screen.getByRole('button', { name: /secundário/i });
    
    expect(button).toHaveClass('bg-gray-600');
    expect(button).toHaveClass('hover:bg-gray-700');
  });

  test('renderiza com variante de perigo', () => {
    render(<Button variant="danger">Excluir</Button>);
    
    const button = screen.getByRole('button', { name: /excluir/i });
    
    expect(button).toHaveClass('bg-red-600');
    expect(button).toHaveClass('hover:bg-red-700');
  });

  test('renderiza com tamanho pequeno', () => {
    render(<Button size="sm">Pequeno</Button>);
    
    const button = screen.getByRole('button', { name: /pequeno/i });
    
    expect(button).toHaveClass('px-3');
    expect(button).toHaveClass('py-1.5');
    expect(button).toHaveClass('text-sm');
  });

  test('renderiza com largura total', () => {
    render(<Button fullWidth>Largura Total</Button>);
    
    const button = screen.getByRole('button', { name: /largura total/i });
    
    expect(button).toHaveClass('w-full');
  });

  test('mostra ícone de carregamento quando isLoading é true', () => {
    render(<Button isLoading>Carregando</Button>);
    
    const button = screen.getByRole('button', { name: /carregando/i });
    const spinner = button.querySelector('svg.animate-spin');
    
    expect(spinner).toBeInTheDocument();
  });

  test('desabilita o botão quando disabled é true', () => {
    render(<Button disabled>Desabilitado</Button>);
    
    const button = screen.getByRole('button', { name: /desabilitado/i });
    
    expect(button).toBeDisabled();
    expect(button).toHaveClass('opacity-70');
    expect(button).toHaveClass('cursor-not-allowed');
  });

  test('desabilita o botão quando isLoading é true', () => {
    render(<Button isLoading>Carregando</Button>);
    
    const button = screen.getByRole('button', { name: /carregando/i });
    
    expect(button).toBeDisabled();
  });

  test('chama a função onClick quando clicado', () => {
    const handleClick = jest.fn();
    
    render(<Button onClick={handleClick}>Clique-me</Button>);
    
    const button = screen.getByRole('button', { name: /clique-me/i });
    fireEvent.click(button);
    
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  test('não chama a função onClick quando desabilitado', () => {
    const handleClick = jest.fn();
    
    render(
      <Button onClick={handleClick} disabled>
        Desabilitado
      </Button>
    );
    
    const button = screen.getByRole('button', { name: /desabilitado/i });
    fireEvent.click(button);
    
    expect(handleClick).not.toHaveBeenCalled();
  });

  test('aplica classes personalizadas através da prop className', () => {
    const customClass = 'custom-class';
    
    render(<Button className={customClass}>Personalizado</Button>);
    
    const button = screen.getByRole('button', { name: /personalizado/i });
    
    expect(button).toHaveClass(customClass);
  });

  test('renderiza com tipo submit', () => {
    render(<Button type="submit">Enviar</Button>);
    
    const button = screen.getByRole('button', { name: /enviar/i });
    
    expect(button).toHaveAttribute('type', 'submit');
  });
});

