import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { useAuth } from '../../../context/AuthContext';
import { MainLayout } from '../../../layouts/MainLayout';
import Button from '../../../components/ui/Button';
import Input from '../../../components/ui/Input';
import LoadingSpinner from '../../../components/common/LoadingSpinner';
import api from '../../../services/api';

interface CitizenFormData {
  nomeCompleto: string;
  numeroBi: string;
  cpf?: string;
  dataNascimento?: string;
  naturalidade?: string;
  residencia?: string;
}

const RegistroPage: React.FC = () => {
  const { user } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  const [citizenId, setCitizenId] = useState<number | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset
  } = useForm<CitizenFormData>({
    defaultValues: {
      nomeCompleto: user?.name || ''
    }
  });

  const onSubmit = async (data: CitizenFormData) => {
    try {
      setIsLoading(true);
      
      const response = await api.post('/api/citizenship/citizens/', {
        nomeCompleto: data.nomeCompleto,
        numeroBi: data.numeroBi,
        cpf: data.cpf || null,
        dataNascimento: data.dataNascimento || null,
        naturalidade: data.naturalidade || null,
        residencia: data.residencia || null
      });

      setCitizenId(response.data.id);
      
      // Mostrar sucesso
      alert('Cidadão registrado com sucesso! ID: ' + response.data.id);
      
      // Resetar formulário
      reset();
      
    } catch (error: any) {
      console.error('Erro ao registrar cidadão:', error);
      alert('Erro ao registrar cidadão: ' + (error.response?.data?.detail || error.message));
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <MainLayout>
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="bg-white shadow rounded-lg">
          <div className="px-6 py-4 border-b border-gray-200">
            <h1 className="text-2xl font-bold text-gray-900">
              Registro de Cidadão
            </h1>
            <p className="mt-1 text-sm text-gray-600">
              Cadastre-se como cidadão do município para acessar os serviços
            </p>
          </div>

          <div className="px-6 py-6">
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Input
                  label="Nome Completo"
                  {...register('nomeCompleto', { 
                    required: 'Nome é obrigatório',
                    minLength: {
                      value: 3,
                      message: 'Nome deve ter pelo menos 3 caracteres'
                    }
                  })}
                  error={errors.nomeCompleto?.message}
                />

                <Input
                  label="Número do BI"
                  {...register('numeroBi', { 
                    required: 'Número do BI é obrigatório',
                    pattern: {
                      value: /^[A-Z0-9]{9}[A-Z]{2}[0-9]{3}$/,
                      message: 'Formato inválido. Use: 999999999LA999'
                    }
                  })}
                  error={errors.numeroBi?.message}
                  placeholder="999999999LA999"
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Input
                  label="CPF (opcional)"
                  {...register('cpf')}
                  error={errors.cpf?.message}
                  placeholder="000.000.000-00"
                />

                <Input
                  label="Data de Nascimento"
                  type="date"
                  {...register('dataNascimento')}
                  error={errors.dataNascimento?.message}
                />
              </div>

              <Input
                label="Naturalidade"
                {...register('naturalidade')}
                error={errors.naturalidade?.message}
                placeholder="Cidade, Estado"
              />

              <Input
                label="Endereço de Residência"
                {...register('residencia')}
                error={errors.residencia?.message}
                placeholder="Rua, número, bairro, cidade"
              />

              <div className="flex justify-end space-x-4">
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => window.history.back()}
                >
                  Cancelar
                </Button>
                <Button
                  type="submit"
                  variant="primary"
                  disabled={isLoading}
                >
                  {isLoading ? <LoadingSpinner size="sm" /> : 'Registrar Cidadão'}
                </Button>
              </div>
            </form>

            {citizenId && (
              <div className="mt-8 p-4 bg-green-50 border border-green-200 rounded-lg">
                <h3 className="text-lg font-medium text-green-900 mb-2">
                  Cidadão registrado com sucesso!
                </h3>
                <p className="text-sm text-green-700 mb-4">
                  ID do cidadão: {citizenId}
                </p>
                <p className="text-sm text-green-700">
                  Agora você pode acessar todos os serviços de cidadania.
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Informações adicionais */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
            <h3 className="text-lg font-medium text-blue-900 mb-4">
              Benefícios do registro
            </h3>
            <ul className="space-y-2 text-sm text-blue-800">
              <li>• Acesso a todos os serviços municipais</li>
              <li>• Solicitação de documentos oficiais</li>
              <li>• Acompanhamento de processos</li>
              <li>• Notificações personalizadas</li>
            </ul>
          </div>

          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
            <h3 className="text-lg font-medium text-yellow-900 mb-4">
              Dados obrigatórios
            </h3>
            <ul className="space-y-2 text-sm text-yellow-800">
              <li>• Nome completo</li>
              <li>• Número do BI</li>
              <li>• Demais campos são opcionais</li>
            </ul>
          </div>
        </div>
      </div>
    </MainLayout>
  );
};

export default RegistroPage; 
