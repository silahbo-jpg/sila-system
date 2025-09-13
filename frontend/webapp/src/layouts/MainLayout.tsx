import * as React from 'react';
import { useState, useEffect } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import Button from '../components/ui/Button';
import Logo from '../components/common/Logo';
import SyncStatusBar from '../components/mobile/SyncStatusBar';
import LanguageSelector from '../components/LanguageSelector';

type NavItem = {
  name: string;
  path: string;
  icon: React.ReactNode;
  requiresAuth?: boolean;
  roles?: string[];
};

const mainNavItems: NavItem[] = [
  { 
    name: 'Início', 
    path: '/', 
    icon: (
      <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
      </svg>
    )
  },
  { 
    name: 'Serviços', 
    path: '/servicos', 
    icon: (
      <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
      </svg>
    )
  },
  { 
    name: 'Meu Perfil', 
    path: '/perfil', 
    requiresAuth: true,
    icon: (
      <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
      </svg>
    )
  },
  { 
    name: 'Área do Cidadão', 
    path: '/dashboard', 
    requiresAuth: true,
    icon: (
      <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
      </svg>
    )
  },
];

const adminNavItems: NavItem[] = [
  { 
    name: 'Painel de Controle', 
    path: '/admin/dashboard', 
    roles: ['admin', 'manager'],
    icon: (
      <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
      </svg>
    )
  },
  { 
    name: 'Administração', 
    path: '/admin', 
    roles: ['admin'],
    icon: (
      <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
      </svg>
    )
  },
];

interface MainLayoutProps {
  children: React.ReactNode;
  showHeader?: boolean;
  showFooter?: boolean;
  className?: string;
}

export const MainLayout: React.FC<MainLayoutProps> = ({
  children,
  showHeader = true,
  showFooter = true,
  className = '',
}: MainLayoutProps) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const { isAuthenticated, user, logout } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();
  const isAdminRoute = location.pathname.startsWith('/admin');
  
  // Close mobile menu when route changes
  useEffect(() => {
    setMobileMenuOpen(false);
  }, [location]);

  // Filter navigation items based on auth status and user role
  const filteredNavItems = (isAdminRoute ? adminNavItems : mainNavItems).filter(item => {
    // Show all items if not requiring auth
    if (!item.requiresAuth && !item.roles) return true;
    
    // Hide if not authenticated
    if (!isAuthenticated) return false;
    
    // Check user role if specified
    if (item.roles && user?.role) {
      return item.roles.includes(user.role);
    }
    
    return true;
  });

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      {/* Header */}
      {showHeader && (
        <header className="bg-white shadow-sm sticky top-0 z-10">
          <div className="page-container">
            <div className="flex justify-between h-16">
              <div className="flex items-center">
                {/* Mobile menu button */}
                <button
                  type="button"
                  className="md:hidden inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-500 transition-colors"
                  onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                >
                  <span className="sr-only">Abrir menu</span>
                  {mobileMenuOpen ? (
                    <svg className="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  ) : (
                    <svg className="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                    </svg>
                  )}
                </button>
                
                {/* Logo */}
                <div className="flex-shrink-0 flex items-center">
                  <Link to="/">
                    <Logo className="h-8 w-auto" />
                  </Link>
                </div>
                
                {/* Desktop Navigation */}
                <nav className="hidden md:ml-6 md:flex md:space-x-8">
                  {filteredNavItems.map((item) => {
                    const isActive = location.pathname === item.path || 
                                  (item.path !== '/' && location.pathname.startsWith(item.path));
                    
                    return (
                      <Link
                        key={item.path}
                        to={item.path}
                        className={`
                          inline-flex items-center px-3 py-2 border-b-2 text-sm font-medium transition-colors
                          ${
                            isActive
                              ? 'border-primary-500 text-gray-900'
                              : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
                          }
                        `}
                      >
                        <span className="mr-2">{item.icon}</span>
                        {item.name}
                      </Link>
                    );
                  })}
                </nav>
              </div>
              
              {/* Right side items */}
              <div className="hidden md:ml-4 md:flex-shrink-0 md:flex md:items-center md:space-x-4">
                <LanguageSelector />
                
                {isAuthenticated ? (
                  <div className="flex items-center space-x-4">
                    <Link 
                      to="/perfil" 
                      className="flex items-center text-sm text-gray-700 hover:text-gray-900 transition-colors"
                    >
                      <span className="mr-2">
                        {user?.avatar ? (
                          <img 
                            className="h-8 w-8 rounded-full object-cover border border-gray-200" 
                            src={user.avatar} 
                            alt={user.name} 
                          />
                        ) : (
                          <div className="h-8 w-8 rounded-full bg-primary-100 flex items-center justify-center text-primary-600 shadow-sm">
                            {user?.name?.charAt(0) || 'U'}
                          </div>
                        )}
                      </span>
                      <span className="hidden lg:inline font-medium">{user?.name || 'Usuário'}</span>
                    </Link>
                    <Button 
                      variant="angola-secondary" 
                      size="sm" 
                      onClick={handleLogout}
                      className="transition-colors"
                    >
                      Sair
                    </Button>
                  </div>
                ) : (
                  <div className="flex items-center space-x-4">
                    <Button 
                      variant="angola-secondary" 
                      size="sm" 
                      onClick={() => navigate('/login')}
                      className="transition-colors"
                    >
                      Entrar
                    </Button>
                    <Button 
                      variant="angola-primary" 
                      size="sm" 
                      onClick={() => navigate('/cadastro')}
                      className="shadow-sm hover:shadow transition-all"
                    >
                      Cadastre-se
                    </Button>
                  </div>
                )}
              </div>
            </div>
          </div>
                    {/* Language Selector for Mobile */}
                {mobileMenuOpen && (
                  <div className="md:hidden px-4 py-3 border-t border-gray-200">
                    <div className="mb-2 font-medium text-sm text-gray-500">Idioma</div>
                    <LanguageSelector />
                  </div>
                )}
                
                {/* Mobile menu */}
                {mobileMenuOpen && (
                  <div className="md:hidden shadow-sm">
                    <div className="pt-2 pb-3 space-y-1">
                      {filteredNavItems.map((item) => (
                        <Link
                          key={item.path}
                          to={item.path}
                          className={`
                            group flex items-center px-4 py-2.5 text-base font-medium rounded-md transition-colors
                            ${
                              location.pathname === item.path
                                ? 'bg-primary-50 border-l-4 border-primary-500 text-primary-700'
                                : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900 border-l-4 border-transparent hover:border-gray-300'
                            }
                          `}
                        >
                          <span className="mr-4 text-gray-500 group-hover:text-gray-600">{item.icon}</span>
                          {item.name}
                        </Link>
                      ))}
                      
                      {isAuthenticated ? (
                        <div className="pt-4 pb-3 border-t border-gray-200">
                          <div className="flex items-center px-4 py-2">
                            <div className="flex-shrink-0">
                              {user?.avatar ? (
                                <img 
                                  className="h-10 w-10 rounded-full object-cover border border-gray-200" 
                                  src={user.avatar} 
                                  alt={user.name} 
                                />
                              ) : (
                                <div className="h-10 w-10 rounded-full bg-primary-100 flex items-center justify-center text-primary-600 shadow-sm">
                                  {user?.name?.charAt(0) || 'U'}
                                </div>
                              )}
                            </div>
                      <div className="ml-3">
                        <div className="text-base font-medium text-gray-800">
                          {user?.name || 'Usuário'}
                        </div>
                        <div className="text-sm font-medium text-gray-500">
                          {user?.email || ''}
                        </div>
                      </div>
                    </div>
                    <div className="mt-3 space-y-1">
                      <button
                        onClick={handleLogout}
                        className="block w-full text-left px-4 py-2 text-base font-medium text-gray-500 hover:text-gray-800 hover:bg-gray-100"
                      >
                        Sair
                      </button>
                    </div>
                  </div>
                ) : (
                  <div className="px-3 py-4 space-y-3">
                    <Button 
                      variant="angola-primary" 
                      block
                      onClick={() => navigate('/login')}
                    >
                      Entrar
                    </Button>
                    <p className="text-center text-sm text-gray-600">
                      Novo por aqui?{' '}
                      <button 
                        onClick={() => navigate('/cadastro')}
                        className="font-medium text-primary-600 hover:text-primary-500"
                      >
                        Crie uma conta
                      </button>
                    </p>
                  </div>
                )}
              </div>
            </div>
          )}
        </header>
      )}

      {/* Main Content */}
      <main className="flex-1">
        <div className={`${className || ''}`}>
          {children}
        </div>
      </main>

      {/* Footer */}
      {showFooter && (
        <footer className="bg-white border-t border-gray-200 mt-auto">
          <div className="page-container py-8 md:py-12">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div>
                <h3 className="text-base font-semibold mb-4 text-gray-900">SILA - HUAMBO</h3>
                <p className="text-sm text-gray-600">
                  SILA - Sistema Integrado Local de Administração.
                  Desenvolvido para tornar os serviços mais acessíveis e transparentes.
                </p>
              </div>

              <div>
                <h3 className="text-base font-semibold mb-4 text-gray-900">Links Rápidos</h3>
                <ul className="space-y-2">
                  <li>
                    <Link to="/sobre" className="text-sm text-gray-600 hover:text-primary-600 transition-colors">
                      Sobre Nós
                    </Link>
                  </li>
                  <li>
                    <Link to="/termos" className="text-sm text-gray-600 hover:text-primary-600 transition-colors">
                      Termos de Uso
                    </Link>
                  </li>
                  <li>
                    <Link to="/contato" className="text-sm text-gray-600 hover:text-primary-600 transition-colors">
                      Contato
                    </Link>
                  </li>
                  <li>
                    <Link to="/ajuda" className="text-sm text-gray-600 hover:text-primary-600 transition-colors">
                      Ajuda
                    </Link>
                  </li>
                </ul>
              </div>

              <div>
                <h3 className="text-base font-semibold mb-4 text-gray-900">Suporte</h3>
                <p className="text-sm text-gray-600 mb-2">
                  Precisa de ajuda? Entre em contato conosco:
                </p>
                <p className="text-sm text-gray-600">
                  Email: suporte@sila.gov.ao
                </p>
                <p className="text-sm text-gray-600">
                  Tel/WhatsApp: 926880397
                </p>
              </div>
            </div>

            <div className="mt-8 pt-6 border-t border-gray-200 flex flex-col md:flex-row justify-between items-center">
              <p className="text-sm text-gray-500">
                &copy; {new Date().getFullYear()} Administração Municipal de Huambo. Todos os direitos reservados.
              </p>
              <div className="mt-4 md:mt-0 flex space-x-6">
                <a href="#" className="text-gray-400 hover:text-gray-500 transition-colors">
                  <span className="sr-only">Facebook</span>
                  <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path fillRule="evenodd" d="M22 12c0-5.523-4.477-10-10-10S2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12z" clipRule="evenodd" />
                  </svg>
                </a>
                <a href="#" className="text-gray-400 hover:text-gray-500 transition-colors">
                  <span className="sr-only">Twitter</span>
                  <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84" />
                  </svg>
                </a>
                <a href="#" className="text-gray-400 hover:text-gray-500 transition-colors">
                  <span className="sr-only">Instagram</span>
                  <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path fillRule="evenodd" d="M12.315 2c2.43 0 2.784.013 3.808.06 1.064.049 1.791.218 2.427.465a4.902 4.902 0 011.772 1.153 4.902 4.902 0 011.153 1.772c.247.636.416 1.363.465 2.427.048 1.067.06 1.407.06 4.123v.08c0 2.643-.012 2.987-.06 4.043-.049 1.064-.218 1.791-.465 2.427a4.902 4.902 0 01-1.153 1.772 4.902 4.902 0 01-1.772 1.153c-.636.247-1.363.416-2.427.465-1.067.048-1.407.06-4.123.06h-.08c-2.643 0-2.987-.012-4.043-.06-1.064-.049-1.791-.218-2.427-.465a4.902 4.902 0 01-1.772-1.153 4.902 4.902 0 01-1.153-1.772c-.247-.636-.416-1.363-.465-2.427-.047-1.024-.06-1.379-.06-3.808v-.63c0-2.43.013-2.784.06-3.808.049-1.064.218-1.791.465-2.427a4.902 4.902 0 011.153-1.772A4.902 4.902 0 015.45 2.525c.636-.247 1.363-.416 2.427-.465C8.901 2.013 9.256 2 11.685 2h.63zm-.081 1.802h-.468c-2.456 0-2.784.011-3.807.058-.975.045-1.504.207-1.857.344-.467.182-.8.398-1.15.748-.35.35-.566.683-.748 1.15-.137.353-.3.882-.344 1.857-.047 1.023-.058 1.351-.058 3.807v.468c0 2.456.011 2.784.058 3.807.045.975.207 1.504.344 1.857.182.466.399.8.748 1.15.35.35.683.566 1.15.748.353.137.882.3 1.857.344 1.054.048 1.37.058 4.041.058h.08c2.597 0 2.917-.01 3.96-.058.976-.045 1.505-.207 1.858-.344.466-.182.8-.398 1.15-.748.35-.35.566-.683.748-1.15.137-.353.3-.882.344-1.857.048-1.055.058-1.37.058-4.041v-.08c0-2.597-.01-2.917-.058-3.96-.045-.976-.207-1.505-.344-1.858a3.097 3.097 0 00-.748-1.15 3.098 3.098 0 00-1.15-.748c-.353-.137-.882-.3-1.857-.344-1.023-.047-1.351-.058-3.807-.058zM12 6.865a5.135 5.135 0 110 10.27 5.135 5.135 0 010-10.27zm0 1.802a3.333 3.333 0 100 6.666 3.333 3.333 0 000-6.666zm5.338-3.205a1.2 1.2 0 110 2.4 1.2 1.2 0 010-2.4z" clipRule="evenodd" />
                  </svg>
                </a>
              </div>
            </div>
          </div>
          <SyncStatusBar />
        </footer>
      )}
    </div>
  );
};

export default MainLayout;

