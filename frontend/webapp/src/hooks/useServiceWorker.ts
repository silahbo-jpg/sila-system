import { useState, useEffect, useCallback } from 'react';

interface ServiceWorkerState {
  isSupported: boolean;
  isInstalled: boolean;
  isActive: boolean;
  isUpdateAvailable: boolean;
  isInstalling: boolean;
  error: string | null;
}

interface NotificationState {
  isSupported: boolean;
  permission: NotificationPermission;
  isSubscribed: boolean;
}

export const useServiceWorker = () => {
  const [swState, setSwState] = useState({
    isSupported: 'serviceWorker' in navigator,
    isInstalled: false,
    isActive: false,
    isUpdateAvailable: false,
    isInstalling: false,
    error: null,
  } as ServiceWorkerState);

  const [notificationState, setNotificationState] = useState({
    isSupported: 'Notification' in window,
    permission: 'default' as NotificationPermission,
    isSubscribed: false,
  } as NotificationState);

  // Registrar Service Worker
  const registerServiceWorker = useCallback(async () => {
    if (!swState.isSupported) {
      setSwState(prev => ({ ...prev, error: 'Service Worker não suportado' }));
      return false;
    }

    try {
      setSwState(prev => ({ ...prev, isInstalling: true, error: null }));

      const registration = await navigator.serviceWorker.register('/sw.js', {
        scope: '/',
      });

      console.log('Service Worker registrado:', registration);

      // Verificar se há atualização disponível
      registration.addEventListener('updatefound', () => {
        const newWorker = registration.installing;
        if (newWorker) {
          newWorker.addEventListener('statechange', () => {
            if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
              setSwState(prev => ({ ...prev, isUpdateAvailable: true }));
            }
          });
        }
      });

      // Atualizar estado
      setSwState(prev => ({
        ...prev,
        isInstalled: true,
        isActive: !!registration.active,
        isInstalling: false,
      }));

      return true;
    } catch (error) {
      console.error('Erro ao registrar Service Worker:', error);
      setSwState(prev => ({
        ...prev,
        error: `Erro ao registrar: ${error}`,
        isInstalling: false,
      }));
      return false;
    }
  }, [swState.isSupported]);

  // Atualizar Service Worker
  const updateServiceWorker = useCallback(() => {
    if (swState.isUpdateAvailable) {
      navigator.serviceWorker.controller?.postMessage({ type: 'SKIP_WAITING' });
      window.location.reload();
    }
  }, [swState.isUpdateAvailable]);

  // Verificar permissões de notificação
  const checkNotificationPermission = useCallback(async () => {
    if (!notificationState.isSupported) {
      return;
    }

    const permission = await Notification.requestPermission();
    setNotificationState(prev => ({ ...prev, permission }));

    return permission;
  }, [notificationState.isSupported]);

  // Solicitar permissão de notificação
  const requestNotificationPermission = useCallback(async () => {
    if (!notificationState.isSupported) {
      return false;
    }

    const permission = await Notification.requestPermission();
    setNotificationState(prev => ({ ...prev, permission }));

    if (permission === 'granted') {
      // Registrar para notificações push
      await registerForPushNotifications();
    }

    return permission === 'granted';
  }, [notificationState.isSupported]);

  // Registrar para notificações push
  const registerForPushNotifications = useCallback(async () => {
    if (!swState.isInstalled || notificationState.permission !== 'granted') {
      return false;
    }

    try {
      const registration = await navigator.serviceWorker.ready;
      const subscription = await registration.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: urlBase64ToUint8Array(''),
      });

      // Enviar subscription para o servidor
      await fetch('/api/notifications/subscribe', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(subscription),
      });

      setNotificationState(prev => ({ ...prev, isSubscribed: true }));
      return true;
    } catch (error) {
      console.error('Erro ao registrar notificações push:', error);
      return false;
    }
  }, [swState.isInstalled, notificationState.permission]);

  // Enviar notificação local
  const sendLocalNotification = useCallback((title: string, options?: NotificationOptions) => {
    if (notificationState.permission === 'granted') {
      return new Notification(title, {
        icon: '/icons/icon-192x192.png',
        badge: '/icons/icon-72x72.png',
        ...options,
      });
    }
    return null;
  }, [notificationState.permission]);

  // Sincronizar dados offline
  const syncOfflineData = useCallback(async () => {
    if (!swState.isInstalled) {
      return false;
    }

    try {
      const registration = await navigator.serviceWorker.ready;
      
      if ('sync' in registration) {
        await (registration as any).sync.register('background-sync');
        return true;
      }
      
      return false;
    } catch (error) {
      console.error('Erro ao sincronizar dados offline:', error);
      return false;
    }
  }, [swState.isInstalled]);

  // Verificar conectividade
  const checkConnectivity = useCallback(() => {
    return navigator.onLine;
  }, []);

  // Instalar PWA
  const installPWA = useCallback(async () => {
    if (!swState.isInstalled) {
      return false;
    }

    try {
      const registration = await navigator.serviceWorker.ready;
      
      if ('beforeinstallprompt' in window) {
        const promptEvent = (window as any).deferredPrompt;
        if (promptEvent) {
          promptEvent.prompt();
          const result = await promptEvent.userChoice;
          (window as any).deferredPrompt = null;
          return result.outcome === 'accepted';
        }
      }
      
      return false;
    } catch (error) {
      console.error('Erro ao instalar PWA:', error);
      return false;
    }
  }, [swState.isInstalled]);

  // Efeitos
  useEffect(() => {
    // Registrar Service Worker na inicialização
    registerServiceWorker();

    // Verificar permissão de notificação
    if (notificationState.isSupported) {
      setNotificationState(prev => ({ 
        ...prev, 
        permission: Notification.permission 
      }));
    }

    // Listener para eventos de conectividade
    const handleOnline = () => {
      console.log('Aplicação online');
      syncOfflineData();
    };

    const handleOffline = () => {
      console.log('Aplicação offline');
    };

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    // Listener para prompt de instalação
    const handleBeforeInstallPrompt = (event: Event) => {
      event.preventDefault();
      (window as any).deferredPrompt = event;
    };

    window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
      window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
    };
  }, []);

  // Converter VAPID key
  const urlBase64ToUint8Array = (base64String: string) => {
    const padding = '='.repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding)
      .replace(/-/g, '+')
      .replace(/_/g, '/');

    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);

    for (let i = 0; i < rawData.length; ++i) {
      outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray;
  };

  return {
    // Estado do Service Worker
    swState,
    
    // Estado das notificações
    notificationState,
    
    // Métodos do Service Worker
    registerServiceWorker,
    updateServiceWorker,
    
    // Métodos de notificação
    checkNotificationPermission,
    requestNotificationPermission,
    sendLocalNotification,
    
    // Métodos de sincronização
    syncOfflineData,
    
    // Métodos de conectividade
    checkConnectivity,
    
    // Métodos de instalação
    installPWA,
  };
}; 
