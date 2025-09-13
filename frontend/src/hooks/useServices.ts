import { useState, useEffect, useCallback } from 'react';
import { useTranslation } from 'react-i18next';

// Types for services (matching backend)
export interface ServiceDefinition {
  id: string;
  name: string;
  description?: string;
  module: string;
  icon?: string;
  roles: string[];
  status: 'active' | 'inactive' | 'maintenance' | 'deprecated';
  api_endpoint: string;
  form_schema?: {
    title: string;
    description?: string;
    fields: Array<{
      name: string;
      label: string;
      type: string;
      required?: boolean;
      placeholder?: string;
      help_text?: string;
      default_value?: any;
      options?: Array<{ value: string; label: string; }>;
      validation?: Record<string, any>;
      conditional?: Record<string, any>;
    }>;
    submit_button_text?: string;
    cancel_button_text?: string;
  };
  translations?: {
    en: Record<string, string>;
    pt: Record<string, string>;
  };
  metadata?: {
    category?: string;
    estimated_time?: string;
    required_documents?: string[];
    fee?: string;
    prerequisites?: string[];
    municipality_specific?: boolean;
    online_only?: boolean;
  };
  created_at: string;
  updated_at: string;
}

export interface ServiceListResponse {
  services: ServiceDefinition[];
  total: number;
  filtered: number;
}

interface UseServicesOptions {
  role?: string;
  status?: string;
  category?: string;
  autoFetch?: boolean;
}

interface UseServicesResult {
  services: ServiceDefinition[];
  loading: boolean;
  error: string | null;
  total: number;
  filtered: number;
  refetch: () => Promise<void>;
  getService: (serviceId: string) => ServiceDefinition | undefined;
  categories: string[];
  fetchCategories: () => Promise<void>;
}

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

export const useServices = (options: UseServicesOptions = {}): UseServicesResult => {
  const { role, status = 'active', category, autoFetch = true } = options;
  const { i18n } = useTranslation();
  
  const [services, setServices] = useState<ServiceDefinition[]>([]);
  const [categories, setCategories] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [total, setTotal] = useState(0);
  const [filtered, setFiltered] = useState(0);

  // Get authentication token from localStorage or sessionStorage
  const getAuthToken = useCallback(() => {
    return localStorage.getItem('sila_token') || sessionStorage.getItem('sila_token');
  }, []);

  // Fetch services from API
  const fetchServices = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const token = getAuthToken();
      const params = new URLSearchParams();
      
      if (role) params.append('role', role);
      if (status) params.append('status', status);
      if (category) params.append('category', category);

      const response = await fetch(`${API_BASE_URL}/services?${params.toString()}`, {
        headers: {
          'Authorization': token ? `Bearer ${token}` : '',
          'Content-Type': 'application/json',
          'Accept-Language': i18n.language
        }
      });

      if (!response.ok) {
        if (response.status === 401) {
          throw new Error('Authentication required. Please log in.');
        }
        throw new Error(`Failed to fetch services: ${response.statusText}`);
      }

      const data: ServiceListResponse = await response.json();
      
      setServices(data.services);
      setTotal(data.total);
      setFiltered(data.filtered);
    } catch (err) {
      console.error('Error fetching services:', err);
      setError(err instanceof Error ? err.message : 'Failed to fetch services');
      setServices([]);
    } finally {
      setLoading(false);
    }
  }, [role, status, category, i18n.language, getAuthToken]);

  // Fetch service categories
  const fetchCategories = useCallback(async () => {
    try {
      const token = getAuthToken();
      const response = await fetch(`${API_BASE_URL}/services/categories`, {
        headers: {
          'Authorization': token ? `Bearer ${token}` : '',
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        setCategories(data.categories || []);
      }
    } catch (err) {
      console.error('Error fetching categories:', err);
    }
  }, [getAuthToken]);

  // Get a specific service by ID
  const getService = useCallback((serviceId: string): ServiceDefinition | undefined => {
    return services.find(service => service.id === serviceId);
  }, [services]);

  // Auto-fetch on mount and when dependencies change
  useEffect(() => {
    if (autoFetch) {
      fetchServices();
    }
  }, [fetchServices, autoFetch]);

  // Fetch categories on mount
  useEffect(() => {
    fetchCategories();
  }, [fetchCategories]);

  return {
    services,
    loading,
    error,
    total,
    filtered,
    refetch: fetchServices,
    getService,
    categories,
    fetchCategories
  };
};

// Hook for fetching a single service
export const useService = (serviceId: string) => {
  const [service, setService] = useState<ServiceDefinition | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { i18n } = useTranslation();

  const getAuthToken = useCallback(() => {
    return localStorage.getItem('sila_token') || sessionStorage.getItem('sila_token');
  }, []);

  const fetchService = useCallback(async () => {
    if (!serviceId) return;

    setLoading(true);
    setError(null);

    try {
      const token = getAuthToken();
      const response = await fetch(`${API_BASE_URL}/services/${serviceId}`, {
        headers: {
          'Authorization': token ? `Bearer ${token}` : '',
          'Content-Type': 'application/json',
          'Accept-Language': i18n.language
        }
      });

      if (!response.ok) {
        if (response.status === 401) {
          throw new Error('Authentication required. Please log in.');
        }
        if (response.status === 404) {
          throw new Error('Service not found.');
        }
        throw new Error(`Failed to fetch service: ${response.statusText}`);
      }

      const data: ServiceDefinition = await response.json();
      setService(data);
    } catch (err) {
      console.error('Error fetching service:', err);
      setError(err instanceof Error ? err.message : 'Failed to fetch service');
      setService(null);
    } finally {
      setLoading(false);
    }
  }, [serviceId, i18n.language, getAuthToken]);

  useEffect(() => {
    fetchService();
  }, [fetchService]);

  return {
    service,
    loading,
    error,
    refetch: fetchService
  };
};

// Hook for submitting service requests
export const useServiceSubmission = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const getAuthToken = useCallback(() => {
    return localStorage.getItem('sila_token') || sessionStorage.getItem('sila_token');
  }, []);

  const submitServiceRequest = useCallback(async (serviceId: string, formData: Record<string, any>) => {
    setLoading(true);
    setError(null);

    try {
      const token = getAuthToken();
      if (!token) {
        throw new Error('Authentication required. Please log in.');
      }

      // Get service details to find the API endpoint
      const serviceResponse = await fetch(`${API_BASE_URL}/services/${serviceId}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (!serviceResponse.ok) {
        throw new Error('Service not found');
      }

      const service: ServiceDefinition = await serviceResponse.json();

      // Submit the form data to the service's API endpoint
      const response = await fetch(`${API_BASE_URL}${service.api_endpoint.replace('/api/v1', '')}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Failed to submit request: ${response.statusText}`);
      }

      const result = await response.json();
      return result;
    } catch (err) {
      console.error('Error submitting service request:', err);
      const errorMessage = err instanceof Error ? err.message : 'Failed to submit request';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [getAuthToken]);

  return {
    submitServiceRequest,
    loading,
    error
  };
};