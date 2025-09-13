import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { 
  Bars3Icon, 
  XMarkIcon, 
  HomeIcon, 
  CogIcon, 
  UserIcon,
  AcademicCapIcon,
  BuildingOfficeIcon
} from '@heroicons/react/24/outline';

const Header: React.FC = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const { t, i18n } = useTranslation();
  const location = useLocation();

  const navigation = [
    { name: t('nav.home'), href: '/', icon: HomeIcon },
    { name: t('nav.services'), href: '/services', icon: BuildingOfficeIcon },
    { name: t('nav.training'), href: '/training', icon: AcademicCapIcon },
    { name: t('nav.dashboard'), href: '/dashboard', icon: CogIcon },
  ];

  const toggleLanguage = () => {
    const newLang = i18n.language === 'pt' ? 'en' : 'pt';
    i18n.changeLanguage(newLang);
  };

  const isCurrentPage = (href: string) => {
    return location.pathname === href;
  };

  return (
    <header className="bg-sila-primary shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo and Brand */}
          <div className="flex items-center">
            <Link to="/" className="flex items-center">
              <div className="flex-shrink-0 flex items-center">
                <div className="w-8 h-8 bg-sila-accent rounded-full flex items-center justify-center mr-3">
                  <span className="text-white font-bold text-sm">AO</span>
                </div>
                <div className="text-white">
                  <h1 className="text-xl font-bold">SILA</h1>
                  <p className="text-xs opacity-90">{t('header.subtitle')}</p>
                </div>
              </div>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex space-x-8">
            {navigation.map((item) => {
              const Icon = item.icon;
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={`flex items-center px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${
                    isCurrentPage(item.href)
                      ? 'bg-sila-accent text-white'
                      : 'text-sila-light hover:bg-sila-secondary hover:text-white'
                  }`}
                  aria-current={isCurrentPage(item.href) ? 'page' : undefined}
                >
                  <Icon className="w-4 h-4 mr-2" />
                  {item.name}
                </Link>
              );
            })}
          </nav>

          {/* Right Side - Language Toggle & User */}
          <div className="hidden md:flex items-center space-x-4">
            {/* Language Toggle */}
            <button
              onClick={toggleLanguage}
              className="bg-sila-secondary text-white px-3 py-2 rounded-md text-sm font-medium hover:bg-sila-accent transition-colors duration-200"
              aria-label={t('header.toggleLanguage')}
            >
              {i18n.language === 'pt' ? 'EN' : 'PT'}
            </button>

            {/* User Menu */}
            <Link
              to="/login"
              className="flex items-center text-sila-light hover:text-white transition-colors duration-200"
              aria-label={t('header.login')}
            >
              <UserIcon className="w-5 h-5 mr-1" />
              <span className="text-sm font-medium">{t('header.login')}</span>
            </Link>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="text-sila-light hover:text-white p-2 rounded-md"
              aria-expanded={isMenuOpen}
              aria-label={t('header.toggleMenu')}
            >
              {isMenuOpen ? (
                <XMarkIcon className="w-6 h-6" />
              ) : (
                <Bars3Icon className="w-6 h-6" />
              )}
            </button>
          </div>
        </div>

        {/* Mobile Navigation Menu */}
        {isMenuOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1 bg-sila-secondary rounded-lg mt-2">
              {navigation.map((item) => {
                const Icon = item.icon;
                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    className={`flex items-center px-3 py-2 rounded-md text-base font-medium transition-colors duration-200 ${
                      isCurrentPage(item.href)
                        ? 'bg-sila-accent text-white'
                        : 'text-sila-light hover:bg-sila-primary hover:text-white'
                    }`}
                    onClick={() => setIsMenuOpen(false)}
                    aria-current={isCurrentPage(item.href) ? 'page' : undefined}
                  >
                    <Icon className="w-5 h-5 mr-3" />
                    {item.name}
                  </Link>
                );
              })}
              
              {/* Mobile Language Toggle */}
              <button
                onClick={() => {
                  toggleLanguage();
                  setIsMenuOpen(false);
                }}
                className="w-full text-left flex items-center px-3 py-2 rounded-md text-base font-medium text-sila-light hover:bg-sila-primary hover:text-white transition-colors duration-200"
              >
                🌐 {i18n.language === 'pt' ? 'English' : 'Português'}
              </button>

              {/* Mobile Login */}
              <Link
                to="/login"
                className="flex items-center px-3 py-2 rounded-md text-base font-medium text-sila-light hover:bg-sila-primary hover:text-white transition-colors duration-200"
                onClick={() => setIsMenuOpen(false)}
              >
                <UserIcon className="w-5 h-5 mr-3" />
                {t('header.login')}
              </Link>
            </div>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;