import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import { 
  MagnifyingGlassIcon,
  MapPinIcon,
  ClockIcon,
  DocumentTextIcon,
  TagIcon,
  BuildingOfficeIcon,
  ChevronRightIcon
} from '@heroicons/react/24/outline';

import { useServices, ServiceDefinition } from '../hooks/useServices';

const ServicesPage: React.FC = () => {
  const { t, i18n } = useTranslation();
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedMunicipality, setSelectedMunicipality] = useState('all');
  const [selectedCategory, setSelectedCategory] = useState('all');
  
  // Use dynamic services hook
  const { 
    services, 
    loading: isLoading, 
    error, 
    categories,
    refetch 
  } = useServices({ 
    status: 'active',
    category: selectedCategory === 'all' ? undefined : selectedCategory 
  });
  
  const [filteredServices, setFilteredServices] = useState<ServiceDefinition[]>([]);

  // Huambo Province Municipalities from memory specification
  const municipalities = [
    'Huambo', 'Bailundo', 'Bimbe', 'Ecunha', 'Caála', 'Cuima', 
    'Cachiungo', 'Galanga', 'Londuimbali', 'Alto Hama', 'Longonjo', 
    'Chilata', 'Mungo', 'Chinjenje', 'Chicala-Cholohanga', 'Sambo', 'Ucuma'
  ];

  // Filter services based on search and municipality
  useEffect(() => {
    let filtered = services;

    if (searchTerm) {
      filtered = filtered.filter(service => {
        const name = i18n.language === 'pt' ? service.name : service.translations?.en?.name || service.name;
        const description = i18n.language === 'pt' ? service.description : service.translations?.en?.description || service.description;
        return name.toLowerCase().includes(searchTerm.toLowerCase()) ||
               (description && description.toLowerCase().includes(searchTerm.toLowerCase()));
      });
    }

    if (selectedMunicipality !== 'all') {
      filtered = filtered.filter(service => 
        service.metadata?.municipality_specific && 
        service.metadata?.municipality === selectedMunicipality
      );
    }

    setFilteredServices(filtered);
  }, [searchTerm, selectedMunicipality, services, i18n.language]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-800';
      case 'maintenance': return 'bg-yellow-100 text-yellow-800';
      case 'inactive': return 'bg-red-100 text-red-800';
      case 'deprecated': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'active': return t('services.status.active');
      case 'maintenance': return t('services.status.maintenance');
      case 'inactive': return t('services.status.inactive');
      case 'deprecated': return t('services.status.deprecated');
      default: return status;
    }
  };

  const handleServiceAccess = (serviceId: string) => {
    const service = services.find(s => s.id === serviceId);
    if (service?.status === 'active') {
      // Navigate to dynamic service form
      navigate(`/services/${serviceId}`);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-sila-primary mx-auto"></div>
          <p className="mt-4 text-gray-600">{t('common.loading')}</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center max-w-md mx-auto">
          <div className="bg-red-100 rounded-full p-3 mx-auto w-16 h-16 flex items-center justify-center mb-4">
            <DocumentTextIcon className="w-8 h-8 text-red-600" />
          </div>
          <h2 className="text-xl font-semibold text-gray-900 mb-2">
            {t('services.errors.loadFailed')}
          </h2>
          <p className="text-gray-600 mb-6">{error}</p>
          <button
            onClick={refetch}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-sila-primary hover:bg-sila-secondary transition-colors duration-200"
          >
            {t('common.retry')}
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center mb-4">
            <BuildingOfficeIcon className="w-8 h-8 text-sila-primary mr-3" />
            <h1 className="text-3xl font-bold text-gray-900">
              {t('services.title')}
            </h1>
          </div>
          <p className="text-gray-600 text-lg">
            {t('services.subtitle')}
          </p>
        </div>

        {/* Filters */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Search */}
            <div className="relative">
              <label htmlFor="search" className="sr-only">
                {t('services.search.placeholder')}
              </label>
              <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                id="search"
                placeholder={t('services.search.placeholder')}
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:ring-sila-primary focus:border-sila-primary"
              />
            </div>

            {/* Municipality Filter */}
            <div>
              <label htmlFor="municipality" className="sr-only">
                {t('services.filters.municipality')}
              </label>
              <select
                id="municipality"
                value={selectedMunicipality}
                onChange={(e) => setSelectedMunicipality(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-sila-primary focus:border-sila-primary"
              >
                <option value="all">{t('services.filters.allMunicipalities')}</option>
                {municipalities.map(municipality => (
                  <option key={municipality} value={municipality}>
                    {municipality}
                  </option>
                ))}
              </select>
            </div>

            {/* Category Filter */}
            <div>
              <label htmlFor="category" className="sr-only">
                {t('services.filters.category')}
              </label>
              <select
                id="category"
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-sila-primary focus:border-sila-primary"
              >
                <option value="all">{t('services.filters.allCategories')}</option>
                {categories.map(category => (
                  <option key={category} value={category}>
                    {t(`services.categories.${category}`, category)}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Results Count */}
        <div className="mb-6">
          <p className="text-gray-600">
            {t('services.resultsCount', { count: filteredServices.length })}
          </p>
        </div>

        {/* Services Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredServices.map((service) => (
            <div
              key={service.id}
              className="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200 overflow-hidden border border-gray-200"
            >
              <div className="p-6">
                {/* Service Header */}
                <div className="flex justify-between items-start mb-4">
                  <h3 className="text-lg font-semibold text-gray-900 flex-1 pr-2">
                    {i18n.language === 'pt' ? service.name : service.translations?.en?.name || service.name}
                  </h3>
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(service.status)}`}>
                    {getStatusText(service.status)}
                  </span>
                </div>

                {/* Service Description */}
                <p className="text-gray-600 text-sm mb-4 line-clamp-3">
                  {i18n.language === 'pt' ? service.description : service.translations?.en?.description || service.description}
                </p>

                {/* Service Details */}
                <div className="space-y-2 mb-4">
                  {service.metadata?.category && (
                    <div className="flex items-center text-sm text-gray-500">
                      <TagIcon className="w-4 h-4 mr-2 flex-shrink-0" />
                      <span>{t(`services.categories.${service.metadata.category}`, service.metadata.category)}</span>
                    </div>
                  )}
                  {service.metadata?.estimated_time && (
                    <div className="flex items-center text-sm text-gray-500">
                      <ClockIcon className="w-4 h-4 mr-2 flex-shrink-0" />
                      <span>{service.metadata.estimated_time}</span>
                    </div>
                  )}
                  {service.metadata?.fee && (
                    <div className="flex items-center text-sm text-gray-500">
                      <DocumentTextIcon className="w-4 h-4 mr-2 flex-shrink-0" />
                      <span>{service.metadata.fee}</span>
                    </div>
                  )}
                </div>

                {/* Action Button */}
                <button 
                  onClick={() => handleServiceAccess(service.id)}
                  disabled={service.status !== 'active'}
                  className="w-full flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-sila-primary hover:bg-sila-secondary transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-sila-primary"
                >
                  {service.status === 'active' && (
                    <>
                      {t('services.actions.access')}
                      <ChevronRightIcon className="w-4 h-4 ml-2" />
                    </>
                  )}
                  {service.status === 'inactive' && t('services.actions.inactive')}
                  {service.status === 'maintenance' && t('services.actions.maintenance')}
                  {service.status === 'deprecated' && t('services.actions.deprecated')}
                </button>
              </div>
            </div>
          ))}
        </div>

        {/* No Results */}
        {filteredServices.length === 0 && (
          <div className="text-center py-12">
            <DocumentTextIcon className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              {t('services.noResults.title')}
            </h3>
            <p className="text-gray-600 mb-4">
              {t('services.noResults.description')}
            </p>
            <button
              onClick={() => {
                setSearchTerm('');
                setSelectedMunicipality('all');
                setSelectedCategory('all');
              }}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-sila-primary bg-sila-primary/10 hover:bg-sila-primary/20 transition-colors duration-200"
            >
              {t('services.noResults.clearFilters')}
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default ServicesPage;