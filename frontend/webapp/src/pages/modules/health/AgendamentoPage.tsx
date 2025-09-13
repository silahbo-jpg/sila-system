import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { useAuth } from '../../../context/AuthContext';
import { MainLayout } from '../../../layouts/MainLayout';
import Button from '../../../components/ui/Button';
import Input from '../../../components/ui/Input';
import LoadingSpinner from '../../../components/common/LoadingSpinner';
import api from '../../../services/api';

interface AppointmentFormData {
  patientName: string;
  patientAge: number;
  patientPhone: string;
  specialty: string;
  preferredDate: string;
  preferredTime: string;
  symptoms: string;
  urgency: 'normal' | 'urgent' | 'emergency';
}

const AgendamentoPage: React.FC = () => {
  const { user } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  const [specialties, setSpecialties] = useState([
    'Clínico Geral',
    'Pediatria',
    'Ginecologia',
    'Cardiologia',
    'Ortopedia',
    'Dermatologia',
    'Oftalmologia',
    'Odontologia',
    'Psicologia',
    'Nutrição'
  ]);
  const [availableSlots, setAvailableSlots] = useState<string[]>([]);
  const [appointmentId, setAppointmentId] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
    reset
  } = useForm<AppointmentFormData>({
    defaultValues: {
      patientName: user?.name || '',
      urgency: 'normal'
    }
  });

  const selectedDate = watch('preferredDate');
  const selectedSpecialty = watch('specialty');

  // Simular busca de horários disponíveis
  useEffect(() => {
    if (selectedDate && selectedSpecialty) {
      // Em produção, isso viria da API
      const slots = [
        '08:00', '08:30', '09:00', '09:30', '10:00', '10:30',
        '14:00', '14:30', '15:00', '15:30', '16:00', '16:30'
      ];
      setAvailableSlots(slots);
    }
  }, [selectedDate, selectedSpecialty]);

  const onSubmit = async (data: AppointmentFormData) => {
    try {
      setIsLoading(true);
      
      const response = await api.post('/api/health/appointments/', {
        patientName: data.patientName,
        patientAge: data.patientAge,
        patientPhone: data.patientPhone,
        specialty: data.specialty,
        appointmentDate: `${data.preferredDate}T${data.preferredTime}:00`,
        symptoms: data.symptoms,
        urgency: data.urgency,
        userId: user?.id
      });

      setAppointmentId(response.data.id);
      
      // Mostrar sucesso
      alert('Consulta agendada com sucesso! ID: ' + response.data.id);
      
      // Resetar formulário
      reset();
      
    } catch (error: any) {
      console.error('Erro ao agendar consulta:', error);
      alert('Erro ao agendar consulta: ' + (error.response?.data?.detail || error.message));
    } finally {
      setIsLoading(false);
    }
  };

  const getMinDate = () => {
    const today = new Date();
    return today.toISOString().split('T')[0];
  };

  const getMaxDate = () => {
    const maxDate = new Date();
    maxDate.setDate(maxDate.getDate() + 30); // 30 dias à frente
    return maxDate.toISOString().split('T')[0];
  };

  return (
    <MainLayout>
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="bg-white shadow rounded-lg">
          <div className="px-6 py-4 border-b border-gray-200">
            <h1 className="text-2xl font-bold text-gray-900">
              Agendar Consulta Médica
            </h1>
            <p className="mt-1 text-sm text-gray-600">
              Preencha os dados para agendar sua consulta
            </p>
          </div>

          <div className="px-6 py-6">
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
              {/* Dados do paciente */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Input
                  label="Nome do Paciente"
                  {...register('patientName', { 
                    required: 'Nome é obrigatório',
                    minLength: {
                      value: 3,
                      message: 'Nome deve ter pelo menos 3 caracteres'
                    }
                  })}
                  error={errors.patientName?.message}
                />

                <Input
                  label="Idade"
                  type="number"
                  {...register('patientAge', { 
                    required: 'Idade é obrigatória',
                    min: { value: 0, message: 'Idade deve ser maior que 0' },
                    max: { value: 120, message: 'Idade deve ser menor que 120' }
                  })}
                  error={errors.patientAge?.message}
                />

                <Input
                  label="Telefone"
                  {...register('patientPhone', { 
                    required: 'Telefone é obrigatório',
                    pattern: {
                      value: /^[0-9+\-\s()]+$/,
                      message: 'Telefone inválido'
                    }
                  })}
                  error={errors.patientPhone?.message}
                  placeholder="+244 123 456 789"
                />
              </div>

              {/* Especialidade e urgência */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Especialidade
                  </label>
                  <select
                    {...register('specialty', { required: 'Especialidade é obrigatória' })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="">Selecione uma especialidade</option>
                    {specialties.map((specialty) => (
                      <option key={specialty} value={specialty}>
                        {specialty}
                      </option>
                    ))}
                  </select>
                  {errors.specialty && (
                    <p className="mt-1 text-sm text-red-600">{errors.specialty.message}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Urgência
                  </label>
                  <select
                    {...register('urgency')}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="normal">Normal</option>
                    <option value="urgent">Urgente</option>
                    <option value="emergency">Emergência</option>
                  </select>
                </div>
              </div>

              {/* Data e horário */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Input
                  label="Data Preferida"
                  type="date"
                  {...register('preferredDate', { 
                    required: 'Data é obrigatória'
                  })}
                  error={errors.preferredDate?.message}
                  min={getMinDate()}
                  max={getMaxDate()}
                />

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Horário Preferido
                  </label>
                  <select
                    {...register('preferredTime', { required: 'Horário é obrigatório' })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    disabled={!selectedDate || !selectedSpecialty}
                  >
                    <option value="">Selecione um horário</option>
                    {availableSlots.map((slot) => (
                      <option key={slot} value={slot}>
                        {slot}
                      </option>
                    ))}
                  </select>
                  {errors.preferredTime && (
                    <p className="mt-1 text-sm text-red-600">{errors.preferredTime.message}</p>
                  )}
                </div>
              </div>

              {/* Sintomas */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Sintomas / Motivo da Consulta
                </label>
                <textarea
                  {...register('symptoms', { 
                    required: 'Descrição dos sintomas é obrigatória',
                    minLength: {
                      value: 10,
                      message: 'Descrição deve ter pelo menos 10 caracteres'
                    }
                  })}
                  rows={4}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="Descreva seus sintomas ou motivo da consulta..."
                />
                {errors.symptoms && (
                  <p className="mt-1 text-sm text-red-600">{errors.symptoms.message}</p>
                )}
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
                  {isLoading ? <LoadingSpinner size="sm" /> : 'Agendar Consulta'}
                </Button>
              </div>
            </form>

            {appointmentId && (
              <div className="mt-8 p-4 bg-green-50 border border-green-200 rounded-lg">
                <h3 className="text-lg font-medium text-green-900 mb-2">
                  Consulta agendada com sucesso!
                </h3>
                <p className="text-sm text-green-700 mb-4">
                  ID da consulta: {appointmentId}
                </p>
                <p className="text-sm text-green-700">
                  Você receberá uma confirmação por SMS e email.
                </p>
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
              <li>• Chegue 15 minutos antes do horário</li>
              <li>• Traga documentos de identificação</li>
              <li>• Em caso de cancelamento, avise com antecedência</li>
              <li>• Consultas gratuitas para cidadãos cadastrados</li>
            </ul>
          </div>

          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
            <h3 className="text-lg font-medium text-yellow-900 mb-4">
              Horários de funcionamento
            </h3>
            <ul className="space-y-2 text-sm text-yellow-800">
              <li>• Segunda a Sexta: 8h às 17h</li>
              <li>• Sábados: 8h às 12h</li>
              <li>• Domingos: Fechado</li>
              <li>• Feriados: Plantão de emergência</li>
            </ul>
          </div>
        </div>
      </div>
    </MainLayout>
  );
};

export default AgendamentoPage; 
