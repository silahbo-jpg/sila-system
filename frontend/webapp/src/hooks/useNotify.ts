/**
 * Hook unificado para notificações visuais e de backend
 * Reutilizado em todos os forms e componentes
 */
import { useState, useCallback } from 'react';

export type NotificationLevel = 'info' | 'success' | 'warning' | 'error';

export interface Notification {
  id: string;
  message: string;
  level: NotificationLevel;
  title?: string;
  duration?: number;
  persistent?: boolean;
}

export interface NotificationOptions {
  level?: NotificationLevel;
  title?: string;
  duration?: number;
  persistent?: boolean;
}

export const useNotify = () => {
  const [notifications, setNotifications] = useState<Notification[]>([]);

  const addNotification = useCallback((
    message: string, 
    options: NotificationOptions = {}
  ) => {
    const {
      level = 'info',
      title,
      duration = 5000,
      persistent = false
    } = options;

    const id = `notif_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    
    const notification: Notification = {
      id,
      message,
      level,
      title,
      duration,
      persistent
    };

    setNotifications(prev => [...prev, notification]);

    // Auto-remove notification after duration (unless persistent)
    if (!persistent && duration > 0) {
      setTimeout(() => {
        removeNotification(id);
      }, duration);
    }

    return id;
  }, []);

  const removeNotification = useCallback((id: string) => {
    setNotifications(prev => prev.filter(notif => notif.id !== id));
  }, []);

  const clearAllNotifications = useCallback(() => {
    setNotifications([]);
  }, []);

  // Convenience methods for different notification levels
  const info = useCallback((message: string, options?: Omit<NotificationOptions, 'level'>) => {
    return addNotification(message, { ...options, level: 'info' });
  }, [addNotification]);

  const success = useCallback((message: string, options?: Omit<NotificationOptions, 'level'>) => {
    return addNotification(message, { ...options, level: 'success' });
  }, [addNotification]);

  const warning = useCallback((message: string, options?: Omit<NotificationOptions, 'level'>) => {
    return addNotification(message, { ...options, level: 'warning' });
  }, [addNotification]);

  const error = useCallback((message: string, options?: Omit<NotificationOptions, 'level'>) => {
    return addNotification(message, { ...options, level: 'error' });
  }, [addNotification]);

  // API integration methods
  const sendBackendNotification = useCallback(async (
    userId: number,
    title: string,
    message: string,
    channel: 'email' | 'sms' | 'push' | 'in_app' = 'in_app'
  ) => {
    try {
      const response = await fetch('/api/notifications/send', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          user_id: userId,
          title,
          message,
          channel
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      
      // Show success notification
      success(`Notificação enviada via ${channel}`);
      
      return result;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Erro ao enviar notificação';
      error(errorMessage);
      throw err;
    }
  }, [success, error]);

  const fetchUserNotifications = useCallback(async (userId: number, limit = 10) => {
    try {
      const response = await fetch(`/api/notifications/user/${userId}?limit=${limit}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Erro ao buscar notificações';
      error(errorMessage);
      throw err;
    }
  }, [error]);

  const markNotificationAsRead = useCallback(async (notificationId: string) => {
    try {
      const response = await fetch(`/api/notifications/${notificationId}/mark-read`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Erro ao marcar notificação como lida';
      error(errorMessage);
      throw err;
    }
  }, [error]);

  return {
    notifications,
    addNotification,
    removeNotification,
    clearAllNotifications,
    info,
    success,
    warning,
    error,
    sendBackendNotification,
    fetchUserNotifications,
    markNotificationAsRead
  };
}; 
