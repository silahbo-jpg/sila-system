import React, { useState, useEffect, lazy, Suspense } from 'react';
import { Routes, Route, Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { MainLayout } from '../../layouts/MainLayout';
import Button from '../../components/ui/Button';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import api from '../../services/api';

// Subpáginas do módulo
const AgendamentoPage = lazy(() => import('./health/AgendamentoPage'));
const ConsultasPage = lazy(() => import('./health/ConsultasPage'));
const VacinasPage = lazy(() => import('./health/VacinasPage'));

const SaudePage: React.FC = () => {
  const { isAuthenticated, user } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [isLoading, setIsLoading] = useState(false);

  const services = [
    {
      id: 'agendamento',
      name: 'Agendar Consulta',
      description: 'Agende consultas médicas e exames',
      icon: '🏥',
      path: '/saude/agendamento',
      requiresAuth: true
    },
    {
      id: 'consultas',
      name: 'Minhas Consultas',
      description: 'Visualize histórico e próximas consultas',
      icon: '📋',
      path: '/saude/consultas',
      requiresAuth: true
    },
    {
      id: 'vacinas',
      name: 'Carteira de Vacinação',
      description: 'Acesse sua carteira de vacinação digital',
      icon: '💉',
      path: '/saude/vacinas',
      requiresAuth: true
    },
    {
      id: 'emergencia',
      name: 'Emergência',
      description: 'Informações de emergência e contatos',
      icon: '🚨',
      path: '/saude/emergencia',
      requiresAuth: false
    },
    {
      id: 'farmacias',
      name: 'Farmácias Populares',
      description: 'Localize farmácias e medicamentos gratuitos',
      icon: '💊',
      path: '/saude/farmacias',
      requiresAuth: false
    },
    {
      id: 'exames',
      name: 'Resultados de Exames',
      description: 'Consulte resultados de exames laboratoriais',
      icon: '🔬',
      path: '/saude/exames',
      requiresAuth: true
    }
  ];

  const handleServiceClick = (service: any) => {
    if (service.requiresAuth && !isAuthenticated) {
      navigate('/login', {
        state: {
          from: service.path,
          serviceAction: true,
          message: 'Faça login para acessar este serviço'
        }
      });
      return;
    }
    navigate(service.path);
  };

  return (
    <MainLayout>
      <div className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between">
            <div className="flex-1 min-w-0">
              <nav className="flex" aria-label="Breadcrumb">
                <ol className="flex items-center space-x-2">
                  <li>
                    <Link 
                      to="/" 
                      className="text-sm font-medium text-gray-500 hover:text-gray-700"
                    >
                      Início
                    </Link>
                  </li>
                  <li>
                    <div className="flex items-center">
                      <svg className="flex-shrink-0 h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                      </svg>
                      <span className="ml-2 text-sm font-medium text-gray-500">
                        Saúde
                      </span>
                    </div>
                  </li>
                </ol>
              </nav>
              <h1 className="mt-2 text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">
                Serviços de Saúde
              </h1>
              <p className="mt-1 text-sm text-gray-500">
                Agendamentos, consultas e serviços de saúde municipal
              </p>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Serviços disponíveis */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {services.map((service) => (
            <div
              key={service.id}
              className="bg-white overflow-hidden shadow rounded-lg border border-gray-200 hover:shadow-md transition-shadow duration-200 cursor-pointer"
              onClick={() => handleServiceClick(service)}
            >
              <div className="px-4 py-5 sm:p-6">
                <div className="flex items-center">
                  <div className="flex-shrink-0 bg-red-100 rounded-md p-3">
                    <span className="text-2xl">{service.icon}</span>
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <h3 className="text-lg font-medium text-gray-900">
                      {service.name}
                    </h3>
                    <p className="mt-1 text-sm text-gray-500">
                      {service.description}
                    </p>
                    <div className="mt-4">
                      <Button 
                        variant="outline"
                        size="sm"
                        className="w-full"
                      >
                        Acessar
                      </Button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Informações adicionais */}
        <div className="mt-12 grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="bg-red-50 border border-red-200 rounded-lg p-6">
            <h3 className="text-lg font-medium text-red-900 mb-4">
              Como funciona
            </h3>
            <ul className="space-y-3 text-sm text-red-800">
              <li className="flex items-start">
                <svg className="h-5 w-5 text-red-600 mr-2 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                Escolha o serviço de saúde
              </li>
              <li className="flex items-start">
                <svg className="h-5 w-5 text-red-600 mr-2 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                Agende sua consulta ou exame
              </li>
              <li className="flex items-start">
                <svg className="h-5 w-5 text-red-600 mr-2 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                Receba confirmação por SMS/email
              </li>
              <li className="flex items-start">
                <svg className="h-5 w-5 text-red-600 mr-2 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                Acompanhe seu histórico de saúde
              </li>
            </ul>
          </div>

          <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
            <h3 className="text-lg font-medium text-blue-900 mb-4">
              Documentos necessários
            </h3>
            <ul className="space-y-2 text-sm text-blue-800">
              <li className="flex items-center">
                <svg className="h-4 w-4 text-blue-600 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                Bilhete de Identidade (BI)
              </li>
              <li className="flex items-center">
                <svg className="h-4 w-4 text-blue-600 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                Cartão de Saúde (se disponível)
              </li>
              <li className="flex items-center">
                <svg className="h-4 w-4 text-blue-600 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                Comprovante de residência
              </li>
              <li className="flex items-center">
                <svg className="h-4 w-4 text-blue-600 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                Carteira de vacinação
              </li>
            </ul>
          </div>
        </div>

        {/* Informações de emergência */}
        <div className="mt-8 bg-yellow-50 border border-yellow-200 rounded-lg p-6">
          <h3 className="text-lg font-medium text-yellow-900 mb-4">
            🚨 Emergências
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-yellow-800">
            <div className="flex items-center">
              <svg className="h-5 w-5 text-yellow-600 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z" />
              </svg>
              <span><strong>Ambulância:</strong> 113</span>
            </div>
            <div className="flex items-center">
              <svg className="h-5 w-5 text-yellow-600 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z" />
              </svg>
              <span><strong>Bombeiros:</strong> 115</span>
            </div>
            <div className="flex items-center">
              <svg className="h-5 w-5 text-yellow-600 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z" />
              </svg>
              <span><strong>Polícia:</strong> 114</span>
            </div>
          </div>
        </div>
      </div>

      {/* Rotas do módulo */}
      <Suspense fallback={<LoadingSpinner size="lg" />}>
        <Routes>
          <Route path="/agendamento/*" element={<AgendamentoPage />} />
          <Route path="/consultas/*" element={<ConsultasPage />} />
          <Route path="/vacinas/*" element={<VacinasPage />} />
        </Routes>
      </Suspense>
    </MainLayout>
  );
};

export default SaudePage; 
