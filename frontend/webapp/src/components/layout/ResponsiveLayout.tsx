import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { Button } from '../ui/Button';
import { Logo } from '../common/Logo';
import { useFeatureFlags } from '../../hooks/useFeatureFlags';
import { getModulesByCategory } from '../../data/modules';

interface ResponsiveLayoutProps {
  children: React.ReactNode;
  showSidebar?: boolean;
  onToggleSidebar?: () => void;
}

const ResponsiveLayout: React.FC<ResponsiveLayoutProps> = ({
  children,
  showSidebar = true,
  onToggleSidebar,
}) => {
  const { isAuthenticated, user, logout } = useAuth();
  const { isFeatureEnabled } = useFeatureFlags();
  const location = useLocation();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);
  
  // Get modules for navigation
  const citizenModules = getModulesByCategory('Cidadão').filter(module => 
    isFeatureEnabled(module.featureFlag)
  );
  
  // Handle scroll effect for header
  useEffect(() => {
    const handleScroll = () => {
      const offset = window.scrollY;
      setIsScrolled(offset > 10);
    };
    
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);
  
  // Close mobile menu when location changes
  useEffect(() => {
    setIsMobileMenuOpen(false);
  }, [location]);
  
  // Toggle mobile menu
  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };
  
  // Handle logout
  const handleLogout = () => {
    logout();
    setIsMobileMenuOpen(false);
  };
  
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <header className={`sticky top-0 z-40 transition-shadow duration-200 ${isScrolled ? 'shadow-md' : 'shadow-sm'} bg-white`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              {/* Mobile menu button */}
              <button
                type="button"
                className="inline-flex items-center justify-center p-2 rounded-md text-gray-500 hover:text-gray-600 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-500 lg:hidden"
                aria-controls="mobile-menu"
                aria-expanded="false"
                onClick={toggleMobileMenu}
              >
                <span className="sr-only">Abrir menu principal</span>
                {isMobileMenuOpen ? (
                  <svg className="block h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                ) : (
                  <svg className="block h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                  </svg>
                )}
              </button>
              
              {/* Logo */}
              <div className="flex-shrink-0 flex items-center ml-2 lg:ml-0">
                <Link to="/">
                  <Logo variant="default" size="md" />
                </Link>
              </div>
              
              {/* Desktop Navigation */}
              <nav className="hidden lg:ml-6 lg:flex lg:space-x-8">
                <Link
                  to="/"
                  className={`${location.pathname === '/' ? 'border-primary-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'} inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium`}
                >
                  Início
                </Link>
                {isAuthenticated && (
                  <Link
                    to="/dashboard"
                    className={`${location.pathname.startsWith('/dashboard') ? 'border-primary-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'} inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium`}
                  >
                    Meu Painel
                  </Link>
                )}
                <Link
                  to="/servicos"
                  className={`${location.pathname.startsWith('/servicos') ? 'border-primary-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'} inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium`}
                >
                  Serviços
                </Link>
                <Link
                  to="/ajuda"
                  className={`${location.pathname.startsWith('/ajuda') ? 'border-primary-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'} inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium`}
                >
                  Ajuda
                </Link>
              </nav>
            </div>
            
            {/* Desktop Profile Dropdown */}
            <div className="hidden lg:ml-4 lg:flex lg:items-center">
              {isAuthenticated ? (
                <div className="ml-4 relative flex-shrink-0">
                  <div className="flex items-center">
                    <div className="text-right mr-3">
                      <p className="text-sm font-medium text-gray-700">{user?.name || 'Usuário'}</p>
                      <p className="text-xs text-gray-500">{user?.role || 'Cidadão'}</p>
                    </div>
                    <div className="relative">
                      <button
                        type="button"
                        className="bg-white rounded-full flex text-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                        id="user-menu-button"
                        aria-expanded="false"
                        aria-haspopup="true"
                        onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                      >
                        <span className="sr-only">Abrir menu de usuário</span>
                        <div className="h-8 w-8 rounded-full bg-primary-100 flex items-center justify-center text-primary-700 font-medium">
                          {user?.name ? user.name.charAt(0).toUpperCase() : 'U'}
                        </div>
                      </button>
                      
                      {/* Dropdown menu */}
                      {isMobileMenuOpen && (
                        <div className="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg py-1 bg-white ring-1 ring-black ring-opacity-5 focus:outline-none z-50">
                          <Link
                            to="/perfil"
                            className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                          >
                            Meu Perfil
                          </Link>
                          <Link
                            to="/configuracoes"
                            className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                          >
                            Configurações
                          </Link>
                          <button
                            onClick={handleLogout}
                            className="w-full text-left block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                          >
                            Sair
                          </button>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ) : (
                <div className="flex items-center space-x-4">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => navigate('/login', { state: { from: location.pathname } })}
                  >
                    Entrar
                  </Button>
                  <Button
                    variant="primary"
                    size="sm"
                    onClick={() => navigate('/registro')}
                  >
                    Criar Conta
                  </Button>
                </div>
              )}
            </div>
          </div>
        </div>
        
        {/* Mobile menu */}
        <div className={`lg:hidden ${isMobileMenuOpen ? 'block' : 'hidden'}`} id="mobile-menu">
          <div className="pt-2 pb-3 space-y-1 bg-white">
            <Link
              to="/"
              className={`${location.pathname === '/' ? 'bg-primary-50 border-primary-500 text-primary-700' : 'border-transparent text-gray-600 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-800'} block pl-3 pr-4 py-2 border-l-4 text-base font-medium`}
            >
              Início
            </Link>
            {isAuthenticated && (
              <Link
                to="/dashboard"
                className={`${location.pathname.startsWith('/dashboard') ? 'bg-primary-50 border-primary-500 text-primary-700' : 'border-transparent text-gray-600 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-800'} block pl-3 pr-4 py-2 border-l-4 text-base font-medium`}
              >
                Meu Painel
              </Link>
            )}
            <Link
              to="/servicos"
              className={`${location.pathname.startsWith('/servicos') ? 'bg-primary-50 border-primary-500 text-primary-700' : 'border-transparent text-gray-600 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-800'} block pl-3 pr-4 py-2 border-l-4 text-base font-medium`}
            >
              Serviços
            </Link>
            <Link
              to="/ajuda"
              className={`${location.pathname.startsWith('/ajuda') ? 'bg-primary-50 border-primary-500 text-primary-700' : 'border-transparent text-gray-600 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-800'} block pl-3 pr-4 py-2 border-l-4 text-base font-medium`}
            >
              Ajuda
            </Link>
            
            {/* Mobile modules list */}
            {isAuthenticated && citizenModules.length > 0 && (
              <div className="pt-2">
                <div className="px-3 py-2 text-xs font-semibold text-gray-500 uppercase tracking-wider">
                  Meus Serviços
                </div>
                {citizenModules.map((module) => (
                  <Link
                    key={module.id}
                    to={module.path}
                    className="group flex items-center px-3 py-2 text-base font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50"
                  >
                    <span className="mr-3">
                      {module.icon}
                    </span>
                    {module.name}
                  </Link>
                ))}
              </div>
            )}
          </div>
          
          {/* Mobile auth actions */}
          <div className="pt-4 pb-3 border-t border-gray-200">
            {isAuthenticated ? (
              <div className="flex items-center px-4">
                <div className="flex-shrink-0">
                  <div className="h-10 w-10 rounded-full bg-primary-100 flex items-center justify-center text-primary-700 font-medium">
                    {user?.name ? user.name.charAt(0).toUpperCase() : 'U'}
                  </div>
                </div>
                <div className="ml-3">
                  <div className="text-base font-medium text-gray-800">{user?.name || 'Usuário'}</div>
                  <div className="text-sm font-medium text-gray-500">{user?.email || ''}</div>
                </div>
              </div>
            ) : (
              <div className="px-4 space-y-3">
                <Button
                  variant="primary"
                  className="w-full justify-center"
                  onClick={() => {
                    setIsMobileMenuOpen(false);
                    navigate('/login', { state: { from: location.pathname } });
                  }}
                >
                  Entrar
                </Button>
                <p className="text-center text-sm text-gray-600">
                  Não tem uma conta?{' '}
                  <button
                    onClick={() => {
                      setIsMobileMenuOpen(false);
                      navigate('/registro');
                    }}
                    className="font-medium text-primary-600 hover:text-primary-500"
                  >
                    Cadastre-se
                  </button>
                </p>
              </div>
            )}
            
            {isAuthenticated && (
              <div className="mt-3 space-y-1">
                <Link
                  to="/perfil"
                  className="block px-4 py-2 text-base font-medium text-gray-500 hover:text-gray-800 hover:bg-gray-100"
                >
                  Meu Perfil
                </Link>
                <Link
                  to="/configuracoes"
                  className="block px-4 py-2 text-base font-medium text-gray-500 hover:text-gray-800 hover:bg-gray-100"
                >
                  Configurações
                </Link>
                <button
                  onClick={handleLogout}
                  className="w-full text-left block px-4 py-2 text-base font-medium text-gray-500 hover:text-gray-800 hover:bg-gray-100"
                >
                  Sair
                </button>
              </div>
            )}
          </div>
        </div>
      </header>
      
      {/* Main Content */}
      <div className="flex flex-1">
        {/* Sidebar */}
        {showSidebar && isAuthenticated && (
          <div className="hidden lg:flex lg:flex-shrink-0">
            <div className="flex flex-col w-64 border-r border-gray-200 bg-white">
              <div className="h-0 flex-1 flex flex-col pt-5 pb-4 overflow-y-auto">
                {/* Sidebar Navigation */}
                <nav className="mt-5 flex-1 px-2 space-y-1">
                  <SidebarLink
                    to="/dashboard"
                    icon={
                      <svg className="mr-3 h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                      </svg>
                    }
                    label="Visão Geral"
                    isActive={location.pathname === '/dashboard'}
                  />
                  
                  <SidebarSection title="Meus Serviços" />
                  
                  {citizenModules.map((module) => (
                    <SidebarLink
                      key={module.id}
                      to={module.path}
                      icon={module.icon}
                      label={module.name}
                      isActive={location.pathname.startsWith(module.path)}
                    />
                  ))}
                  
                  <SidebarSection title="Minha Conta" />
                  
                  <SidebarLink
                    to="/perfil"
                    icon={
                      <svg className="mr-3 h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                      </svg>
                    }
                    label="Meu Perfil"
                    isActive={location.pathname.startsWith('/perfil')}
                  />
                  
                  <SidebarLink
                    to="/documentos"
                    icon={
                      <svg className="mr-3 h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                    }
                    label="Meus Documentos"
                    isActive={location.pathname.startsWith('/documentos')}
                  />
                  
                  <SidebarLink
                    to="/configuracoes"
                    icon={
                      <svg className="mr-3 h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      </svg>
                    }
                    label="Configurações"
                    isActive={location.pathname.startsWith('/configuracoes')}
                  />
                </nav>
              </div>
              
              {/* Sidebar Footer */}
              <div className="flex-shrink-0 flex border-t border-gray-200 p-4">
                <div className="flex-shrink-0 group block">
                  <div className="flex items-center">
                    <div>
                      <div className="h-9 w-9 rounded-full bg-primary-100 flex items-center justify-center text-primary-700 font-medium">
                        {user?.name ? user.name.charAt(0).toUpperCase() : 'U'}
                      </div>
                    </div>
                    <div className="ml-3">
                      <p className="text-sm font-medium text-gray-700 group-hover:text-gray-900">
                        {user?.name || 'Usuário'}
                      </p>
                      <button
                        onClick={handleLogout}
                        className="text-xs font-medium text-gray-500 group-hover:text-gray-700"
                      >
                        Sair
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
        
        {/* Main Content Area */}
        <div className="flex flex-col w-0 flex-1 overflow-hidden">
          {/* Mobile header toggle */}
          {showSidebar && isAuthenticated && (
            <div className="lg:hidden pl-1 pt-1 sm:pl-3 sm:pt-3">
              <button
                type="button"
                className="-ml-0.5 -mt-0.5 h-12 inline-flex items-center justify-center rounded-md text-gray-500 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-500"
                onClick={onToggleSidebar}
              >
                <span className="sr-only">Abrir menu lateral</span>
                <svg className="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
            </div>
          )}
          
          {/* Page Content */}
          <main className="flex-1 relative z-0 overflow-y-auto focus:outline-none">
            <div className="py-6">
              <div className="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
                {children}
              </div>
            </div>
          </main>
        </div>
      </div>
      
      {/* Footer */}
      <footer className="bg-white border-t border-gray-200">
        <div className="max-w-7xl mx-auto py-6 px-4 overflow-hidden sm:px-6 lg:px-8">
          <nav className="-mx-5 -my-2 flex flex-wrap justify-center" aria-label="Footer">
            <div className="px-5 py-2">
              <a href="#" className="text-base text-gray-500 hover:text-gray-900">
                Sobre
              </a>
            </div>
            <div className="px-5 py-2">
              <a href="#" className="text-base text-gray-500 hover:text-gray-900">
                Termos de Uso
              </a>
            </div>
            <div className="px-5 py-2">
              <a href="#" className="text-base text-gray-500 hover:text-gray-900">
                Privacidade
              </a>
            </div>
            <div className="px-5 py-2">
              <a href="#" className="text-base text-gray-500 hover:text-gray-900">
                Contato
              </a>
            </div>
            <div className="px-5 py-2">
              <a href="#" className="text-base text-gray-500 hover:text-gray-900">
                Ajuda
              </a>
            </div>
          </nav>
          <p className="mt-8 text-center text-base text-gray-400">
            &copy; {new Date().getFullYear()} Administração Municipal de Huambo. Todos os direitos reservados.
          </p>
        </div>
      </footer>
    </div>
  );
};

// Sidebar Link Component
const SidebarLink: React.FC<{
  to: string;
  icon: React.ReactNode;
  label: string;
  isActive: boolean;
}> = ({ to, icon, label, isActive }) => (
  <Link
    to={to}
    className={`${isActive ? 'bg-primary-50 border-primary-500 text-primary-700' : 'border-transparent text-gray-600 hover:bg-gray-50 hover:text-gray-900'} group flex items-center px-2 py-2 text-sm font-medium border-l-4`}
  >
    <span className={`${isActive ? 'text-primary-500' : 'text-gray-400 group-hover:text-gray-500'} mr-3`}>
      {icon}
    </span>
    {label}
  </Link>
);

// Sidebar Section Title Component
const SidebarSection: React.FC<{ title: string }> = ({ title }) => (
  <div className="px-2 pt-5 pb-2">
    <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider">
      {title}
    </h3>
  </div>
);

export default ResponsiveLayout;

