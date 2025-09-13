import React from 'react';
import { FileInput } from '../components/ui';
import type { Meta, StoryObj } from '@storybook/react';

// Configuração padrão para o componente FileInput
const meta: Meta<typeof FileInput> = {
  title: 'Components/FileInput',
  component: FileInput,
  tags: ['autodocs'],
  argTypes: {
    accept: { control: 'text' },
    disabled: { control: 'boolean' },
    required: { control: 'boolean' },
    multiple: { control: 'boolean' },
    error: { control: 'object' },
    helperText: { control: 'text' },
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
type Story = StoryObj<typeof FileInput>;

// Mock para o register do react-hook-form
const mockRegister = {
  name: 'fileInput',
  onChange: () => {},
  onBlur: () => {},
  ref: () => {},
};

// Componente de preview de imagem para os stories
const ImagePreview = ({ src }: { src: string }) => (
  <div className="mt-2">
    <p className="text-sm font-medium text-gray-700 mb-1">Preview:</p>
    <img 
      src={src} 
      alt="Preview" 
      className="w-32 h-32 object-cover rounded-md border border-gray-200" 
    />
  </div>
);

// Histórias (stories) para o componente FileInput
export const Default: Story = {
  args: {
    label: 'Enviar arquivo',
    id: 'file-upload',
    register: mockRegister,
  },
};

export const WithHelperText: Story = {
  args: {
    label: 'Documento de identificação',
    helperText: 'Apenas arquivos PDF, máximo 5MB',
    accept: '.pdf',
    register: mockRegister,
  },
};

export const WithError: Story = {
  args: {
    label: 'Foto de perfil',
    error: { message: 'O arquivo deve ser uma imagem' },
    register: mockRegister,
  },
};

export const Required: Story = {
  args: {
    label: 'Comprovante de residência',
    required: true,
    register: mockRegister,
  },
};

export const MultipleFiles: Story = {
  args: {
    label: 'Enviar múltiplos arquivos',
    multiple: true,
    helperText: 'Selecione um ou mais arquivos',
    register: {
      ...mockRegister,
      name: 'files',
    },
  },
};

export const WithImagePreview: Story = {
  args: {
    label: 'Foto do documento',
    accept: 'image/*',
    register: mockRegister,
  },
  render: (args) => {
    const [preview, setPreview] = React.useState<string | null>(null);
    
    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      const file = e.target.files?.[0];
      if (file) {
        const url = URL.createObjectURL(file);
        setPreview(url);
      }
    };
    
    return (
      <div>
        <FileInput 
          {...args} 
          onChange={handleFileChange}
        />
        {preview && <ImagePreview src={preview} />}
      </div>
    );
  },
};

export const Disabled: Story = {
  args: {
    label: 'Arquivo desabilitado',
    disabled: true,
    helperText: 'Este campo está desabilitado',
    register: mockRegister,
  },
};

export const WithCustomAccept: Story = {
  args: {
    label: 'Enviar documento',
    accept: '.pdf,.doc,.docx',
    helperText: 'Aceita apenas PDF e Word',
    register: mockRegister,
  },
};

