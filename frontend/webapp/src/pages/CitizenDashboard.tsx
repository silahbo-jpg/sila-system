import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { MainLayout } from '../layouts/MainLayout';
import { Button } from '../components/ui/Button';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { getFeaturedModules, getModulesByCategory } from '../data/modules';
import { useFeatureFlags } from '../hooks/useFeatureFlags';

// Mock data - in a real app, this would come from an API
const mockNotifications = [
  { id: 1, title: 'Atualização de status', message: 'Seu pedido #12345 foi aprovado', date: '10 min atrás', read: false, type: 'success' },
  { id: 2, title: 'Novo serviço disponível', message: 'Confira o novo serviço de agendamento online', date: '2 horas atrás', read: true, type: 'info' },
  { id: 3, title: 'Documento pronto', message: 'Sua certidão de nascimento está disponível para download', date: '1 dia atrás', read: true, type: 'document' },
];

const mockRecentActivities = [
  { id: 1, title: 'Solicitação de 2ª via de RG', status: 'Concluído', date: 'Hoje', icon: 'document-text' },
  { id: 2, title: 'Agendamento de atendimento', status: 'Aguardando confirmação', date: 'Ontem', icon: 'calendar' },
  { id: 3, title: 'Atualização cadastral', status: 'Em andamento', date: '3 dias atrás', icon: 'pencil' },
];

const CitizenDashboard: React.FC = () => {
  const { user, logout } = useAuth();
  const { isFeatureEnabled } = useFeatureFlags();
  const navigate = useNavigate();
  
  const [isLoading, setIsLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');
  const [notifications, setNotifications] = useState(mockNotifications);
  
  // Filter modules by feature flags and permissions
  const featuredModules = getFeaturedModules().filter(module => 
    isFeatureEnabled(module.featureFlag)
  );
  
  const citizenModules = getModulesByCategory('Cidadão').filter(module => 
    isFeatureEnabled(module.featureFlag)
  );
  
  // Mark notification as read
  const markAsRead = (id: number) => {
    setNotifications(notifications.map(notification => 
      notification.id === id ? { ...notification, read: true } : notification
    ));
  };
  
  // Mark all notifications as read
  const markAllAsRead = () => {
    setNotifications(notifications.map(notification => ({
      ...notification,
      read: true
    })));
  };
  
  // Simulate loading user data
  useEffect(() => {
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 500);
    
    return () => clearTimeout(timer);
  }, []);
  
  if (isLoading) {
    return (
      <MainLayout>
        <div className="flex items-center justify-center min-h-[60vh]">
          <LoadingSpinner size="lg" />
        </div>
      </MainLayout>
    );
  }
  
  // Calculate unread notifications
  const unreadCount = notifications.filter(n => !n.read).length;
  
  return (
    <MainLayout>
      {/* Header */}
      <div className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <div className="md:flex md:items-center md:justify-between">
            <div className="flex-1 min-w-0">
              <h1 className="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">
                Olá, {user?.name || 'Cidadão'}
              </h1>
              <p className="mt-1 text-sm text-gray-500">
                Bem-vindo(a) ao seu painel de controle
              </p>
            </div>
            <div className="mt-4 flex md:mt-0 md:ml-4
            ">
              <Button
                variant="outline"
                className="mr-2"
                onClick={() => navigate('/perfil')}
              >
                Meu Perfil
              </Button>
              <Button
                variant="primary"
                onClick={() => navigate('/solicitar')}
              >
                Nova Solicitação
              </Button>
            </div>
          </div>
        </div>
      </div>
      
      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {/* Quick Stats */}
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8">
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <div className="flex items-center">
                <div className="flex-shrink-0 bg-blue-500 rounded-md p-3">
                  <svg className="h-6 w-6 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      Em andamento
                    </dt>
                    <dd className="flex items-baseline">
                      <div className="text-2xl font-semibold text-gray-900">
                        3
                      </div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
          
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <div className="flex items-center">
                <div className="flex-shrink-0 bg-green-500 rounded-md p-3">
                  <svg className="h-6 w-6 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      Concluídos
                    </dt>
                    <dd className="flex items-baseline">
                      <div className="text-2xl font-semibold text-gray-900">
                        12
                      </div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
          
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <div className="flex items-center">
                <div className="flex-shrink-0 bg-yellow-500 rounded-md p-3">
                  <svg className="h-6 w-6 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      Pendentes
                    </dt>
                    <dd className="flex items-baseline">
                      <div className="text-2xl font-semibold text-gray-900">
                        2
                      </div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
          
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <div className="flex items-center">
                <div className="flex-shrink-0 bg-purple-500 rounded-md p-3">
                  <svg className="h-6 w-6 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                  </svg>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      Notificações
                    </dt>
                    <dd className="flex items-baseline">
                      <div className="text-2xl font-semibold text-gray-900">
                        {unreadCount} nova{unreadCount !== 1 ? 's' : ''}
                      </div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Quick Actions */}
          <div className="lg:col-span-2 space-y-6">
            {/* Quick Actions */}
            <div className="bg-white shadow overflow-hidden sm:rounded-lg">
              <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
                <h3 className="text-lg leading-6 font-medium text-gray-900">
                  Ações Rápidas
                </h3>
                <p className="mt-1 max-w-2xl text-sm text-gray-500">
                  Acesse rapidamente os serviços mais utilizados
                </p>
              </div>
              <div className="bg-gray-50 px-4 py-5 sm:p-6">
                <div className="grid grid-cols-2 gap-4">
                  {featuredModules.map((module) => (
                    <button
                      key={module.id}
                      onClick={() => navigate(module.path)}
                      className="inline-flex items-center justify-center px-4 py-3 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                    >
                      {module.icon}
                      <span className="ml-2">{module.name}</span>
                    </button>
                  ))}
                </div>
              </div>
            </div>
            
            {/* Recent Activities */}
            <div className="bg-white shadow overflow-hidden sm:rounded-lg">
              <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg leading-6 font-medium text-gray-900">
                    Atividades Recentes
                  </h3>
                  <button
                    type="button"
                    className="text-sm font-medium text-primary-600 hover:text-primary-500"
                    onClick={() => navigate('/atividades')}
                  >
                    Ver todas
                  </button>
                </div>
              </div>
              <div className="divide-y divide-gray-200">
                {mockRecentActivities.map((activity) => (
                  <div key={activity.id} className="px-4 py-4 sm:px-6 hover:bg-gray-50">
                    <div className="flex items-center">
                      <div className="flex-shrink-0">
                        <div className="h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center">
                          <svg className="h-6 w-6 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                          </svg>
                        </div>
                      </div>
                      <div className="ml-4 flex-1">
                        <div className="flex items-center justify-between">
                          <p className="text-sm font-medium text-gray-900 truncate">
                            {activity.title}
                          </p>
                          <div className="ml-2 flex-shrink-0 flex">
                            <p className="text-xs text-gray-500">{activity.date}</p>
                          </div>
                        </div>
                        <p className="text-sm text-gray-500">
                          Status: <span className="font-medium">{activity.status}</span>
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
          
          {/* Right Column - Notifications */}
          <div className="space-y-6">
            {/* Notifications */}
            <div className="bg-white shadow overflow-hidden sm:rounded-lg">
              <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg leading-6 font-medium text-gray-900">
                    Notificações
                    {unreadCount > 0 && (
                      <span className="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                        {unreadCount}
                      </span>
                    )}
                  </h3>
                  <button
                    type="button"
                    className="text-sm font-medium text-primary-600 hover:text-primary-500"
                    onClick={markAllAsRead}
                  >
                    Marcar todas como lidas
                  </button>
                </div>
              </div>
              <div className="divide-y divide-gray-200">
                {notifications.map((notification) => (
                  <div 
                    key={notification.id} 
                    className={`px-4 py-4 sm:px-6 ${!notification.read ? 'bg-blue-50' : 'bg-white'} hover:bg-gray-50`}
                    onClick={() => markAsRead(notification.id)}
                  >
                    <div className="flex">
                      <div className="flex-shrink-0">
                        {notification.type === 'success' && (
                          <div className="h-8 w-8 rounded-full bg-green-100 flex items-center justify-center">
                            <svg className="h-5 w-5 text-green-600" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                            </svg>
                          </div>
                        )}
                        {notification.type === 'info' && (
                          <div className="h-8 w-8 rounded-full bg-blue-100 flex items-center justify-center">
                            <svg className="h-5 w-5 text-blue-600" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h2a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                            </svg>
                          </div>
                        )}
                        {notification.type === 'document' && (
                          <div className="h-8 w-8 rounded-full bg-yellow-100 flex items-center justify-center">
                            <svg className="h-5 w-5 text-yellow-600" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                              <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clipRule="evenodd" />
                            </svg>
                          </div>
                        )}
                      </div>
                      <div className="ml-3 flex-1">
                        <p className="text-sm font-medium text-gray-900">
                          {notification.title}
                        </p>
                        <p className="mt-1 text-sm text-gray-500">
                          {notification.message}
                        </p>
                        <p className="mt-1 text-xs text-gray-400">
                          {notification.date}
                        </p>
                      </div>
                      {!notification.read && (
                        <div className="ml-4 flex-shrink-0">
                          <span className="h-2 w-2 rounded-full bg-blue-500"></span>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
                {notifications.length === 0 && (
                  <div className="px-4 py-5 sm:px-6 text-center">
                    <p className="text-sm text-gray-500">
                      Nenhuma notificação encontrada
                    </p>
                  </div>
                )}
              </div>
              <div className="px-4 py-4 sm:px-6 border-t border-gray-200 text-center">
                <button
                  type="button"
                  className="text-sm font-medium text-primary-600 hover:text-primary-500"
                  onClick={() => navigate('/notificacoes')}
                >
                  Ver todas as notificações
                </button>
              </div>
            </div>
            
            {/* Quick Links */}
            <div className="bg-white shadow overflow-hidden sm:rounded-lg">
              <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
                <h3 className="text-lg leading-6 font-medium text-gray-900">
                  Links Rápidos
                </h3>
              </div>
              <div className="px-4 py-5 sm:p-6">
                <ul className="space-y-3">
                  <li>
                    <a href="#" className="text-sm font-medium text-primary-600 hover:text-primary-500 flex items-center">
                      <svg className="h-5 w-5 text-gray-400 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                      Meus Documentos
                    </a>
                  </li>
                  <li>
                    <a href="#" className="text-sm font-medium text-primary-600 hover:text-primary-500 flex items-center">
                      <svg className="h-5 w-5 text-gray-400 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                      Meus Agendamentos
                    </a>
                  </li>
                  <li>
                    <a href="#" className="text-sm font-medium text-primary-600 hover:text-primary-500 flex items-center">
                      <svg className="h-5 w-5 text-gray-400 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      Meus Pagamentos
                    </a>
                  </li>
                  <li>
                    <a href="#" className="text-sm font-medium text-primary-600 hover:text-primary-500 flex items-center">
                      <svg className="h-5 w-5 text-gray-400 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      </svg>
                      Configurações
                    </a>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </main>
    </MainLayout>
  );
};

export default CitizenDashboard;

