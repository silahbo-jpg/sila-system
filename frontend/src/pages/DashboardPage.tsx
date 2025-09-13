import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { 
  ChartBarIcon,
  DocumentCheckIcon,
  ClockIcon,
  UserGroupIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
  XCircleIcon,
  ArrowTrendingUpIcon,
  MapPinIcon,
  BellIcon,
  Cog6ToothIcon,
  EyeIcon
} from '@heroicons/react/24/outline';

interface DashboardStats {
  totalServices: number;
  activeServices: number;
  pendingRequests: number;
  completedToday: number;
  totalCitizens: number;
  averageProcessingTime: string;
}

interface RecentActivity {
  id: string;
  type: 'service_request' | 'approval' | 'completion' | 'error';
  title: string;
  description: string;
  timestamp: string;
  status: 'pending' | 'approved' | 'completed' | 'rejected';
  municipality?: string;
}

interface ServicePerformance {
  id: string;
  name: string;
  requests: number;
  completionRate: number;
  avgProcessingTime: string;
  trend: 'up' | 'down' | 'stable';
}

const DashboardPage: React.FC = () => {
  const { t, i18n } = useTranslation();
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [recentActivity, setRecentActivity] = useState<RecentActivity[]>([]);
  const [servicePerformance, setServicePerformance] = useState<ServicePerformance[]>([]);
  const [selectedMunicipality, setSelectedMunicipality] = useState('all');
  const [timeRange, setTimeRange] = useState('7d');
  const [isLoading, setIsLoading] = useState(true);

  const municipalities = [
    'Huambo', 'Bailundo', 'Bimbe', 'Ecunha', 'Caála', 'Cuima', 
    'Cachiungo', 'Galanga', 'Londuimbali', 'Alto Hama', 'Longonjo', 
    'Chilata', 'Mungo', 'Chinjenje', 'Chicala-Cholohanga', 'Sambo', 'Ucuma'
  ];

  useEffect(() => {
    const loadDashboardData = async () => {
      setIsLoading(true);

      // Mock data - in production, this would come from API
      const mockStats: DashboardStats = {
        totalServices: 150,
        activeServices: 142,
        pendingRequests: 234,
        completedToday: 67,
        totalCitizens: 12847,
        averageProcessingTime: '3.2 dias'
      };

      const mockActivity: RecentActivity[] = [
        {
          id: '1',
          type: 'service_request',
          title: 'Nova solicitação de Certidão de Nascimento',
          description: 'Cidadão João Silva solicitou certidão de nascimento',
          timestamp: '2025-01-15T10:30:00Z',
          status: 'pending',
          municipality: 'Huambo'
        },
        {
          id: '2',
          type: 'completion',
          title: 'Licença Comercial aprovada',
          description: 'Licença para Empresa ABC Lda foi aprovada',
          timestamp: '2025-01-15T09:15:00Z',
          status: 'completed',
          municipality: 'Bailundo'
        },
        {
          id: '3',
          type: 'approval',
          title: 'Documento aprovado pelo supervisor',
          description: 'Alvará de construção foi aprovado',
          timestamp: '2025-01-15T08:45:00Z',
          status: 'approved',
          municipality: 'Caála'
        },
        {
          id: '4',
          type: 'error',
          title: 'Erro no processamento',
          description: 'Falha na validação de documento NIF',
          timestamp: '2025-01-15T08:00:00Z',
          status: 'rejected',
          municipality: 'Huambo'
        }
      ];

      const mockPerformance: ServicePerformance[] = [
        {
          id: '1',
          name: 'Registo de Nascimento',
          requests: 145,
          completionRate: 94,
          avgProcessingTime: '2.1 dias',
          trend: 'up'
        },
        {
          id: '2',
          name: 'Licença Comercial',
          requests: 89,
          completionRate: 87,
          avgProcessingTime: '5.3 dias',
          trend: 'stable'
        },
        {
          id: '3',
          name: 'Certidão de Casamento',
          requests: 67,
          completionRate: 92,
          avgProcessingTime: '3.8 dias',
          trend: 'up'
        },
        {
          id: '4',
          name: 'Alvará de Construção',
          requests: 34,
          completionRate: 76,
          avgProcessingTime: '8.2 dias',
          trend: 'down'
        }
      ];

      setTimeout(() => {
        setStats(mockStats);
        setRecentActivity(mockActivity);
        setServicePerformance(mockPerformance);
        setIsLoading(false);
      }, 1000);
    };

    loadDashboardData();
  }, [selectedMunicipality, timeRange]);

  const getActivityIcon = (type: RecentActivity['type']) => {
    switch (type) {
      case 'service_request': return DocumentCheckIcon;
      case 'approval': return CheckCircleIcon;
      case 'completion': return CheckCircleIcon;
      case 'error': return XCircleIcon;
      default: return DocumentCheckIcon;
    }
  };

  const getActivityColor = (type: RecentActivity['type']) => {
    switch (type) {
      case 'service_request': return 'text-blue-500';
      case 'approval': return 'text-green-500';
      case 'completion': return 'text-green-500';
      case 'error': return 'text-red-500';
      default: return 'text-gray-500';
    }
  };

  const getStatusColor = (status: RecentActivity['status']) => {
    switch (status) {
      case 'pending': return 'bg-yellow-100 text-yellow-800';
      case 'approved': return 'bg-green-100 text-green-800';
      case 'completed': return 'bg-green-100 text-green-800';
      case 'rejected': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getTrendIcon = (trend: ServicePerformance['trend']) => {
    return trend === 'up' ? '↗️' : trend === 'down' ? '↘️' : '➡️';
  };

  const formatRelativeTime = (timestamp: string) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    
    if (diffHours < 1) return t('dashboard.activity.justNow');
    if (diffHours < 24) return t('dashboard.activity.hoursAgo', { hours: diffHours });
    
    const diffDays = Math.floor(diffHours / 24);
    return t('dashboard.activity.daysAgo', { days: diffDays });
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-sila-primary mx-auto"></div>
          <p className="mt-4 text-gray-600">{t('common.loading')}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              {t('dashboard.title')}
            </h1>
            <p className="text-gray-600">
              {t('dashboard.subtitle')}
            </p>
          </div>
          
          <div className="mt-4 sm:mt-0 flex space-x-4">
            <select
              value={selectedMunicipality}
              onChange={(e) => setSelectedMunicipality(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-md focus:ring-sila-primary focus:border-sila-primary"
            >
              <option value="all">{t('dashboard.filters.allMunicipalities')}</option>
              {municipalities.map(municipality => (
                <option key={municipality} value={municipality}>
                  {municipality}
                </option>
              ))}
            </select>
            
            <select
              value={timeRange}
              onChange={(e) => setTimeRange(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-md focus:ring-sila-primary focus:border-sila-primary"
            >
              <option value="24h">{t('dashboard.filters.last24h')}</option>
              <option value="7d">{t('dashboard.filters.last7d')}</option>
              <option value="30d">{t('dashboard.filters.last30d')}</option>
              <option value="90d">{t('dashboard.filters.last90d')}</option>
            </select>
          </div>
        </div>

        {/* Stats Cards */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-6 mb-8">
            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="flex items-center">
                <ChartBarIcon className="w-8 h-8 text-blue-500" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500">{t('dashboard.stats.totalServices')}</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.totalServices}</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="flex items-center">
                <CheckCircleIcon className="w-8 h-8 text-green-500" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500">{t('dashboard.stats.activeServices')}</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.activeServices}</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="flex items-center">
                <ClockIcon className="w-8 h-8 text-yellow-500" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500">{t('dashboard.stats.pendingRequests')}</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.pendingRequests}</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="flex items-center">
                <DocumentCheckIcon className="w-8 h-8 text-purple-500" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500">{t('dashboard.stats.completedToday')}</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.completedToday}</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="flex items-center">
                <UserGroupIcon className="w-8 h-8 text-indigo-500" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500">{t('dashboard.stats.totalCitizens')}</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.totalCitizens.toLocaleString()}</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="flex items-center">
                <ArrowTrendingUpIcon className="w-8 h-8 text-orange-500" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500">{t('dashboard.stats.avgProcessingTime')}</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.averageProcessingTime}</p>
                </div>
              </div>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Recent Activity */}
          <div className="bg-white rounded-lg shadow-sm">
            <div className="p-6 border-b border-gray-200">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-semibold text-gray-900">
                  {t('dashboard.recentActivity.title')}
                </h2>
                <button className="text-sila-primary hover:text-sila-secondary text-sm font-medium">
                  {t('dashboard.recentActivity.viewAll')}
                </button>
              </div>
            </div>
            <div className="p-6">
              <div className="space-y-4">
                {recentActivity.map((activity) => {
                  const Icon = getActivityIcon(activity.type);
                  return (
                    <div key={activity.id} className="flex items-start space-x-3">
                      <Icon className={`w-5 h-5 mt-0.5 ${getActivityColor(activity.type)}`} />
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center justify-between">
                          <p className="text-sm font-medium text-gray-900">
                            {activity.title}
                          </p>
                          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(activity.status)}`}>
                            {t(`dashboard.status.${activity.status}`)}
                          </span>
                        </div>
                        <p className="text-sm text-gray-500 mt-1">
                          {activity.description}
                        </p>
                        <div className="flex items-center space-x-2 mt-2 text-xs text-gray-400">
                          {activity.municipality && (
                            <>
                              <MapPinIcon className="w-3 h-3" />
                              <span>{activity.municipality}</span>
                              <span>•</span>
                            </>
                          )}
                          <span>{formatRelativeTime(activity.timestamp)}</span>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>

          {/* Service Performance */}
          <div className="bg-white rounded-lg shadow-sm">
            <div className="p-6 border-b border-gray-200">
              <h2 className="text-lg font-semibold text-gray-900">
                {t('dashboard.servicePerformance.title')}
              </h2>
            </div>
            <div className="p-6">
              <div className="space-y-4">
                {servicePerformance.map((service) => (
                  <div key={service.id} className="flex items-center justify-between">
                    <div className="flex-1">
                      <div className="flex items-center justify-between mb-1">
                        <h3 className="text-sm font-medium text-gray-900">
                          {service.name}
                        </h3>
                        <span className="text-sm text-gray-500">
                          {getTrendIcon(service.trend)} {service.completionRate}%
                        </span>
                      </div>
                      <div className="flex items-center space-x-4 text-xs text-gray-500">
                        <span>{service.requests} {t('dashboard.servicePerformance.requests')}</span>
                        <span>•</span>
                        <span>{service.avgProcessingTime}</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                        <div 
                          className="bg-sila-primary h-2 rounded-full" 
                          style={{ width: `${service.completionRate}%` }}
                        ></div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="mt-8 bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            {t('dashboard.quickActions.title')}
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <button className="flex items-center justify-center p-4 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors duration-200">
              <BellIcon className="w-5 h-5 text-gray-600 mr-2" />
              <span className="text-sm font-medium text-gray-700">
                {t('dashboard.quickActions.notifications')}
              </span>
            </button>
            
            <button className="flex items-center justify-center p-4 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors duration-200">
              <EyeIcon className="w-5 h-5 text-gray-600 mr-2" />
              <span className="text-sm font-medium text-gray-700">
                {t('dashboard.quickActions.reports')}
              </span>
            </button>
            
            <button className="flex items-center justify-center p-4 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors duration-200">
              <UserGroupIcon className="w-5 h-5 text-gray-600 mr-2" />
              <span className="text-sm font-medium text-gray-700">
                {t('dashboard.quickActions.users')}
              </span>
            </button>
            
            <button className="flex items-center justify-center p-4 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors duration-200">
              <Cog6ToothIcon className="w-5 h-5 text-gray-600 mr-2" />
              <span className="text-sm font-medium text-gray-700">
                {t('dashboard.quickActions.settings')}
              </span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;