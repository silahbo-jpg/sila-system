import React, { useState, useEffect } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { Button } from '../ui/Button';
import { Logo } from '../common/Logo';
import { Menu, X, ChevronDown } from 'lucide-react';

interface NavItem {
  name: string;
  path: string;
  icon?: React.ReactNode;
  children?: NavItem[];
  requiresAuth?: boolean;
  roles?: string[];
}

interface ResponsiveNavProps {
  items: NavItem[];
  className?: string;
}

const ResponsiveNav: React.FC<ResponsiveNavProps> = ({ items, className = '' }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [openSubmenu, setOpenSubmenu] = useState<string | null>(null);
  const location = useLocation();
  const navigate = useNavigate();
  const { isAuthenticated, user, logout } = useAuth();
  
  // Close mobile menu when location changes
  useEffect(() => {
    setIsOpen(false);
    setOpenSubmenu(null);
  }, [location]);
  
  // Toggle mobile menu
  const toggleMenu = () => {
    setIsOpen(!isOpen);
    if (!isOpen) {
      setOpenSubmenu(null);
    }
  };
  
  // Toggle submenu
  const toggleSubmenu = (path: string) => {
    setOpenSubmenu(openSubmenu === path ? null : path);
  };
  
  // Check if user has required role for nav item
  const hasRequiredRole = (roles?: string[]) => {
    if (!roles || roles.length === 0) return true;
    if (!user?.role) return false;
    return roles.includes(user.role);
  };
  
  // Filter nav items based on auth and roles
  const filteredItems = items.filter(item => {
    if (item.requiresAuth && !isAuthenticated) return false;
    if (item.roles && !hasRequiredRole(item.roles)) return false;
    return true;
  });
  
  // Render desktop navigation
  const renderDesktopNav = () => (
    <div className="hidden lg:flex lg:space-x-8">
      {filteredItems.map((item) => (
        <div key={item.path} className="relative group">
          <div className="flex items-center">
            <Link
              to={item.path}
              className={`${
                location.pathname === item.path
                  ? 'text-primary-600 border-primary-500'
                  : 'text-gray-700 hover:text-gray-900 border-transparent hover:border-gray-300'
              } inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium`}
            >
              {item.icon && <span className="mr-2">{item.icon}</span>}
              {item.name}
            </Link>
            {item.children && item.children.length > 0 && (
              <button
                onClick={() => toggleSubmenu(item.path)}
                className="ml-1 p-1 rounded-md text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <ChevronDown className="h-4 w-4" />
              </button>
            )}
          </div>
          
          {/* Desktop dropdown */}
          {item.children && item.children.length > 0 && (
            <div 
              className={`absolute z-10 left-0 mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 focus:outline-none transition-all duration-200 ${
                openSubmenu === item.path ? 'opacity-100 visible' : 'opacity-0 invisible'
              }`}
            >
              <div className="py-1">
                {item.children.map((child) => (
                  <Link
                    key={child.path}
                    to={child.path}
                    className={`${
                      location.pathname === child.path
                        ? 'bg-gray-100 text-gray-900'
                        : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
                    } block px-4 py-2 text-sm`}
                  >
                    {child.name}
                  </Link>
                ))}
              </div>
            </div>
          )}
        </div>
      ))}
    </div>
  );
  
  // Render mobile navigation
  const renderMobileNav = () => (
    <div className={`lg:hidden ${isOpen ? 'block' : 'hidden'}`}>
      <div className="pt-2 pb-3 space-y-1">
        {filteredItems.map((item) => (
          <div key={item.path}>
            <div className="flex items-center">
              <Link
                to={item.path}
                className={`${
                  location.pathname === item.path
                    ? 'bg-primary-50 border-primary-500 text-primary-700'
                    : 'border-transparent text-gray-600 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-800'
                } flex-1 block pl-3 pr-4 py-2 border-l-4 text-base font-medium`}
              >
                <div className="flex items-center">
                  {item.icon && <span className="mr-3">{item.icon}</span>}
                  {item.name}
                </div>
              </Link>
              {item.children && item.children.length > 0 && (
                <button
                  onClick={() => toggleSubmenu(item.path)}
                  className="p-2 mr-2 rounded-md text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500"
                >
                  <ChevronDown 
                    className={`h-5 w-5 transition-transform duration-200 ${
                      openSubmenu === item.path ? 'transform rotate-180' : ''
                    }`} 
                  />
                </button>
              )}
            </div>
            
            {/* Mobile submenu */}
            {item.children && item.children.length > 0 && (
              <div 
                className={`pl-8 overflow-hidden transition-all duration-300 ${
                  openSubmenu === item.path ? 'max-h-96' : 'max-h-0'
                }`}
              >
                {item.children.map((child) => (
                  <Link
                    key={child.path}
                    to={child.path}
                    className={`${
                      location.pathname === child.path
                        ? 'bg-gray-100 text-gray-900'
                        : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                    } block pl-3 pr-4 py-2 text-base font-medium border-l-2 border-gray-200`}
                  >
                    {child.name}
                  </Link>
                ))}
              </div>
            )}
          </div>
        ))}
        
        {/* Auth buttons for mobile */}
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
            <div className="space-y-3 px-2">
              <Button
                variant="primary"
                className="w-full justify-center"
                onClick={() => navigate('/login', { state: { from: location.pathname } })}
              >
                Entrar
              </Button>
              <p className="text-center text-sm text-gray-600">
                Não tem uma conta?{' '}
                <button
                  onClick={() => navigate('/registro')}
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
                onClick={logout}
                className="w-full text-left block px-4 py-2 text-base font-medium text-gray-500 hover:text-gray-800 hover:bg-gray-100"
              >
                Sair
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
  
  return (
    <nav className={`bg-white shadow-sm ${className}`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            {/* Mobile menu button */}
            <button
              type="button"
              className="lg:hidden inline-flex items-center justify-center p-2 rounded-md text-gray-500 hover:text-gray-600 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-500"
              aria-controls="mobile-menu"
              aria-expanded={isOpen}
              onClick={toggleMenu}
            >
              <span className="sr-only">Abrir menu principal</span>
              {isOpen ? (
                <X className="block h-6 w-6" aria-hidden="true" />
              ) : (
                <Menu className="block h-6 w-6" aria-hidden="true" />
              )}
            </button>
            
            {/* Logo */}
            <div className="flex-shrink-0 flex items-center ml-2 lg:ml-0">
              <Link to="/">
                <Logo variant="default" size="md" />
              </Link>
            </div>
            
            {/* Desktop Navigation */}
            {renderDesktopNav()}
          </div>
          
          {/* Desktop auth buttons */}
          <div className="hidden lg:ml-6 lg:flex lg:items-center">
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
                      onClick={() => setOpenSubmenu(openSubmenu === 'user' ? null : 'user')}
                    >
                      <span className="sr-only">Abrir menu de usuário</span>
                      <div className="h-8 w-8 rounded-full bg-primary-100 flex items-center justify-center text-primary-700 font-medium">
                        {user?.name ? user.name.charAt(0).toUpperCase() : 'U'}
                      </div>
                    </button>
                    
                    {/* User dropdown menu */}
                    {openSubmenu === 'user' && (
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
                          onClick={logout}
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
      {renderMobileNav()}
    </nav>
  );
};

export default ResponsiveNav;

