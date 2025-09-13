import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { MainLayout } from '../layouts/MainLayout';
import Button from '../components/ui/Button';
import LoadingSpinner from '../components/common/LoadingSpinner';

interface Service {
  id: string;
  name: string;
  description: string;
  module: string;
  estimatedTime: string;
  requirements: string[];
  documents: string[];
  steps: string[];
  status: 'active' | 'coming-soon' | 'maintenance';
  requiresAuth: boolean;
}

const ServiceDetails: React.FC = () => {
  const { serviceId } = useParams<{ serviceId: string }>();
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();
  
  const [service, setService] = useState<Service | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadService = async () => {
      try {
        setIsLoading(true);
        
        // Simular carregamento do serviço - em produção seria uma API call
        const mockService: Service = {
          id: serviceId || '',
          name: 'Solicitar Certidão de Nascimento',
          description: 'Solicite sua certidão de nascimento de forma rápida e segura, sem sair de casa.',
          module: 'Cidadania',
          estimatedTime: '3-5 dias úteis',
          requirements: [
            'NIF válido',
            'Documento de identificação',
            'Comprovante de residência'
          ],
          documents: [
            'Cópia do RG ou CNH',
            'Comprovante de residência',
            'Formulário preenchido'
          ],
          steps: [
            'Preencher formulário online',
            'Enviar documentos digitalizados',
            'Aguardar validação',
            'Receber certidão por e-mail'
          ],
          status: 'active',
          requiresAuth: true
        };
        
        setService(mockService);
      } catch (error) {
        console.error('Error loading service:', error);
      } finally {
        setIsLoading(false);
      }
    };
    
    loadService();
  }, [serviceId]);

  const handleStartService = () => {
    if (!isAuthenticated) {
      navigate('/login', {
        state: {
          from: `/servico/${serviceId}`,
          serviceAction: true,
          message: 'Faça login para acessar este serviço'
        }
      });
    } else {
      // Redirecionar para o fluxo do serviço
      navigate(`/cidadania/solicitar-certidao`);
    }
  };

  if (isLoading) {
    return (
      <MainLayout>
        <div className="flex items-center justify-center min-h-[60vh]">
          <LoadingSpinner size="lg" />
        </div>
      </MainLayout>
    );
  }

  if (!service) {
    return (
      <MainLayout>
        <div className="max-w-4xl mx-auto px-4 py-12 text-center">
          <div className="bg-red-50 border-l-4 border-red-400 p-4 mb-6">
            <div className="flex">
                              <div className="flex-shrink-0">
                  <svg className="h-5 w-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                  </svg>
                </div>
              <div className="ml-3">
                <p className="text-sm text-red-700">
                  Serviço não encontrado
                </p>
              </div>
            </div>
          </div>
          <Button 
            variant="primary" 
            onClick={() => navigate('/')}
            className="mt-4"
          >
            Voltar para a página inicial
          </Button>
        </div>
      </MainLayout>
    );
  }

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
                      <Link 
                        to={`/modulos/${service.module.toLowerCase()}`}
                        className="ml-2 text-sm font-medium text-gray-500 hover:text-gray-700"
                      >
                        {service.module}
                      </Link>
                    </div>
                  </li>
                  <li>
                    <div className="flex items-center">
                      <svg className="flex-shrink-0 h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                      </svg>
                      <span className="ml-2 text-sm font-medium text-gray-500">
                        {service.name}
                      </span>
                    </div>
                  </li>
                </ol>
              </nav>
              <h1 className="mt-2 text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">
                {service.name}
              </h1>
              <p className="mt-1 text-sm text-gray-500">
                {service.description}
              </p>
            </div>
            <div className="mt-4 flex-shrink-0 flex md:mt-0 md:ml-4">
              <Button 
                variant="primary"
                onClick={handleStartService}
                disabled={service.status !== 'active'}
                className="flex items-center gap-2"
              >
                {isAuthenticated ? 'Iniciar Serviço' : 'Fazer Login para Acessar'}
                <svg className="h-4 w-4 rotate-180" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
              </Button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main content */}
          <div className="lg:col-span-2 space-y-8">
            {/* Service overview */}
            <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-lg font-medium text-gray-900 mb-4">Sobre este serviço</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="flex items-center">
                  <svg className="h-5 w-5 text-gray-400 mr-3" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
                  </svg>
                  <div>
                    <p className="text-sm font-medium text-gray-900">Tempo estimado</p>
                    <p className="text-sm text-gray-500">{service.estimatedTime}</p>
                  </div>
                </div>
                <div className="flex items-center">
                  <svg className="h-5 w-5 text-green-400 mr-3" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  <div>
                    <p className="text-sm font-medium text-gray-900">Status</p>
                    <p className="text-sm text-gray-500 capitalize">
                      {service.status === 'active' ? 'Disponível' : 
                       service.status === 'coming-soon' ? 'Em breve' : 'Em manutenção'}
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Steps */}
            <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-lg font-medium text-gray-900 mb-4">Como funciona</h2>
              <div className="space-y-4">
                {service.steps.map((step, index) => (
                  <div key={index} className="flex items-start">
                    <div className="flex-shrink-0 w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
                      <span className="text-sm font-medium text-primary-600">{index + 1}</span>
                    </div>
                    <div className="ml-4">
                      <p className="text-sm text-gray-900">{step}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Requirements */}
            <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-lg font-medium text-gray-900 mb-4">Requisitos</h2>
              <ul className="space-y-2">
                {service.requirements.map((requirement, index) => (
                  <li key={index} className="flex items-center">
                    <svg className="h-4 w-4 text-green-400 mr-3" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                    <span className="text-sm text-gray-700">{requirement}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Documents */}
            <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-lg font-medium text-gray-900 mb-4">Documentos necessários</h2>
              <ul className="space-y-2">
                {service.documents.map((document, index) => (
                  <li key={index} className="flex items-center">
                    <svg className="h-4 w-4 text-blue-400 mr-3" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clipRule="evenodd" />
                    </svg>
                    <span className="text-sm text-gray-700">{document}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Quick actions */}
            <div className="bg-white shadow rounded-lg p-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Ações rápidas</h3>
              <div className="space-y-3">
                <Button 
                  variant="primary" 
                  onClick={handleStartService}
                  disabled={service.status !== 'active'}
                  className="w-full"
                >
                  {isAuthenticated ? 'Iniciar Serviço' : 'Fazer Login'}
                </Button>
                
                <Button 
                  variant="outline" 
                  onClick={() => navigate(`/modulos/${service.module.toLowerCase()}`)}
                  className="w-full"
                >
                  Ver outros serviços
                </Button>
              </div>
            </div>

            {/* Help */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
              <h3 className="text-lg font-medium text-blue-900 mb-4">Precisa de ajuda?</h3>
              <div className="space-y-3">
                <div className="flex items-center">
                  <svg className="h-4 w-4 text-blue-400 mr-3" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z" />
                  </svg>
                  <span className="text-sm text-blue-700">0800 123 4567</span>
                </div>
                <div className="flex items-center">
                  <svg className="h-4 w-4 text-blue-400 mr-3" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z" />
                    <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" />
                  </svg>
                  <span className="text-sm text-blue-700">suporte@prefeitura.gov.br</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </MainLayout>
  );
};

export default ServiceDetails; 
