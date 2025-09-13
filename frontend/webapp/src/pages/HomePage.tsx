import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { ModuleCard } from '../components/modules/ModuleCard';
import { MainLayout } from '../layouts/MainLayout';
import { modules } from '../data/modules';
import Button from '../components/ui/Button';
import { useFeatureFlags } from '../hooks/useFeatureFlags';

const HomePage: React.FC = () => {
  const { isAuthenticated, user } = useAuth();
  const navigate = useNavigate();
  const { isFeatureEnabled } = useFeatureFlags();

  // Redirect to dashboard if already authenticated
  useEffect(() => {
    if (isAuthenticated && user) {
      if (user.role === 'admin' || user.role === 'manager' || user.role === 'auditor') {
        navigate('/admin/dashboard');
      } else {
        navigate('/dashboard');
      }
    }
  }, [isAuthenticated, user, navigate]);

  const handleModuleClick = (moduleId: string) => {
    navigate(`/modulos/${moduleId}`);
  };

  return (
    <MainLayout>
      <div className="container mx-auto px-4 py-8">
        {/* Hero Section */}
        <section className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">Bem-vindo ao Portal do Cidadão</h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Acesse serviços públicos de forma rápida, simples e segura, sem sair de casa.
          </p>
          
          <div className="mt-8">
            <p className="text-lg text-gray-600 mb-4">
              Explore os serviços disponíveis e faça login apenas quando necessário
            </p>
          </div>
        </section>

        {/* Featured Services */}
        <section className="mb-16">
          <h2 className="text-2xl font-semibold mb-6">Serviços em Destaque</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {modules
              .filter(module => module.featured)
              .map(module => (
                <ModuleCard 
                  key={module.id}
                  title={module.name}
                  description={module.description}
                  icon={module.icon}
                  onClick={() => handleModuleClick(module.id)}
                  className="h-full"
                />
              ))}
          </div>
        </section>

        {/* All Services */}
        <section>
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-semibold">Todos os Serviços</h2>
            <div className="relative">
              <input
                type="text"
                placeholder="Buscar serviço..."
                className="px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
              <span className="absolute right-3 top-2.5 text-gray-400">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </span>
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {modules
              .filter(module => isFeatureEnabled(module.featureFlag))
              .map(module => (
                <ModuleCard 
                  key={module.id}
                  title={module.name}
                  description={module.description}
                  icon={module.icon}
                  status={module.status}
                  onClick={() => handleModuleClick(module.id)}
                  className="h-full"
                />
              ))}
          </div>
        </section>

        {/* Help Section */}
        <section className="mt-16 bg-gray-50 rounded-xl p-8 text-center">
          <h2 className="text-2xl font-semibold mb-4">Precisa de ajuda?</h2>
          <p className="text-gray-600 mb-6 max-w-2xl mx-auto">
            Nossa equipe está pronta para te ajudar com qualquer dúvida ou problema que você possa ter.
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <Button variant="outline" className="flex items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
              </svg>
              Fale Conosco
            </Button>
            <Button variant="outline" className="flex items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Central de Ajuda
            </Button>
          </div>
        </section>
      </div>
    </MainLayout>
  );
};

export default HomePage;

