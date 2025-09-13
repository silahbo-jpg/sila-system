/**
 * Hook para dados unificados do cidadão
 * Centraliza todas as informações do munícipe para o dashboard
 */
import { useState, useEffect, useCallback } from 'react';
import { useAuth } from '../context/AuthContext';

export interface CitizenData {
  id: number;
  nome_completo: string;
  numero_bi: string;
  naturalidade?: string;
  residencia?: string;
  fiscal: {
    total_taxas: number;
    taxas_pendentes: number;
    taxas_pagas: number;
    proximo_vencimento?: string;
  };
  licencas: {
    total: number;
    ativas: number;
    vencendo_em_30_dias: number;
    vencidas: number;
  };
  processos: {
    total: number;
    em_andamento: number;
    concluidos: number;
    pendentes: number;
  };
  notificacoes: {
    total: number;
    nao_lidas: number;
    recentes: Array<{
      id: string;
      title: string;
      message: string;
      created_at: string;
      read: boolean;
    }>;
  };
  agendamentos: {
    total: number;
    proximos: Array<{
      id: string;
      service: string;
      location: string;
      datetime: string;
      status: string;
    }>;
  };
  ultimas_atividades: Array<{
    id: string;
    title: string;
    status: string;
    date: string;
    icon: string;
  }>;
}

export const useCitizenData = () => {
  const { user } = useAuth();
  const [data, setData] = useState<CitizenData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchCitizenData = useCallback(async () => {
    if (!user?.id) {
      setError('Usuário não autenticado');
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      setError(null);

      // Buscar dados unificados do cidadão
      const response = await fetch(`/api/citizen/${user.id}/summary`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const citizenData = await response.json();
      setData(citizenData);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Erro ao buscar dados do cidadão';
      setError(errorMessage);
      console.error('Erro ao buscar dados do cidadão:', err);
    } finally {
      setLoading(false);
    }
  }, [user?.id]);

  const refreshData = useCallback(() => {
    fetchCitizenData();
  }, [fetchCitizenData]);

  // Buscar dados na montagem do componente
  useEffect(() => {
    fetchCitizenData();
  }, [fetchCitizenData]);

  // Buscar dados específicos
  const fetchFiscalData = useCallback(async () => {
    if (!user?.id) return null;

    try {
      const response = await fetch(`/api/citizen/${user.id}/fiscal`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (err) {
      console.error('Erro ao buscar dados fiscais:', err);
      return null;
    }
  }, [user?.id]);

  const fetchLicensesData = useCallback(async () => {
    if (!user?.id) return null;

    try {
      const response = await fetch(`/api/citizen/${user.id}/licenses`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (err) {
      console.error('Erro ao buscar dados de licenças:', err);
      return null;
    }
  }, [user?.id]);

  const fetchProcessesData = useCallback(async () => {
    if (!user?.id) return null;

    try {
      const response = await fetch(`/api/citizen/${user.id}/processes`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (err) {
      console.error('Erro ao buscar dados de processos:', err);
      return null;
    }
  }, [user?.id]);

  const fetchNotificationsData = useCallback(async () => {
    if (!user?.id) return null;

    try {
      const response = await fetch(`/api/notifications/user/${user.id}?limit=10`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (err) {
      console.error('Erro ao buscar notificações:', err);
      return null;
    }
  }, [user?.id]);

  const fetchAppointmentsData = useCallback(async () => {
    if (!user?.id) return null;

    try {
      const response = await fetch(`/api/appointments/user/${user.id}?limit=5`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (err) {
      console.error('Erro ao buscar agendamentos:', err);
      return null;
    }
  }, [user?.id]);

  return {
    data,
    loading,
    error,
    refreshData,
    fetchFiscalData,
    fetchLicensesData,
    fetchProcessesData,
    fetchNotificationsData,
    fetchAppointmentsData
  };
}; 
