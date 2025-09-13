import React from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { 
  HomeIcon, 
  MagnifyingGlassIcon,
  ExclamationTriangleIcon,
  ArrowLeftIcon,
  BuildingOfficeIcon,
  PhoneIcon,
  QuestionMarkCircleIcon
} from '@heroicons/react/24/outline';

const NotFoundPage: React.FC = () => {
  const { t } = useTranslation();

  const suggestedLinks = [
    {
      name: t('notFound.suggestions.home'),
      href: '/',
      description: t('notFound.suggestions.homeDesc'),
      icon: HomeIcon
    },
    {
      name: t('notFound.suggestions.services'),
      href: '/services',
      description: t('notFound.suggestions.servicesDesc'),
      icon: BuildingOfficeIcon
    },
    {
      name: t('notFound.suggestions.training'),
      href: '/training',
      description: t('notFound.suggestions.trainingDesc'),
      icon: QuestionMarkCircleIcon
    }
  ];

  const handleGoBack = () => {
    window.history.back();
  };

  const handleReportProblem = () => {
    // In a real app, this would open a support form or contact system
    alert(t('notFound.reportProblem.comingSoon'));
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md lg:max-w-2xl">
        {/* Error Illustration */}
        <div className="text-center">
          <div className="mx-auto w-24 h-24 bg-red-100 rounded-full flex items-center justify-center mb-6">
            <ExclamationTriangleIcon className="w-12 h-12 text-red-600" />
          </div>
          
          {/* Error Code */}
          <h1 className="text-6xl font-bold text-gray-900 mb-4">404</h1>
          
          {/* Error Title */}
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            {t('notFound.title')}
          </h2>
          
          {/* Error Description */}
          <p className="text-lg text-gray-600 mb-8 max-w-md mx-auto">
            {t('notFound.description')}
          </p>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
          <button
            onClick={handleGoBack}
            className="flex items-center justify-center px-6 py-3 border border-gray-300 rounded-md text-base font-medium text-gray-700 bg-white hover:bg-gray-50 transition-colors duration-200"
          >
            <ArrowLeftIcon className="w-5 h-5 mr-2" />
            {t('notFound.actions.goBack')}
          </button>
          
          <Link
            to="/"
            className="flex items-center justify-center px-6 py-3 border border-transparent rounded-md text-base font-medium text-white bg-sila-primary hover:bg-sila-secondary transition-colors duration-200"
          >
            <HomeIcon className="w-5 h-5 mr-2" />
            {t('notFound.actions.goHome')}
          </Link>
        </div>

        {/* Suggested Links */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 text-center">
            {t('notFound.suggestions.title')}
          </h3>
          <div className="space-y-4">
            {suggestedLinks.map((link) => {
              const Icon = link.icon;
              return (
                <Link
                  key={link.href}
                  to={link.href}
                  className="flex items-start p-4 border border-gray-200 rounded-lg hover:border-sila-primary hover:bg-sila-primary/5 transition-all duration-200 group"
                >
                  <Icon className="w-6 h-6 text-sila-primary mr-4 mt-0.5 group-hover:text-sila-secondary" />
                  <div>
                    <h4 className="text-base font-medium text-gray-900 group-hover:text-sila-primary">
                      {link.name}
                    </h4>
                    <p className="text-sm text-gray-600 mt-1">
                      {link.description}
                    </p>
                  </div>
                </Link>
              );
            })}
          </div>
        </div>

        {/* Search Box */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 text-center">
            {t('notFound.search.title')}
          </h3>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <MagnifyingGlassIcon className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="text"
              placeholder={t('notFound.search.placeholder')}
              className="block w-full pl-10 pr-4 py-3 border border-gray-300 rounded-md focus:ring-sila-primary focus:border-sila-primary text-base"
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  // In a real app, this would perform a search
                  alert(t('notFound.search.comingSoon'));
                }
              }}
            />
          </div>
          <p className="text-sm text-gray-500 mt-2 text-center">
            {t('notFound.search.help')}
          </p>
        </div>

        {/* Help and Contact */}
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 text-center">
            {t('notFound.help.title')}
          </h3>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <button
              onClick={handleReportProblem}
              className="flex items-center justify-center p-4 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors duration-200"
            >
              <ExclamationTriangleIcon className="w-5 h-5 text-orange-500 mr-2" />
              <span className="text-sm font-medium text-gray-700">
                {t('notFound.help.reportProblem')}
              </span>
            </button>
            
            <a
              href="tel:+244123456789"
              className="flex items-center justify-center p-4 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors duration-200"
            >
              <PhoneIcon className="w-5 h-5 text-green-500 mr-2" />
              <span className="text-sm font-medium text-gray-700">
                {t('notFound.help.contactSupport')}
              </span>
            </a>
          </div>
          
          <div className="mt-4 text-center">
            <p className="text-xs text-gray-500">
              {t('notFound.help.businessHours')}
            </p>
          </div>
        </div>

        {/* Footer Info */}
        <div className="mt-8 text-center">
          <p className="text-sm text-gray-500">
            {t('notFound.footer.errorCode')} • {t('notFound.footer.timestamp', { 
              timestamp: new Date().toISOString() 
            })}
          </p>
          <p className="text-xs text-gray-400 mt-1">
            {t('notFound.footer.version')}
          </p>
        </div>
      </div>
    </div>
  );
};

export default NotFoundPage;