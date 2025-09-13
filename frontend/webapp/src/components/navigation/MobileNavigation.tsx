import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import Button from '../ui/Button';

const MobileNavigation: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const { isAuthenticated, user, logout } = useAuth();
  const location = useLocation();

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  const closeMenu = () => {
    setIsOpen(false);
  };

  const handleLogout = () => {
    logout();
    closeMenu();
  };

  return (
    <div className="lg:hidden">
      {/* Hamburger button */}
      <button
        onClick={toggleMenu}
        className="p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500"
      >
        <span className="sr-only">Abrir menu</span>
        <svg
          className={`${isOpen ? 'hidden' : 'block'} h-6 w-6`}
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
        </svg>
        <svg
          className={`${isOpen ? 'block' : 'hidden'} h-6 w-6`}
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>

      {/* Mobile menu */}
      <div className={`${isOpen ? 'block' : 'hidden'} fixed inset-0 z-50 lg:hidden`}>
        <div 
          className="fixed inset-0 bg-gray-600 bg-opacity-75" 
          onClick={closeMenu}
          role="button"
          tabIndex={0}
          onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && closeMenu()}
          aria-label="Fechar menu de navegação"
          style={{ cursor: 'pointer' }}
        ></div>
        
        <div className="fixed inset-y-0 right-0 flex w-full max-w-xs flex-col bg-white shadow-xl">
          <div className="flex h-16 items-center justify-between px-4 sm:px-6">
            <h2 className="text-lg font-medium text-gray-900">Menu</h2>
            <button
              onClick={closeMenu}
              className="p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100"
            >
              <span className="sr-only">Fechar menu</span>
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <div className="flex-1 overflow-y-auto">
            <nav className="px-4 py-6 space-y-6">
              {/* User info */}
              {isAuthenticated && user && (
                <div className="border-b border-gray-200 pb-4">
                  <div className="flex items-center">
                    <div className="h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center">
                      <span className="text-sm font-medium text-blue-600">
                        {user.name.charAt(0).toUpperCase()}
                      </span>
                    </div>
                    <div className="ml-3">
                      <p className="text-sm font-medium text-gray-900">{user.name}</p>
                      <p className="text-xs text-gray-500">{user.email}</p>
                    </div>
                  </div>
                </div>
              )}

              {/* Navigation links */}
              <div className="space-y-2">
                <Link
                  to="/"
                  onClick={closeMenu}
                  className={`block px-3 py-2 rounded-md text-base font-medium ${
                    location.pathname === '/' 
                      ? 'bg-blue-100 text-blue-700' 
                      : 'text-gray-700 hover:bg-gray-50'
                  }`}
                >
                  Início
                </Link>

                {isAuthenticated ? (
                  <>
                    <Link
                      to="/dashboard"
                      onClick={closeMenu}
                      className={`block px-3 py-2 rounded-md text-base font-medium ${
                        location.pathname === '/dashboard' 
                          ? 'bg-blue-100 text-blue-700' 
                          : 'text-gray-700 hover:bg-gray-50'
                      }`}
                    >
                      Meu Painel
                    </Link>
                    
                    <Link
                      to="/perfil"
                      onClick={closeMenu}
                      className={`block px-3 py-2 rounded-md text-base font-medium ${
                        location.pathname === '/perfil' 
                          ? 'bg-blue-100 text-blue-700' 
                          : 'text-gray-700 hover:bg-gray-50'
                      }`}
                    >
                      Meu Perfil
                    </Link>
                  </>
                ) : (
                  <>
                    <Link
                      to="/login"
                      onClick={closeMenu}
                      className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:bg-gray-50"
                    >
                      Entrar
                    </Link>
                    
                    <Link
                      to="/registro"
                      onClick={closeMenu}
                      className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:bg-gray-50"
                    >
                      Criar Conta
                    </Link>
                  </>
                )}

                {/* Admin link */}
                {(user?.role === 'admin' || user?.role === 'manager' || user?.role === 'auditor') && (
                  <Link
                    to="/admin/dashboard"
                    onClick={closeMenu}
                    className={`block px-3 py-2 rounded-md text-base font-medium ${
                      location.pathname.startsWith('/admin') 
                        ? 'bg-blue-100 text-blue-700' 
                        : 'text-gray-700 hover:bg-gray-50'
                    }`}
                  >
                    Painel Administrativo
                  </Link>
                )}
              </div>

              {/* Quick actions */}
              {isAuthenticated && (
                <div className="border-t border-gray-200 pt-4">
                  <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
                    Ações Rápidas
                  </h3>
                  <div className="space-y-2">
                    <Link
                      to="/cidadania"
                      onClick={closeMenu}
                      className="block px-3 py-2 rounded-md text-sm text-gray-700 hover:bg-gray-50"
                    >
                      Serviços de Cidadania
                    </Link>
                    <Link
                      to="/educacao"
                      onClick={closeMenu}
                      className="block px-3 py-2 rounded-md text-sm text-gray-700 hover:bg-gray-50"
                    >
                      Serviços de Educação
                    </Link>
                    <Link
                      to="/saude"
                      onClick={closeMenu}
                      className="block px-3 py-2 rounded-md text-sm text-gray-700 hover:bg-gray-50"
                    >
                      Serviços de Saúde
                    </Link>
                  </div>
                </div>
              )}
            </nav>
          </div>

          {/* Bottom section */}
          <div className="border-t border-gray-200 p-4">
            {isAuthenticated ? (
              <Button
                variant="outline"
                onClick={handleLogout}
                className="w-full"
              >
                Sair
              </Button>
            ) : (
              <div className="space-y-2">
                <Button
                  variant="primary"
                  onClick={() => {
                    closeMenu();
                    window.location.href = '/login';
                  }}
                  className="w-full"
                >
                  Entrar
                </Button>
                <Button
                  variant="outline"
                  onClick={() => {
                    closeMenu();
                    window.location.href = '/registro';
                  }}
                  className="w-full"
                >
                  Criar Conta
                </Button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default MobileNavigation; 
