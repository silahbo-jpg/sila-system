import React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Button } from '../../../components/ui/Button';
import { Input } from '../../../components/ui/Input';
import { Select } from '../../../components/ui/Select';
import { citizenshipApi } from '../api/citizenshipApi';
import { toast } from 'react-hot-toast';

// Define validation schema using Zod
const citizenRequestSchema = z.object({
  name: z.string().min(3, 'Nome deve ter pelo menos 3 caracteres'),
  nif: z.string().regex(/^\d{9}$/, 'NIF deve ter 9 dígitos'),
  birthDate: z.string().regex(/^\d{4}-\d{2}-\d{2}$/, 'Data inválida'),
  gender: z.enum(['M', 'F', 'O']),
  address: z.object({
    street: z.string().min(3, 'Rua inválida'),
    city: z.string().min(2, 'Cidade inválida'),
    postalCode: z.string().regex(/^\d{4}-\d{3}$/, 'Código postal inválido'),
  }),
  contact: z.object({
    email: z.string().email('Email inválido').optional(),
    phone: z.string().min(9, 'Telefone inválido'),
  }),
  // Add other fields as needed
});

type CitizenRequestFormData = z.infer<typeof citizenRequestSchema>;

interface CitizenRequestFormProps {
  initialData?: Partial<CitizenRequestFormData>;
  onSuccess?: () => void;
  onCancel?: () => void;
}

export const CitizenRequestForm: React.FC<CitizenRequestFormProps> = ({
  initialData = {},
  onSuccess,
  onCancel,
}) => {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
  } = useForm<CitizenRequestFormData>({
    resolver: zodResolver(citizenRequestSchema),
    defaultValues: initialData,
  });

  const onSubmit = async (data: CitizenRequestFormData) => {
    try {
      if (initialData.id) {
        // Update existing request
        await citizenshipApi.updateCitizenRequest(initialData.id as string, data);
        toast.success('Pedido atualizado com sucesso!');
      } else {
        // Create new request
        await citizenshipApi.createCitizenRequest(data);
        toast.success('Pedido criado com sucesso!');
      }
      onSuccess?.();
      reset();
    } catch (error) {
      console.error('Error submitting form:', error);
      toast.error('Ocorreu um erro ao processar o pedido. Por favor, tente novamente.');
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <div className="space-y-4">
        <h2 className="text-xl font-semibold">Dados Pessoais</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <Input
              label="Nome Completo"
              {...register('name')}
              error={errors.name?.message}
              required
            />
          </div>
          <div>
            <Input
              label="NIF"
              {...register('nif')}
              error={errors.nif?.message}
              placeholder="123456789"
              required
            />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <Input
              type="date"
              label="Data de Nascimento"
              {...register('birthDate')}
              error={errors.birthDate?.message}
              required
            />
          </div>
          <div>
            <Select
              label="Género"
              {...register('gender')}
              error={errors.gender?.message}
              options={[
                { value: 'M', label: 'Masculino' },
                { value: 'F', label: 'Feminino' },
                { value: 'O', label: 'Outro' },
              ]}
              required
            />
          </div>
        </div>

        <h3 className="text-lg font-semibold mt-6">Morada</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <Input
              label="Rua"
              {...register('address.street')}
              error={errors.address?.street?.message}
              required
            />
          </div>
          <div>
            <Input
              label="Cidade"
              {...register('address.city')}
              error={errors.address?.city?.message}
              required
            />
          </div>
          <div>
            <Input
              label="Código Postal"
              {...register('address.postalCode')}
              placeholder="0000-000"
              error={errors.address?.postalCode?.message}
              required
            />
          </div>
        </div>

        <h3 className="text-lg font-semibold mt-6">Contactos</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <Input
              type="email"
              label="Email"
              {...register('contact.email')}
              error={errors.contact?.email?.message}
            />
          </div>
          <div>
            <Input
              label="Telefone"
              {...register('contact.phone')}
              error={errors.contact?.phone?.message}
              placeholder="912 345 678"
              required
            />
          </div>
        </div>
      </div>

      <div className="flex justify-end space-x-4 pt-6">
        {onCancel && (
          <Button type="button" variant="outline" onClick={onCancel}>
            Cancelar
          </Button>
        )}
        <Button type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'A processar...' : 'Submeter Pedido'}
        </Button>
      </div>
    </form>
  );
};

