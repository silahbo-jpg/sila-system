import React, { useState, useEffect } from 'react';
import { useServiceWorker } from '../../hooks/useServiceWorker';
import Button from '../ui/Button';

const PWAInstallPrompt: React.FC = () => {
  const { swState, installPWA } = useServiceWorker();
  const [showPrompt, setShowPrompt] = useState(false);
  const [hasPrompt, setHasPrompt] = useState(false);

  useEffect(() => {
    // Verificar se o PWA pode ser instalado
    const checkInstallability = () => {
      const isStandalone = window.matchMedia('(display-mode: standalone)').matches;
      const isInstalled = document.referrer.includes('android-app://');
      
      if (!isStandalone && !isInstalled && swState.isInstalled) {
        setHasPrompt(true);
        setShowPrompt(true);
      }
    };

    // Aguardar um pouco para mostrar o prompt
    const timer = setTimeout(checkInstallability, 3000);

    return () => clearTimeout(timer);
  }, [swState.isInstalled]);

  const handleInstall = async () => {
    const success = await installPWA();
    if (success) {
      setShowPrompt(false);
    }
  };

  const handleDismiss = () => {
    setShowPrompt(false);
    // Salvar no localStorage para não mostrar novamente por um tempo
    localStorage.setItem('pwa-prompt-dismissed', Date.now().toString());
  };

  const handleLater = () => {
    setShowPrompt(false);
    // Salvar no localStorage para mostrar novamente em 24h
    localStorage.setItem('pwa-prompt-dismissed', Date.now().toString());
  };

  // Verificar se deve mostrar o prompt
  useEffect(() => {
    const dismissed = localStorage.getItem('pwa-prompt-dismissed');
    if (dismissed) {
      const dismissedTime = parseInt(dismissed);
      const now = Date.now();
      const oneDay = 24 * 60 * 60 * 1000; // 24 horas
      
      if (now - dismissedTime < oneDay) {
        setShowPrompt(false);
      }
    }
  }, []);

  if (!showPrompt || !hasPrompt) {
    return null;
  }

  return (
    <div className="fixed bottom-0 left-0 right-0 z-50 bg-white border-t border-gray-200 shadow-lg">
      <div className="px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="flex-shrink-0">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <svg className="w-6 h-6 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M3 4a1 1 0 011-1h4a1 1 0 010 2H6.414l2.293 2.293a1 1 0 11-1.414 1.414L5 6.414V8a1 1 0 01-2 0V4zm9 1a1 1 0 010-2h4a1 1 0 011 1v4a1 1 0 01-2 0V6.414l-2.293 2.293a1 1 0 11-1.414-1.414L13.586 5H12z" clipRule="evenodd" />
                </svg>
              </div>
            </div>
            <div>
              <h3 className="text-sm font-medium text-gray-900">
                Instalar SILA - HUAMBO
              </h3>
              <p className="text-xs text-gray-500">
                Instale o app para acesso rápido e offline
              </p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <Button
              variant="outline"
              size="sm"
              onClick={handleLater}
              className="text-xs"
            >
              Depois
            </Button>
            <Button
              variant="primary"
              size="sm"
              onClick={handleInstall}
              className="text-xs"
            >
              Instalar
            </Button>
            <button
              onClick={handleDismiss}
              className="text-gray-400 hover:text-gray-600"
            >
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PWAInstallPrompt; 
