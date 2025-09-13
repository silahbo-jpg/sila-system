import { useState, useEffect, useCallback } from 'react';
import api from '../services/api';

interface SyncStatus {
  isOnline: boolean;
  isSyncing: boolean;
  lastSync: Date | null;
  pendingChanges: number;
  error: string | null;
}

interface OfflineData {
  id: string;
  type: 'create' | 'update' | 'delete';
  endpoint: string;
  data: any;
  timestamp: Date;
}

export const useMobileSync = () => {
  const [syncStatus, setSyncStatus] = useState<SyncStatus>({
    isOnline: navigator.onLine,
    isSyncing: false,
    lastSync: null,
    pendingChanges: 0,
    error: null,
  });

  const [offlineData, setOfflineData] = useState<OfflineData[]>([]);

  // Verificar status de conectividade
  useEffect(() => {
    const handleOnline = () => {
      setSyncStatus(prev => ({ ...prev, isOnline: true, error: null }));
      // Tentar sincronizar quando voltar online
      syncOfflineData();
    };

    const handleOffline = () => {
      setSyncStatus(prev => ({ ...prev, isOnline: false }));
    };

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  // Carregar dados offline do localStorage
  useEffect(() => {
    const loadOfflineData = () => {
      try {
        const stored = localStorage.getItem('offlineData');
        if (stored) {
          const data = JSON.parse(stored);
          setOfflineData(data);
          setSyncStatus(prev => ({ ...prev, pendingChanges: data.length }));
        }
      } catch (error) {
        console.error('Erro ao carregar dados offline:', error);
      }
    };

    loadOfflineData();
  }, []);

  // Salvar dados offline no localStorage
  const saveOfflineData = useCallback((data: OfflineData[]) => {
    try {
      localStorage.setItem('offlineData', JSON.stringify(data));
      setSyncStatus(prev => ({ ...prev, pendingChanges: data.length }));
    } catch (error) {
      console.error('Erro ao salvar dados offline:', error);
    }
  }, []);

  // Adicionar operação offline
  const addOfflineOperation = useCallback((operation: Omit<OfflineData, 'id' | 'timestamp'>) => {
    const newOperation: OfflineData = {
      ...operation,
      id: `${Date.now()}-${Math.random()}`,
      timestamp: new Date(),
    };

    const updatedData = [...offlineData, newOperation];
    setOfflineData(updatedData);
    saveOfflineData(updatedData);
  }, [offlineData, saveOfflineData]);

  // Sincronizar dados offline
  const syncOfflineData = useCallback(async () => {
    if (!syncStatus.isOnline || syncStatus.isSyncing || offlineData.length === 0) {
      return;
    }

    setSyncStatus(prev => ({ ...prev, isSyncing: true, error: null }));

    try {
      // Agrupar operações por tipo
      const operations = offlineData.reduce((acc, op) => {
        if (!acc[op.type]) acc[op.type] = [];
        acc[op.type].push(op);
        return acc;
      }, {} as Record<string, OfflineData[]>);

      // Processar operações em ordem: creates, updates, deletes
      const order = ['create', 'update', 'delete'];
      
      for (const type of order) {
        if (operations[type]) {
          for (const operation of operations[type]) {
            try {
              switch (operation.type) {
                case 'create':
                  await api.post(operation.endpoint, operation.data);
                  break;
                case 'update':
                  await api.put(operation.endpoint, operation.data);
                  break;
                case 'delete':
                  await api.delete(operation.endpoint);
                  break;
              }
            } catch (error) {
              console.error(`Erro ao sincronizar operação ${operation.type}:`, error);
              // Continuar com outras operações mesmo se uma falhar
            }
          }
        }
      }

      // Limpar dados sincronizados
      setOfflineData([]);
      saveOfflineData([]);
      
      setSyncStatus(prev => ({
        ...prev,
        isSyncing: false,
        lastSync: new Date(),
        pendingChanges: 0,
      }));

    } catch (error) {
      console.error('Erro durante sincronização:', error);
      setSyncStatus(prev => ({
        ...prev,
        isSyncing: false,
        error: 'Erro durante sincronização',
      }));
    }
  }, [syncStatus.isOnline, syncStatus.isSyncing, offlineData, saveOfflineData]);

  // API wrapper para operações offline
  const offlineApi = {
    post: async (endpoint: string, data: any) => {
      if (syncStatus.isOnline) {
        try {
          return await api.post(endpoint, data);
        } catch (error) {
          // Se falhar online, salvar offline
          addOfflineOperation({
            type: 'create',
            endpoint,
            data,
          });
          throw error;
        }
      } else {
        // Salvar offline
        addOfflineOperation({
          type: 'create',
          endpoint,
          data,
        });
        return { data: { id: 'offline-temp-id' } };
      }
    },

    put: async (endpoint: string, data: any) => {
      if (syncStatus.isOnline) {
        try {
          return await api.put(endpoint, data);
        } catch (error) {
          addOfflineOperation({
            type: 'update',
            endpoint,
            data,
          });
          throw error;
        }
      } else {
        addOfflineOperation({
          type: 'update',
          endpoint,
          data,
        });
        return { data };
      }
    },

    delete: async (endpoint: string) => {
      if (syncStatus.isOnline) {
        try {
          return await api.delete(endpoint);
        } catch (error) {
          addOfflineOperation({
            type: 'delete',
            endpoint,
            data: {},
          });
          throw error;
        }
      } else {
        addOfflineOperation({
          type: 'delete',
          endpoint,
          data: {},
        });
        return { success: true };
      }
    },

    get: async (endpoint: string) => {
      if (syncStatus.isOnline) {
        return await api.get(endpoint);
      } else {
        // Tentar buscar do cache local
        const cached = localStorage.getItem(`cache_${endpoint}`);
        if (cached) {
          return { data: JSON.parse(cached) };
        }
        throw new Error('Dados não disponíveis offline');
      }
    },
  };

  // Cache de dados para uso offline
  const cacheData = useCallback((endpoint: string, data: any) => {
    try {
      localStorage.setItem(`cache_${endpoint}`, JSON.stringify(data));
    } catch (error) {
      console.error('Erro ao cachear dados:', error);
    }
  }, []);

  // Limpar cache
  const clearCache = useCallback(() => {
    try {
      const keys = Object.keys(localStorage);
      keys.forEach(key => {
        if (key.startsWith('cache_')) {
          localStorage.removeItem(key);
        }
      });
    } catch (error) {
      console.error('Erro ao limpar cache:', error);
    }
  }, []);

  // Forçar sincronização
  const forceSync = useCallback(() => {
    if (syncStatus.isOnline) {
      syncOfflineData();
    }
  }, [syncStatus.isOnline, syncOfflineData]);

  return {
    syncStatus,
    offlineData,
    offlineApi,
    cacheData,
    clearCache,
    forceSync,
    syncOfflineData,
  };
}; 
