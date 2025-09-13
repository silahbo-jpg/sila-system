import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { 
  ExclamationTriangleIcon,
  InformationCircleIcon,
  EyeIcon,
  EyeSlashIcon,
  CalendarIcon,
  DocumentIcon,
  PlusIcon,
  XMarkIcon
} from '@heroicons/react/24/outline';

// Types for form schema (matching backend)
interface FormField {
  name: string;
  label: string;
  type: 'string' | 'email' | 'phone' | 'number' | 'integer' | 'boolean' | 'date' | 'datetime' | 'select' | 'multiselect' | 'textarea' | 'file' | 'password';
  required?: boolean;
  placeholder?: string;
  help_text?: string;
  default_value?: string | number | boolean | string[];
  options?: Array<{ value: string; label: string; }>;
  validation?: Record<string, any>;
  conditional?: Record<string, any>;
}

interface FormSchema {
  title: string;
  description?: string;
  fields: FormField[];
  submit_button_text?: string;
  cancel_button_text?: string;
  validation_rules?: Record<string, any>;
}

interface FormRendererProps {
  schema: FormSchema;
  onSubmit: (data: Record<string, any>) => void;
  onCancel?: () => void;
  loading?: boolean;
  error?: string | null;
  initialValues?: Record<string, any>;
  className?: string;
}

interface FormData {
  [key: string]: any;
}

interface FormErrors {
  [key: string]: string;
}

const FormRenderer: React.FC<FormRendererProps> = ({
  schema,
  onSubmit,
  onCancel,
  loading = false,
  error = null,
  initialValues = {},
  className = ''
}) => {
  const { t } = useTranslation();
  const [formData, setFormData] = useState<FormData>(initialValues);
  const [errors, setErrors] = useState<FormErrors>({});
  const [showPasswords, setShowPasswords] = useState<Record<string, boolean>>({});

  // Initialize form data with default values
  useEffect(() => {
    const initData: FormData = { ...initialValues };
    
    schema.fields.forEach(field => {
      if (!(field.name in initData) && field.default_value !== undefined) {
        initData[field.name] = field.default_value;
      }
    });
    
    setFormData(initData);
  }, [schema, initialValues]);

  // Field validation
  const validateField = (field: FormField, value: any): string | null => {
    // Required field validation
    if (field.required && (!value || (typeof value === 'string' && value.trim() === ''))) {
      return t('validation.required', { field: field.label });
    }

    // Type-specific validation
    switch (field.type) {
      case 'email':
        if (value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
          return t('validation.invalidEmail');
        }
        break;
      
      case 'phone':
        if (value && !/^\+?[\d\s\-\(\)]+$/.test(value)) {
          return t('validation.invalidPhone');
        }
        break;
      
      case 'number':
      case 'integer':
        if (value && isNaN(Number(value))) {
          return t('validation.invalidNumber');
        }
        break;
    }

    // Custom validation rules
    if (field.validation) {
      const { min, max, pattern } = field.validation;
      
      if (min && value && value.length < min) {
        return t('validation.minLength', { min });
      }
      
      if (max && value && value.length > max) {
        return t('validation.maxLength', { max });
      }
      
      if (pattern && value && !new RegExp(pattern).test(value)) {
        return t('validation.invalidPattern');
      }
    }

    return null;
  };

  // Handle field change
  const handleFieldChange = (fieldName: string, value: any) => {
    setFormData(prev => ({ ...prev, [fieldName]: value }));
    
    // Clear error for this field
    if (errors[fieldName]) {
      setErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[fieldName];
        return newErrors;
      });
    }
  };

  // Check if field should be shown based on conditional rules
  const isFieldVisible = (field: FormField): boolean => {
    if (!field.conditional) return true;
    
    const { dependsOn, value } = field.conditional;
    if (!dependsOn) return true;
    
    return formData[dependsOn] === value;
  };

  // Handle form submission
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    const newErrors: FormErrors = {};
    
    // Validate all visible fields
    schema.fields.forEach(field => {
      if (isFieldVisible(field)) {
        const error = validateField(field, formData[field.name]);
        if (error) {
          newErrors[field.name] = error;
        }
      }
    });
    
    setErrors(newErrors);
    
    if (Object.keys(newErrors).length === 0) {
      onSubmit(formData);
    }
  };

  // Toggle password visibility
  const togglePasswordVisibility = (fieldName: string) => {
    setShowPasswords(prev => ({
      ...prev,
      [fieldName]: !prev[fieldName]
    }));
  };

  // Render individual field
  const renderField = (field: FormField) => {
    if (!isFieldVisible(field)) return null;

    const fieldError = errors[field.name];
    const fieldValue = formData[field.name] || '';

    const baseClasses = `w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-sila-primary focus:border-transparent transition-colors duration-200 ${
      fieldError ? 'border-red-500' : 'border-gray-300'
    }`;

    const labelClasses = `block text-sm font-medium text-gray-700 mb-1 ${
      field.required ? "after:content-['*'] after:text-red-500 after:ml-1" : ''
    }`;

    switch (field.type) {
      case 'textarea':
        return (
          <div key={field.name} className="mb-4">
            <label htmlFor={field.name} className={labelClasses}>
              {field.label}
            </label>
            <textarea
              id={field.name}
              name={field.name}
              value={fieldValue}
              onChange={(e) => handleFieldChange(field.name, e.target.value)}
              placeholder={field.placeholder}
              className={`${baseClasses} min-h-[80px] resize-y`}
              rows={4}
            />
            {field.help_text && (
              <p className="mt-1 text-sm text-gray-500">{field.help_text}</p>
            )}
            {fieldError && (
              <p className="mt-1 text-sm text-red-600 flex items-center">
                <ExclamationTriangleIcon className="w-4 h-4 mr-1" />
                {fieldError}
              </p>
            )}
          </div>
        );

      case 'select':
        return (
          <div key={field.name} className="mb-4">
            <label htmlFor={field.name} className={labelClasses}>
              {field.label}
            </label>
            <select
              id={field.name}
              name={field.name}
              value={fieldValue}
              onChange={(e) => handleFieldChange(field.name, e.target.value)}
              className={baseClasses}
            >
              <option value="">{field.placeholder || t('common.select')}</option>
              {field.options?.map(option => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
            {field.help_text && (
              <p className="mt-1 text-sm text-gray-500">{field.help_text}</p>
            )}
            {fieldError && (
              <p className="mt-1 text-sm text-red-600 flex items-center">
                <ExclamationTriangleIcon className="w-4 h-4 mr-1" />
                {fieldError}
              </p>
            )}
          </div>
        );

      case 'multiselect':
        return (
          <div key={field.name} className="mb-4">
            <label htmlFor={field.name} className={labelClasses}>
              {field.label}
            </label>
            <div className="space-y-2">
              {field.options?.map(option => (
                <label key={option.value} className="flex items-center">
                  <input
                    type="checkbox"
                    value={option.value}
                    checked={(fieldValue as string[])?.includes(option.value) || false}
                    onChange={(e) => {
                      const currentValues = (fieldValue as string[]) || [];
                      const newValues = e.target.checked 
                        ? [...currentValues, option.value]
                        : currentValues.filter(v => v !== option.value);
                      handleFieldChange(field.name, newValues);
                    }}
                    className="mr-2 h-4 w-4 text-sila-primary focus:ring-sila-primary border-gray-300 rounded"
                  />
                  <span className="text-sm text-gray-700">{option.label}</span>
                </label>
              ))}
            </div>
            {field.help_text && (
              <p className="mt-1 text-sm text-gray-500">{field.help_text}</p>
            )}
            {fieldError && (
              <p className="mt-1 text-sm text-red-600 flex items-center">
                <ExclamationTriangleIcon className="w-4 h-4 mr-1" />
                {fieldError}
              </p>
            )}
          </div>
        );

      case 'boolean':
        return (
          <div key={field.name} className="mb-4">
            <label className="flex items-center">
              <input
                type="checkbox"
                name={field.name}
                checked={fieldValue || false}
                onChange={(e) => handleFieldChange(field.name, e.target.checked)}
                className="mr-2 h-4 w-4 text-sila-primary focus:ring-sila-primary border-gray-300 rounded"
              />
              <span className={`text-sm ${field.required ? "after:content-['*'] after:text-red-500 after:ml-1" : ''}`}>
                {field.label}
              </span>
            </label>
            {field.help_text && (
              <p className="mt-1 text-sm text-gray-500 ml-6">{field.help_text}</p>
            )}
            {fieldError && (
              <p className="mt-1 text-sm text-red-600 flex items-center ml-6">
                <ExclamationTriangleIcon className="w-4 h-4 mr-1" />
                {fieldError}
              </p>
            )}
          </div>
        );

      case 'password':
        return (
          <div key={field.name} className="mb-4">
            <label htmlFor={field.name} className={labelClasses}>
              {field.label}
            </label>
            <div className="relative">
              <input
                type={showPasswords[field.name] ? 'text' : 'password'}
                id={field.name}
                name={field.name}
                value={fieldValue}
                onChange={(e) => handleFieldChange(field.name, e.target.value)}
                placeholder={field.placeholder}
                className={`${baseClasses} pr-10`}
              />
              <button
                type="button"
                onClick={() => togglePasswordVisibility(field.name)}
                className="absolute inset-y-0 right-0 pr-3 flex items-center"
              >
                {showPasswords[field.name] ? (
                  <EyeSlashIcon className="h-5 w-5 text-gray-400" />
                ) : (
                  <EyeIcon className="h-5 w-5 text-gray-400" />
                )}
              </button>
            </div>
            {field.help_text && (
              <p className="mt-1 text-sm text-gray-500">{field.help_text}</p>
            )}
            {fieldError && (
              <p className="mt-1 text-sm text-red-600 flex items-center">
                <ExclamationTriangleIcon className="w-4 h-4 mr-1" />
                {fieldError}
              </p>
            )}
          </div>
        );

      case 'file':
        return (
          <div key={field.name} className="mb-4">
            <label htmlFor={field.name} className={labelClasses}>
              {field.label}
            </label>
            <div className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md hover:border-sila-primary transition-colors duration-200">
              <div className="space-y-1 text-center">
                <DocumentIcon className="mx-auto h-12 w-12 text-gray-400" />
                <div className="flex text-sm text-gray-600">
                  <label
                    htmlFor={field.name}
                    className="relative cursor-pointer bg-white rounded-md font-medium text-sila-primary hover:text-sila-secondary focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-sila-primary"
                  >
                    <span>{t('common.uploadFile')}</span>
                    <input
                      id={field.name}
                      name={field.name}
                      type="file"
                      className="sr-only"
                      onChange={(e) => handleFieldChange(field.name, e.target.files?.[0])}
                    />
                  </label>
                  <p className="pl-1">{t('common.orDragAndDrop')}</p>
                </div>
                <p className="text-xs text-gray-500">
                  {field.placeholder || t('common.fileTypes')}
                </p>
              </div>
            </div>
            {field.help_text && (
              <p className="mt-1 text-sm text-gray-500">{field.help_text}</p>
            )}
            {fieldError && (
              <p className="mt-1 text-sm text-red-600 flex items-center">
                <ExclamationTriangleIcon className="w-4 h-4 mr-1" />
                {fieldError}
              </p>
            )}
          </div>
        );

      case 'date':
      case 'datetime':
        return (
          <div key={field.name} className="mb-4">
            <label htmlFor={field.name} className={labelClasses}>
              {field.label}
            </label>
            <div className="relative">
              <input
                type={field.type === 'datetime' ? 'datetime-local' : 'date'}
                id={field.name}
                name={field.name}
                value={fieldValue}
                onChange={(e) => handleFieldChange(field.name, e.target.value)}
                className={`${baseClasses} pr-10`}
              />
              <CalendarIcon className="absolute inset-y-0 right-0 pr-3 h-full w-5 text-gray-400 pointer-events-none" />
            </div>
            {field.help_text && (
              <p className="mt-1 text-sm text-gray-500">{field.help_text}</p>
            )}
            {fieldError && (
              <p className="mt-1 text-sm text-red-600 flex items-center">
                <ExclamationTriangleIcon className="w-4 h-4 mr-1" />
                {fieldError}
              </p>
            )}
          </div>
        );

      default:
        // string, email, phone, number, integer
        return (
          <div key={field.name} className="mb-4">
            <label htmlFor={field.name} className={labelClasses}>
              {field.label}
            </label>
            <input
              type={field.type === 'email' ? 'email' : field.type === 'number' || field.type === 'integer' ? 'number' : 'text'}
              id={field.name}
              name={field.name}
              value={fieldValue}
              onChange={(e) => handleFieldChange(field.name, e.target.value)}
              placeholder={field.placeholder}
              className={baseClasses}
              step={field.type === 'integer' ? '1' : 'any'}
            />
            {field.help_text && (
              <p className="mt-1 text-sm text-gray-500">{field.help_text}</p>
            )}
            {fieldError && (
              <p className="mt-1 text-sm text-red-600 flex items-center">
                <ExclamationTriangleIcon className="w-4 h-4 mr-1" />
                {fieldError}
              </p>
            )}
          </div>
        );
    }
  };

  return (
    <div className={`bg-white rounded-lg shadow-sm ${className}`}>
      {/* Form Header */}
      <div className="px-6 py-4 border-b border-gray-200">
        <h2 className="text-xl font-semibold text-gray-900">{schema.title}</h2>
        {schema.description && (
          <p className="mt-1 text-sm text-gray-600">{schema.description}</p>
        )}
      </div>

      {/* Error Message */}
      {error && (
        <div className="px-6 py-4 bg-red-50 border-l-4 border-red-400">
          <div className="flex">
            <ExclamationTriangleIcon className="h-5 w-5 text-red-400" />
            <div className="ml-3">
              <p className="text-sm text-red-700">{error}</p>
            </div>
          </div>
        </div>
      )}

      {/* Form Content */}
      <form onSubmit={handleSubmit} className="px-6 py-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {schema.fields.map(renderField)}
        </div>

        {/* Form Actions */}
        <div className="flex flex-col sm:flex-row gap-3 mt-6 pt-4 border-t border-gray-200">
          <button
            type="submit"
            disabled={loading}
            className="flex-1 sm:flex-none sm:w-auto inline-flex justify-center items-center px-6 py-2 border border-transparent text-base font-medium rounded-md text-white bg-sila-primary hover:bg-sila-secondary focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-sila-primary disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
          >
            {loading ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                {t('common.processing')}
              </>
            ) : (
              schema.submit_button_text || t('common.submit')
            )}
          </button>
          
          {onCancel && (
            <button
              type="button"
              onClick={onCancel}
              disabled={loading}
              className="flex-1 sm:flex-none sm:w-auto inline-flex justify-center items-center px-6 py-2 border border-gray-300 text-base font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-sila-primary disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
            >
              {schema.cancel_button_text || t('common.cancel')}
            </button>
          )}
        </div>
      </form>
    </div>
  );
};

export default FormRenderer;