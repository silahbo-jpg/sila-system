import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { 
  ArrowLeftIcon,
  ClockIcon,
  CurrencyDollarIcon,
  DocumentTextIcon,
  ExclamationCircleIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline';

import FormRenderer from '../forms/FormRenderer';
import { useService, useServiceSubmission } from '../../hooks/useServices';

const DynamicServiceForm: React.FC = () => {
  const { serviceId } = useParams<{ serviceId: string }>();
  const navigate = useNavigate();
  const { t, i18n } = useTranslation();
  
  const { service, loading: serviceLoading, error: serviceError } = useService(serviceId || '');
  const { submitServiceRequest, loading: submitLoading, error: submitError } = useServiceSubmission();
  
  const [submitted, setSubmitted] = useState(false);
  const [submissionResult, setSubmissionResult] = useState<any>(null);

  const handleSubmit = async (formData: Record<string, any>) => {
    if (!serviceId) return;

    try {
      const result = await submitServiceRequest(serviceId, formData);
      setSubmissionResult(result);
      setSubmitted(true);
    } catch (error) {
      // Error is handled by the hook
      console.error('Submission failed:', error);
    }
  };

  const handleCancel = () => {
    navigate('/services');
  };

  const handleBackToServices = () => {
    navigate('/services');
  };

  if (serviceLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-sila-primary mx-auto"></div>
          <p className="mt-4 text-gray-600">{t('common.loading')}</p>
        </div>
      </div>
    );
  }

  if (serviceError || !service) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center max-w-md mx-auto">
          <ExclamationCircleIcon className="mx-auto h-12 w-12 text-red-500 mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 mb-2">
            {t('services.errors.notFound')}
          </h2>
          <p className="text-gray-600 mb-6">
            {serviceError || t('services.errors.notFoundDescription')}
          </p>
          <button
            onClick={handleBackToServices}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-sila-primary hover:bg-sila-secondary transition-colors duration-200"
          >
            <ArrowLeftIcon className="w-4 h-4 mr-2" />
            {t('services.backToServices')}
          </button>
        </div>
      </div>
    );
  }

  if (submitted) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="bg-white rounded-lg shadow-sm p-8 text-center">
            <CheckCircleIcon className="mx-auto h-16 w-16 text-green-500 mb-4" />
            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              {t('services.submission.success')}
            </h2>
            <p className="text-gray-600 mb-6">
              {t('services.submission.successDescription', { 
                serviceName: i18n.language === 'pt' ? service.name : service.translations?.en?.name || service.name 
              })}
            </p>
            
            {submissionResult && (
              <div className="bg-gray-50 rounded-lg p-6 mb-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                  {t('services.submission.details')}
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                  {submissionResult.reference_number && (
                    <div>
                      <span className="font-medium text-gray-700">{t('services.submission.referenceNumber')}:</span>
                      <span className="ml-2 font-mono text-sila-primary">{submissionResult.reference_number}</span>
                    </div>
                  )}
                  {submissionResult.status && (
                    <div>
                      <span className="font-medium text-gray-700">{t('services.submission.status')}:</span>
                      <span className="ml-2">{submissionResult.status}</span>
                    </div>
                  )}
                  {submissionResult.estimated_completion && (
                    <div>
                      <span className="font-medium text-gray-700">{t('services.submission.estimatedCompletion')}:</span>
                      <span className="ml-2">{submissionResult.estimated_completion}</span>
                    </div>
                  )}
                </div>
              </div>
            )}
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button
                onClick={handleBackToServices}
                className="inline-flex items-center px-6 py-2 border border-transparent text-base font-medium rounded-md text-white bg-sila-primary hover:bg-sila-secondary transition-colors duration-200"
              >
                {t('services.backToServices')}
              </button>
              <button
                onClick={() => navigate('/dashboard')}
                className="inline-flex items-center px-6 py-2 border border-gray-300 text-base font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 transition-colors duration-200"
              >
                {t('navigation.dashboard')}
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Get service name and description in current language
  const serviceName = i18n.language === 'pt' 
    ? service.name 
    : service.translations?.en?.name || service.name;
  
  const serviceDescription = i18n.language === 'pt' 
    ? service.description 
    : service.translations?.en?.description || service.description;

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-6">
          <button
            onClick={handleBackToServices}
            className="inline-flex items-center text-sm text-gray-500 hover:text-sila-primary transition-colors duration-200 mb-4"
          >
            <ArrowLeftIcon className="w-4 h-4 mr-1" />
            {t('services.backToServices')}
          </button>
          
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <h1 className="text-2xl font-bold text-gray-900 mb-2">
                {serviceName}
              </h1>
              {serviceDescription && (
                <p className="text-gray-600 mb-4">
                  {serviceDescription}
                </p>
              )}
            </div>
          </div>
        </div>

        {/* Service Information */}
        {service.metadata && (
          <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">
              {t('services.information.title')}
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {service.metadata.estimated_time && (
                <div className="flex items-center">
                  <ClockIcon className="w-5 h-5 text-gray-400 mr-3" />
                  <div>
                    <p className="text-sm font-medium text-gray-900">
                      {t('services.information.estimatedTime')}
                    </p>
                    <p className="text-sm text-gray-600">
                      {service.metadata.estimated_time}
                    </p>
                  </div>
                </div>
              )}
              
              {service.metadata.fee && (
                <div className="flex items-center">
                  <CurrencyDollarIcon className="w-5 h-5 text-gray-400 mr-3" />
                  <div>
                    <p className="text-sm font-medium text-gray-900">
                      {t('services.information.fee')}
                    </p>
                    <p className="text-sm text-gray-600">
                      {service.metadata.fee}
                    </p>
                  </div>
                </div>
              )}

              {service.metadata.required_documents && service.metadata.required_documents.length > 0 && (
                <div className="flex items-start">
                  <DocumentTextIcon className="w-5 h-5 text-gray-400 mr-3 mt-0.5" />
                  <div>
                    <p className="text-sm font-medium text-gray-900 mb-1">
                      {t('services.information.requiredDocuments')}
                    </p>
                    <ul className="text-sm text-gray-600 space-y-1">
                      {service.metadata.required_documents.map((doc, index) => (
                        <li key={index} className="flex items-center">
                          <span className="w-1.5 h-1.5 bg-gray-400 rounded-full mr-2"></span>
                          {doc}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Dynamic Form */}
        {service.form_schema ? (
          <FormRenderer
            schema={service.form_schema}
            onSubmit={handleSubmit}
            onCancel={handleCancel}
            loading={submitLoading}
            error={submitError}
          />
        ) : (
          <div className="bg-white rounded-lg shadow-sm p-8 text-center">
            <ExclamationCircleIcon className="mx-auto h-12 w-12 text-yellow-500 mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              {t('services.errors.noForm')}
            </h3>
            <p className="text-gray-600 mb-6">
              {t('services.errors.noFormDescription')}
            </p>
            <button
              onClick={handleBackToServices}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-sila-primary hover:bg-sila-secondary transition-colors duration-200"
            >
              <ArrowLeftIcon className="w-4 h-4 mr-2" />
              {t('services.backToServices')}
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default DynamicServiceForm;