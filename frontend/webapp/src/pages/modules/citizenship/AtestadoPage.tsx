import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { useAuth } from '../../../context/AuthContext';
import { MainLayout } from '../../../layouts/MainLayout';
import Button from '../../../components/ui/Button';
import Input from '../../../components/ui/Input';
import LoadingSpinner from '../../../components/common/LoadingSpinner';
import api from '../../../services/api';

interface AtestadoFormData {
  nomeCompleto: string;
  numeroBi: string;
  morada: string;
  finalidade: string;
  data: string;
}

const AtestadoPage: React.FC = () => {
  const { user } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  const [atestadoId, setAtestadoId] = useState<number | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset
  } = useForm<AtestadoFormData>({
    defaultValues: {
      nomeCompleto: user?.name || '',
      data: new Date().toISOString().split('T')[0]
    }
  });

  const onSubmit = async (data: AtestadoFormData) => {
    try {
      setIsLoading(true);
      
      const response = await api.post('/api/citizenship/atestado/', {
        nomeCompleto: data.nomeCompleto,
        numeroBi: data.numeroBi,
        morada: data.morada,
        finalidade: data.finalidade,
        data: data.data
      });

      setAtestadoId(response.data.id);
      
      // Mostrar sucesso
      alert('Atestado solicitado com sucesso! ID: ' + response.data.id);
      
      // Resetar formulário
      reset();
      
    } catch (error: any) {
      console.error('Erro ao solicitar atestado:', error);
      alert('Erro ao solicitar atestado: ' + (error.response?.data?.detail || error.message));
    } finally {
      setIsLoading(false);
    }
  };

  const downloadPDF = async () => {
    if (!atestadoId) return;
    
    try {
      const response = await api.get(`/api/citizenship/atestado/${atestadoId}/pdf`, {
        responseType: 'blob'
      });
      
      // Criar link para download
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `atestado_${atestadoId}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      
    } catch (error) {
      console.error('Erro ao baixar PDF:', error);
      alert('Erro ao baixar PDF');
    }
  };

  return (
    <MainLayout>
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="bg-white shadow rounded-lg">
          <div className="px-6 py-4 border-b border-gray-200">
            <h1 className="text-2xl font-bold text-gray-900">
              Solicitar Atestado de Residência
            </h1>
            <p className="mt-1 text-sm text-gray-600">
              Preencha os dados para solicitar seu atestado de residência oficial
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

              <Input
                label="Morada"
                {...register('morada', { 
                  required: 'Morada é obrigatória',
                  minLength: {
                    value: 10,
                    message: 'Morada deve ter pelo menos 10 caracteres'
                  }
                })}
                error={errors.morada?.message}
                placeholder="Rua, número, bairro, cidade"
              />

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Input
                  label="Finalidade"
                  {...register('finalidade', { 
                    required: 'Finalidade é obrigatória'
                  })}
                  error={errors.finalidade?.message}
                  placeholder="Ex: Matrícula escolar, trabalho, etc."
                />

                <Input
                  label="Data"
                  type="date"
                  {...register('data', { 
                    required: 'Data é obrigatória'
                  })}
                  error={errors.data?.message}
                />
              </div>

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
                  {isLoading ? <LoadingSpinner size="sm" /> : 'Solicitar Atestado'}
                </Button>
              </div>
            </form>

            {atestadoId && (
              <div className="mt-8 p-4 bg-green-50 border border-green-200 rounded-lg">
                <h3 className="text-lg font-medium text-green-900 mb-2">
                  Atestado solicitado com sucesso!
                </h3>
                <p className="text-sm text-green-700 mb-4">
                  ID do atestado: {atestadoId}
                </p>
                <Button
                  variant="primary"
                  onClick={downloadPDF}
                  className="w-full md:w-auto"
                >
                  Baixar PDF
                </Button>
              </div>
            )}
          </div>
        </div>

        {/* Informações adicionais */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
            <h3 className="text-lg font-medium text-blue-900 mb-4">
              Informações importantes
            </h3>
            <ul className="space-y-2 text-sm text-blue-800">
              <li>• O atestado será processado em até 3 dias úteis</li>
              <li>• Você receberá uma notificação por email</li>
              <li>• O documento possui QR Code para validação</li>
              <li>• Mantenha o ID do atestado para consultas</li>
            </ul>
          </div>

          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
            <h3 className="text-lg font-medium text-yellow-900 mb-4">
              Documentos necessários
            </h3>
            <ul className="space-y-2 text-sm text-yellow-800">
              <li>• Bilhete de Identidade (BI)</li>
              <li>• Comprovante de residência</li>
              <li>• Dados pessoais atualizados</li>
            </ul>
          </div>
        </div>
      </div>
    </MainLayout>
  );
};

export default AtestadoPage; 
