import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { MainLayout } from '../../layouts/MainLayout';
import { Button } from '../../components/ui/Button';
import { LoadingSpinner } from '../../components/common/LoadingSpinner';
import { toast } from 'react-hot-toast';

// Mock data - in a real app, this would come from an API
const mockStats = {
  totalUsers: 1245,
  activeUsers: 987,
  pendingRequests: 42,
  revenue: 12500,
};

const recentActivities = [
  { id: 1, user: 'João Silva', action: 'Aprovou documento #12345', time: '2 minutos atrás', type: 'success' },
  { id: 2, user: 'Maria Santos', action: 'Rejeitou solicitação #12346', time: '10 minutos atrás', type: 'error' },
  { id: 3, user: 'Carlos Oliveira', action: 'Atualizou perfil de usuário', time: '30 minutos atrás', type: 'info' },
  { id: 4, user: 'Ana Pereira', action: 'Criou novo usuário', time: '1 hora atrás', type: 'info' },
  { id: 5, user: 'Sistema', action: 'Backup automático realizado com sucesso', time: 'Ontem', type: 'success' },
];

const AdminDashboard: React.FC = () => {
  const { user, hasRole, hasPermission } = useAuth();
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');
  const [stats, setStats] = useState(mockStats);
  
  // Check if user has admin access
  const hasAdminAccess = hasRole('admin') || hasPermission('admin.access');
  
  // Simulate loading data
  useEffect(() => {
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 800);
    
    return () => clearTimeout(timer);
  }, []);
  
  // Redirect if not admin
  useEffect(() => {
    if (!isLoading && !hasAdminAccess) {
      toast.error('Acesso não autorizado');
      navigate('/');
    }
  }, [isLoading, hasAdminAccess, navigate]);
  
  if (isLoading) {
    return (
      <MainLayout>
        <div className="flex items-center justify-center min-h-[60vh]">
          <LoadingSpinner size="lg" />
        </div>
      </MainLayout>
    );
  }
  
  // Admin navigation items
  const adminNav = [
    { name: 'Visão Geral', id: 'overview', icon: 'chart-bar', permission: 'admin.overview' },
    { name: 'Usuários', id: 'users', icon: 'users', permission: 'admin.users' },
    { name: 'Permissões', id: 'permissions', icon: 'key', permission: 'admin.permissions' },
    { name: 'Configurações', id: 'settings', icon: 'cog', permission: 'admin.settings' },
    { name: 'Relatórios', id: 'reports', icon: 'document-report', permission: 'admin.reports' },
    { name: 'Logs', id: 'logs', icon: 'clipboard-list', permission: 'admin.logs' },
  ].filter(item => hasPermission(item.permission));
  
  // Render the active tab content
  const renderTabContent = () => {
    switch (activeTab) {
      case 'overview':
        return <OverviewTab stats={stats} recentActivities={recentActivities} />;
      case 'users':
        return <div className="p-6">Gerenciamento de Usuários</div>;
      case 'permissions':
        return <div className="p-6">Gerenciamento de Permissões</div>;
      case 'settings':
        return <div className="p-6">Configurações do Sistema</div>;
      case 'reports':
        return <div className="p-6">Relatórios do Sistema</div>;
      case 'logs':
        return <div className="p-6">Logs do Sistema</div>;
      default:
        return <OverviewTab stats={stats} recentActivities={recentActivities} />;
    }
  };
  
  return (
    <MainLayout>
      <div className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="md:flex md:items-center md:justify-between">
            <div className="flex-1 min-w-0">
              <h2 className="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">
                Painel Administrativo
              </h2>
              <p className="mt-1 text-sm text-gray-500">
                Gerencie o sistema e visualize métricas importantes
              </p>
            </div>
            <div className="mt-4 flex md:mt-0 md:ml-4
            ">
              <Button
                variant="outline"
                className="mr-2"
                onClick={() => navigate('/')}
              >
                Voltar ao Site
              </Button>
              {hasPermission('admin.settings') && (
                <Button
                  variant="primary"
                  onClick={() => navigate('/admin/settings')}
                >
                  Configurações
                </Button>
              )}
            </div>
          </div>
          
          {/* Admin Navigation */}
          <div className="mt-6">
            <div className="border-b border-gray-200">
              <nav className="-mb-px flex space-x-8 overflow-x-auto">
                {adminNav.map((item) => (
                  <button
                    key={item.id}
                    onClick={() => setActiveTab(item.id)}
                    className={`${activeTab === item.id
                      ? 'border-primary-500 text-primary-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center`}
                  >
                    <svg 
                      className={`mr-2 h-5 w-5 ${activeTab === item.id ? 'text-primary-500' : 'text-gray-400'}`} 
                      xmlns="http://www.w3.org/2000/svg" 
                      fill="none" 
                      viewBox="0 0 24 24" 
                      stroke="currentColor"
                    >
                      {getIconPath(item.icon)}
                    </svg>
                    {item.name}
                  </button>
                ))}
              </nav>
            </div>
          </div>
        </div>
      </div>
      
      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {renderTabContent()}
      </main>
    </MainLayout>
  );
};

// Helper function to get icon paths
const getIconPath = (icon: string) => {
  switch (icon) {
    case 'chart-bar':
      return <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />;
    case 'users':
      return <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />;
    case 'key':
      return <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />;
    case 'cog':
      return <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />;
    case 'document-report':
      return <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />;
    case 'clipboard-list':
      return <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />;
    default:
      return <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 10h16M4 14h16M4 18h16" />;
  }
};

// Tab Components
const OverviewTab = ({ stats, recentActivities }: { stats: any, recentActivities: any[] }) => {
  return (
    <div>
      {/* Stats */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8">
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-blue-500 rounded-md p-3">
                <svg className="h-6 w-6 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Total de Usuários
                  </dt>
                  <dd className="flex items-baseline">
                    <div className="text-2xl font-semibold text-gray-900">
                      {stats.totalUsers.toLocaleString()}
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
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Usuários Ativos
                  </dt>
                  <dd className="flex items-baseline">
                    <div className="text-2xl font-semibold text-gray-900">
                      {stats.activeUsers.toLocaleString()}
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
                    Solicitações Pendentes
                  </dt>
                  <dd className="flex items-baseline">
                    <div className="text-2xl font-semibold text-gray-900">
                      {stats.pendingRequests}
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
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Receita (últimos 30 dias)
                  </dt>
                  <dd className="flex items-baseline">
                    <div className="text-2xl font-semibold text-gray-900">
                      {new Intl.NumberFormat('pt-PT', { style: 'currency', currency: 'EUR' }).format(stats.revenue)}
                    </div>
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Activities */}
        <div className="lg:col-span-2">
          <div className="bg-white shadow overflow-hidden sm:rounded-lg">
            <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
              <h3 className="text-lg leading-6 font-medium text-gray-900">
                Atividades Recentes
              </h3>
              <p className="mt-1 max-w-2xl text-sm text-gray-500">
                Últimas ações realizadas no sistema
              </p>
            </div>
            <div className="bg-white shadow overflow-hidden sm:rounded-b-lg">
              <ul className="divide-y divide-gray-200">
                {recentActivities.map((activity) => (
                  <li key={activity.id} className="px-4 py-4 sm:px-6 hover:bg-gray-50">
                    <div className="flex items-center">
                      <div className={`min-w-0 flex-1 flex items-center`}>
                        <div className={`flex-shrink-0 h-10 w-10 flex items-center justify-center rounded-full ${getActivityColor(activity.type)}`}>
                          {getActivityIcon(activity.type)}
                        </div>
                        <div className="min-w-0 flex-1 px-4">
                          <div>
                            <p className="text-sm font-medium text-gray-900 truncate">
                              {activity.user}
                            </p>
                            <p className="text-sm text-gray-500">
                              {activity.action}
                            </p>
                          </div>
                        </div>
                        <div className="ml-auto">
                          <p className="text-sm text-gray-500">
                            {activity.time}
                          </p>
                        </div>
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
              <div className="bg-gray-50 px-4 py-3 text-right sm:px-6">
                <button
                  type="button"
                  className="text-sm font-medium text-primary-600 hover:text-primary-500"
                >
                  Ver todas as atividades
                </button>
              </div>
            </div>
          </div>
        </div>
        
        {/* Quick Actions */}
        <div>
          <div className="bg-white shadow overflow-hidden sm:rounded-lg">
            <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
              <h3 className="text-lg leading-6 font-medium text-gray-900">
                Ações Rápidas
              </h3>
            </div>
            <div className="px-4 py-5 sm:p-6">
              <div className="space-y-4">
                <Button
                  variant="primary"
                  className="w-full flex items-center justify-center"
                  onClick={() => {}}
                >
                  <svg className="mr-2 h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                  </svg>
                  Adicionar Usuário
                </Button>
                
                <Button
                  variant="outline"
                  className="w-full flex items-center justify-center"
                  onClick={() => {}}
                >
                  <svg className="mr-2 h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                  </svg>
                  Criar Relatório
                </Button>
                
                <Button
                  variant="outline"
                  className="w-full flex items-center justify-center"
                  onClick={() => {}}
                >
                  <svg className="mr-2 h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                  </svg>
                  Fazer Backup
                </Button>
                
                <Button
                  variant="outline"
                  className="w-full flex items-center justify-center"
                  onClick={() => {}}
                >
                  <svg className="mr-2 h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  Configurações do Sistema
                </Button>
              </div>
              
              <div className="mt-6 border-t border-gray-200 pt-6">
                <h4 className="text-sm font-medium text-gray-500 mb-3">Status do Sistema</h4>
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-500">Uso de Disco</span>
                    <div className="w-1/2 bg-gray-200 rounded-full h-2.5">
                      <div className="bg-green-600 h-2.5 rounded-full" style={{ width: '65%' }}></div>
                    </div>
                    <span className="text-sm text-gray-500 ml-2">65%</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-500">Uso de Memória</span>
                    <div className="w-1/2 bg-gray-200 rounded-full h-2.5">
                      <div className="bg-blue-600 h-2.5 rounded-full" style={{ width: '42%' }}></div>
                    </div>
                    <span className="text-sm text-gray-500 ml-2">42%</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-500">Uso de CPU</span>
                    <div className="w-1/2 bg-gray-200 rounded-full h-2.5">
                      <div className="bg-yellow-500 h-2.5 rounded-full" style={{ width: '28%' }}></div>
                    </div>
                    <span className="text-sm text-gray-500 ml-2">28%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Helper functions for activity items
const getActivityColor = (type: string) => {
  switch (type) {
    case 'success':
      return 'bg-green-100 text-green-600';
    case 'error':
      return 'bg-red-100 text-red-600';
    case 'warning':
      return 'bg-yellow-100 text-yellow-600';
    default:
      return 'bg-blue-100 text-blue-600';
  }
};

const getActivityIcon = (type: string) => {
  switch (type) {
    case 'success':
      return (
        <svg className="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
        </svg>
      );
    case 'error':
      return (
        <svg className="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
        </svg>
      );
    case 'warning':
      return (
        <svg className="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
          <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
        </svg>
      );
    default:
      return (
        <svg className="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
          <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h2a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
        </svg>
      );
  }
};

export default AdminDashboard;

