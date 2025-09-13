import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { MainLayout } from '../layouts/MainLayout';
import { getModuleById, Module } from '../data/modules';
import Button from '../components/ui/Button';
import LoadingSpinner from '../components/common/LoadingSpinner';
import { useFeatureFlags } from '../hooks/useFeatureFlags';

const ModulePage: React.FC = () => {
  const { moduleId } = useParams<{ moduleId: string }>();
  const navigate = useNavigate();
  const { isAuthenticated, user } = useAuth();
  const { isFeatureEnabled } = useFeatureFlags();
  
  const [module, setModule] = useState<Module | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadModule = async () => {
      try {
        setIsLoading(true);
        
        // In a real app, this would be an API call to fetch module details
        // const response = await fetch(`/api/modules/${moduleId}`);
        // const data = await response.json();
        
        // For now, use the static data
        const foundModule = getModuleById(moduleId || '');
        
        if (!foundModule) {
          setError('Módulo não encontrado');
          return;
        }
        
        // Check if module is enabled via feature flag
        if (!isFeatureEnabled(foundModule.featureFlag)) {
          setError('Este módulo não está disponível no momento');
          return;
        }
        
        setModule(foundModule);
      } catch (err) {
        console.error('Error loading module:', err);
        setError('Ocorreu um erro ao carregar o módulo');
      } finally {
        setIsLoading(false);
      }
    };
    
    loadModule();
  }, [moduleId, isFeatureEnabled]);

  const handleActionClick = (path: string, requiresAuth: boolean = true) => {
    if (requiresAuth && !isAuthenticated) {
      // Redirect to login with return URL
      navigate('/login', { 
        state: { 
          from: path,
          message: 'Por favor, faça login para acessar este serviço'
        } 
      });
      return;
    }
    
    navigate(path);
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

  if (error || !module) {
    return (
      <MainLayout>
        <div className="max-w-4xl mx-auto px-4 py-12 text-center">
          <div className="bg-red-50 border-l-4 border-red-400 p-4 mb-6">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-red-700">
                  {error || 'Módulo não encontrado'}
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

  const { name, description, icon, status, submodules } = module;
  const isModuleDisabled = status !== 'active';

  return (
    <MainLayout>
      <div className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between">
            <div className="flex-1 min-w-0">
              <nav className="flex" aria-label="Breadcrumb">
                <ol className="flex items-center space-x-2">
                  <li>
                    <div className="flex">
                      <Link 
                        to="/" 
                        className="text-sm font-medium text-gray-500 hover:text-gray-700"
                      >
                        Início
                      </Link>
                    </div>
                  </li>
                  <li>
                    <div className="flex items-center">
                      <svg 
                        className="flex-shrink-0 h-5 w-5 text-gray-400" 
                        xmlns="http://www.w3.org/2000/svg" 
                        viewBox="0 0 20 20" 
                        fill="currentColor"
                      >
                        <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                      </svg>
                      <span className="ml-2 text-sm font-medium text-gray-500">
                        {name}
                      </span>
                    </div>
                  </li>
                </ol>
              </nav>
              <h1 className="mt-2 text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">
                {name}
              </h1>
              <p className="mt-1 text-sm text-gray-500">
                {description}
              </p>
            </div>
            <div className="mt-4 flex-shrink-0 flex md:mt-0 md:ml-4">
              {isModuleDisabled ? (
                <span className="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-gray-700 bg-gray-100 cursor-not-allowed">
                  {status === 'coming-soon' ? 'Em Breve' : 
                   status === 'beta' ? 'Versão Beta' : 
                   'Em Manutenção'}
                </span>
              ) : (
                <Button 
                  variant="primary"
                  onClick={() => handleActionClick(module.path)}
                  disabled={isModuleDisabled}
                >
                  Acessar {name}
                </Button>
              )}
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {submodules && submodules.length > 0 ? (
          <div>
            <h2 className="text-lg font-medium text-gray-900 mb-4">
              Serviços disponíveis
            </h2>
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {submodules.map((submodule) => (
                <div 
                  key={submodule.id}
                  className="bg-white overflow-hidden shadow rounded-lg border border-gray-200 hover:shadow-md transition-shadow duration-200"
                >
                  <div className="px-4 py-5 sm:p-6">
                    <div className="flex items-center">
                      <div className="flex-shrink-0 bg-primary-100 rounded-md p-3">
                        {submodule.icon}
                      </div>
                      <div className="ml-5 w-0 flex-1">
                        <h3 className="text-lg font-medium text-gray-900">
                          {submodule.name}
                        </h3>
                        <p className="mt-1 text-sm text-gray-500">
                          {submodule.description}
                        </p>
                        <div className="mt-4">
                          <Button 
                            variant="outline"
                            size="sm"
                            onClick={() => handleActionClick(submodule.path)}
                            disabled={isModuleDisabled}
                            className={`${isModuleDisabled ? 'opacity-50 cursor-not-allowed' : ''}`}
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
          </div>
        ) : (
          <div className="bg-white shadow overflow-hidden sm:rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <h3 className="text-lg leading-6 font-medium text-gray-900">
                Sobre este módulo
              </h3>
              <div className="mt-2 max-w-xl text-sm text-gray-500">
                <p>
                  Este módulo está em desenvolvimento. Em breve você poderá acessar todos os serviços relacionados a {name.toLowerCase()}.
                </p>
              </div>
              <div className="mt-5">
                <Button 
                  variant="primary"
                  onClick={() => navigate('/')}
                >
                  Voltar para a página inicial
                </Button>
              </div>
            </div>
          </div>
        )}
      </div>
    </MainLayout>
  );
};

export default ModulePage;

