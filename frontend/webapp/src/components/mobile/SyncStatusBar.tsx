import React from 'react';
import { useMobileSync } from '../../hooks/useMobileSync';
import LoadingSpinner from '../common/LoadingSpinner';

const SyncStatusBar: React.FC = () => {
  const { syncStatus, forceSync } = useMobileSync();

  if (syncStatus.isOnline && syncStatus.pendingChanges === 0) {
    return null; // Não mostrar se estiver online e sem mudanças pendentes
  }

  return (
    <div className="fixed bottom-0 left-0 right-0 z-50 bg-white border-t border-gray-200 shadow-lg">
      <div className="px-4 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            {/* Status de conectividade */}
            <div className="flex items-center">
              {syncStatus.isOnline ? (
                <div className="flex items-center text-green-600">
                  <svg className="h-4 w-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  <span className="text-sm font-medium">Online</span>
                </div>
              ) : (
                <div className="flex items-center text-red-600">
                  <svg className="h-4 w-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                  </svg>
                  <span className="text-sm font-medium">Offline</span>
                </div>
              )}
            </div>

            {/* Status de sincronização */}
            {syncStatus.pendingChanges > 0 && (
              <div className="flex items-center text-orange-600">
                <svg className="h-4 w-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clipRule="evenodd" />
                </svg>
                <span className="text-sm font-medium">
                  {syncStatus.pendingChanges} mudança{syncStatus.pendingChanges > 1 ? 's' : ''} pendente{syncStatus.pendingChanges > 1 ? 's' : ''}
                </span>
              </div>
            )}

            {/* Indicador de sincronização */}
            {syncStatus.isSyncing && (
              <div className="flex items-center text-blue-600">
                <LoadingSpinner size="sm" />
                <span className="text-sm font-medium ml-1">Sincronizando...</span>
              </div>
            )}
          </div>

          {/* Botão de sincronização manual */}
          {syncStatus.isOnline && syncStatus.pendingChanges > 0 && !syncStatus.isSyncing && (
            <button
              onClick={forceSync}
              className="px-3 py-1 bg-blue-600 text-white text-sm font-medium rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            >
              Sincronizar
            </button>
          )}

          {/* Última sincronização */}
          {syncStatus.lastSync && (
            <div className="text-xs text-gray-500">
              Última sincronização: {syncStatus.lastSync.toLocaleTimeString()}
            </div>
          )}
        </div>

        {/* Mensagem de erro */}
        {syncStatus.error && (
          <div className="mt-2 p-2 bg-red-50 border border-red-200 rounded-md">
            <div className="flex items-center text-red-800">
              <svg className="h-4 w-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
              <span className="text-sm">{syncStatus.error}</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default SyncStatusBar; 
