import React from 'react';
import { useTranslation } from 'react-i18next';
import { GlobeAltIcon } from '@heroicons/react/24/outline';

const languages = [
  { code: 'pt', name: 'Português' },
  { code: 'en', name: 'English' },
];

const LanguageSelector: React.FC = () => {
  const { i18n } = useTranslation();

  const changeLanguage = (lng: string) => {
    i18n.changeLanguage(lng);
    // Optional: Save language preference to localStorage
    localStorage.setItem('i18nextLng', lng);
  };

  return (
    <div className="relative group">
      <button
        type="button"
        className="flex items-center space-x-1 text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white"
        aria-label="Change language"
      >
        <GlobeAltIcon className="h-5 w-5" />
        <span className="text-sm font-medium">{i18n.language.toUpperCase()}</span>
      </button>
      <div className="absolute right-0 mt-2 w-40 rounded-md shadow-lg bg-white dark:bg-gray-800 ring-1 ring-black ring-opacity-5 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-opacity duration-200 z-50">
        <div className="py-1">
          {languages.map((lang) => (
            <button
              key={lang.code}
              onClick={() => changeLanguage(lang.code)}
              className={`block w-full text-left px-4 py-2 text-sm ${
                i18n.language === lang.code
                  ? 'bg-gray-100 dark:bg-gray-700 text-primary-600 dark:text-primary-400'
                  : 'text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-700'
              }`}
            >
              {lang.name}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default LanguageSelector;
