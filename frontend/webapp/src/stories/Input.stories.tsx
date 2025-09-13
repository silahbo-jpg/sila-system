import React from 'react';
import { Input } from '../components/ui';
import type { Meta, StoryObj } from '@storybook/react';

// Configuração padrão para o componente Input
const meta: Meta<typeof Input> = {
  title: 'Components/Input',
  component: Input,
  tags: ['autodocs'],
  argTypes: {
    type: {
      control: { type: 'select' },
      options: ['text', 'email', 'password', 'number', 'tel'],
    },
    disabled: { control: 'boolean' },
    required: { control: 'boolean' },
    error: { control: 'object' },
    helperText: { control: 'text' },
  },
  // Mock para o register do react-hook-form
  parameters: {
    mockData: [
      {
        url: '/api/mock',
        method: 'GET',
        status: 200,
        response: {},
      },
    ],
  },
};

export default {
  ...meta,
  decorators: [
    (Story) => (
      <MemoryRouter>
        <Story />
      </MemoryRouter>
    ),
  ],
};
type Story = StoryObj<typeof Input>;

// Mock function para o register do react-hook-form
const mockRegister = {
  name: 'inputName',
  onChange: () => {},
  onBlur: () => {},
  ref: () => {},
};

// Histórias (stories) para o componente Input
export const Default: Story = {
  args: {
    label: 'Nome completo',
    placeholder: 'Digite seu nome',
    register: mockRegister,
  },
};

export const WithHelperText: Story = {
  args: {
    label: 'E-mail',
    type: 'email',
    placeholder: 'seu@email.com',
    helperText: 'Digite um e-mail válido',
    register: mockRegister,
  },
};

export const WithError: Story = {
  args: {
    label: 'Senha',
    type: 'password',
    error: { message: 'A senha deve ter no mínimo 6 caracteres' },
    register: mockRegister,
  },
};

export const Disabled: Story = {
  args: {
    label: 'Campo desabilitado',
    value: 'Valor pré-preenchido',
    disabled: true,
    register: mockRegister,
  },
};

export const Required: Story = {
  args: {
    label: 'Campo obrigatório',
    required: true,
    register: mockRegister,
  },
};

export const WithCustomWidth: Story = {
  args: {
    label: 'Largura personalizada',
    className: 'w-64',
    register: mockRegister,
  },
};

export const EmailType: Story = {
  args: {
    label: 'E-mail',
    type: 'email',
    placeholder: 'seu@email.com',
    autoComplete: 'email',
    register: mockRegister,
  },
};

export const PasswordType: Story = {
  args: {
    label: 'Senha',
    type: 'password',
    placeholder: '••••••••',
    autoComplete: 'current-password',
    register: mockRegister,
  },
};

export const TelType: Story = {
  args: {
    label: 'Telefone',
    type: 'tel',
    placeholder: '(00) 00000-0000',
    register: mockRegister,
  },
};

