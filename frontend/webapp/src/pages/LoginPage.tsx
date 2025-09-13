import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { toast } from 'react-hot-toast';
import { useTranslation } from 'react-i18next';
import {
  LockClosedIcon,
  UserCircleIcon,
  AtSymbolIcon,
  FingerPrintIcon,
  PhoneIcon,
  ArrowRightOnRectangleIcon,
  ExclamationCircleIcon
} from '@heroicons/react/24/outline';
import Button from '../components/ui/Button';

type FormData = {
  nif: string;
  phone: string;
  email: string;
  password: string;
  rememberMe: boolean;
};

type LoginMethod = 'nif' | 'email' | 'veritas' | 'biometric';

interface LoginMethodOption {
  id: LoginMethod;
  label: string;
  icon: React.ReactNode;
}

const LoginPage: React.FC = () => {
  const { t } = useTranslation();
  const { login, isAuthenticated, isLoading } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();

  const from = location.state?.from?.pathname || '/';
  const message = location.state?.message;

  const [activeTab, setActiveTab] = useState<LoginMethod>('nif');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [formData, setFormData] = useState<FormData>({
    nif: '',
    phone: '',
    email: '',
    password: '',
    rememberMe: false
  });
  const [errors, setErrors] = useState<Record<string, string>>({});

  // Exibe toast se houver mensagem
  useEffect(() => {
    if (message) {
      toast(message as string, { icon: 'ℹ️', duration: 5000 });
    }
  }, [message]);

  // Redireciona se já estiver autenticado
  useEffect(() => {
    if (isAuthenticated) {
      navigate(from, { replace: true });
    }
  }, [isAuthenticated, navigate, from]);

  const loginMethods: LoginMethodOption[] = [
    { id: 'nif', label: t('login.tabs.nif') || 'NIF', icon: <UserCircleIcon className="h-5 w-5" /> },
    { id: 'email', label: t('login.tabs.email') || 'Email', icon: <AtSymbolIcon className="h-5 w-5" /> },
    { id: 'veritas', label: t('login.tabs.veritas') || 'Veritas', icon: <FingerPrintIcon className="h-5 w-5" /> },
    { id: 'biometric', label: t('login.tabs.biometric') || 'Biometric', icon: <PhoneIcon className="h-5 w-5" /> },
  ];

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));

    if (errors[name]) {
      const newErrors = { ...errors };
      delete newErrors[name];
      setErrors(newErrors);
    }
  };

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (activeTab === 'nif' && !formData.nif.trim()) {
      newErrors.nif = t('login.errors.nif_required') || 'NIF is required';
    }

    if (activeTab === 'email') {
      if (!formData.email.trim()) {
        newErrors.email = t('login.errors.email_required') || 'Email is required';
      } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
        newErrors.email = t('login.errors.invalid_email') || 'Please enter a valid email address';
      }
    }

    if (!formData.password) {
      newErrors.password = t('login.errors.password_required') || 'Password is required';
    } else if (formData.password.length < 6) {
      newErrors.password = t('login.errors.password_length') || 'Password must be at least 6 characters';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) return;
    setIsSubmitting(true);

    try {
      const credentials = {
        email: activeTab === 'email' ? formData.email : undefined,
        nif: activeTab === 'nif' ? formData.nif : undefined,
        password: formData.password,
        method: 'password' as const,
      };

      await login(credentials);

      toast.success(t('login.success') || 'Login successful!');
    } catch (error: any) {
      console.error('Login error:', error);
      const errorMessage = error?.response?.data?.message ||
        error?.message ||
        t('login.errors.login_failed') ||
        'Failed to login. Please try again.';
      toast.error(errorMessage);

      if (error?.response?.data?.errors) {
        setErrors(error.response.data.errors);
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  const renderLoginForm = () => {
    if (activeTab === 'nif' || activeTab === 'email') {
      return (
        <form onSubmit={handleSubmit} className="space-y-6">
          {activeTab === 'nif' && (
            <div>
              <label htmlFor="nif" className="block text-sm font-medium text-gray-700 mb-1">
                {t('login.nif') || 'NIF'}
              </label>
              <div className="relative rounded-md shadow-sm">
                <UserCircleIcon className="absolute inset-y-0 left-0 pl-3 h-5 w-5 text-gray-400 pointer-events-none" />
                <input
                  id="nif"
                  name="nif"
                  type="text"
                  value={formData.nif}
                  onChange={handleInputChange}
                  className="focus:ring-angola-red focus:border-angola-red block w-full pl-10 sm:text-sm border-gray-300 rounded-md h-10"
                  placeholder={t('login.nif_placeholder') || 'Enter your NIF'}
                />
              </div>
              {errors.nif && <p className="mt-1 text-sm text-red-600">{errors.nif}</p>}
            </div>
          )}

          {activeTab === 'email' && (
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                {t('login.email') || 'Email'}
              </label>
              <div className="relative rounded-md shadow-sm">
                <AtSymbolIcon className="absolute inset-y-0 left-0 pl-3 h-5 w-5 text-gray-400 pointer-events-none" />
                <input
                  id="email"
                  name="email"
                  type="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  className="focus:ring-angola-red focus:border-angola-red block w-full pl-10 sm:text-sm border-gray-300 rounded-md h-10"
                  placeholder={t('login.email_placeholder') || 'Enter your email'}
                />
              </div>
              {errors.email && <p className="mt-1 text-sm text-red-600">{errors.email}</p>}
            </div>
          )}

          {/* Senha */}
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
              {t('login.password') || 'Password'}
            </label>
            <div className="relative rounded-md shadow-sm">
              <LockClosedIcon className="absolute inset-y-0 left-0 pl-3 h-5 w-5 text-gray-400 pointer-events-none" />
              <input
                id="password"
                name="password"
                type="password"
                value={formData.password}
                onChange={handleInputChange}
                className="focus:ring-angola-red focus:border-angola-red block w-full pl-10 sm:text-sm border-gray-300 rounded-md h-10"
                placeholder={t('login.password_placeholder') || 'Enter your password'}
              />
            </div>
            {errors.password && <p className="mt-1 text-sm text-red-600">{errors.password}</p>}
          </div>

          {/* Lembrar e Esqueci senha */}
          <div className="flex items-center justify-between">
            <label className="flex items-center text-sm text-gray-700">
              <input
                id="remember-me"
                name="rememberMe"
                type="checkbox"
                checked={formData.rememberMe}
                onChange={handleInputChange}
                className="h-4 w-4 text-angola-red focus:ring-angola-red border-gray-300 rounded"
              />
              <span className="ml-2">{t('login.remember_me') || 'Remember me'}</span>
            </label>
            <Link to="/forgot-password" className="text-sm font-medium text-angola-red hover:text-angola-red-dark transition-colors">
              {t('login.forgot_password') || 'Forgot password?'}
            </Link>
          </div>

          <Button type="submit" variant="angola-primary" block isLoading={isSubmitting}>
            <ArrowRightOnRectangleIcon className="h-5 w-5 mr-2" />
            {t('login.sign_in') || 'Sign in'}
          </Button>

          <div className="text-center text-sm">
            <span className="text-gray-600">{t('login.no_account') || "Don't have an account?"}</span>{' '}
            <Link to="/register" className="font-medium text-angola-red hover:text-angola-red-dark transition-colors">
              {t('login.create_account') || 'Create one now'}
            </Link>
          </div>
        </form>
      );
    }

    if (activeTab === 'veritas' || activeTab === 'biometric') {
      return (
        <div className="text-center py-8">
          {activeTab === 'veritas' ? (
            <FingerPrintIcon className="mx-auto h-12 w-12 text-gray-400" />
          ) : (
            <PhoneIcon className="mx-auto h-12 w-12 text-gray-400" />
          )}
          <h3 className="mt-2 text-sm font-medium text-gray-900">
            {t(`login.${activeTab}_title`) || (activeTab === 'veritas' ? 'Veritas Authentication' : 'Biometric Authentication')}
          </h3>
          <p className="mt-1 text-sm text-gray-500">
            {t(`login.${activeTab}_description`) || (activeTab === 'veritas'
              ? 'Use your Veritas credentials to sign in.'
              : 'Use your device biometrics to sign in.')}
          </p>
          <Button
            type="button"
            variant="primary"
            onClick={() => toast(t('login.coming_soon') || 'This feature is coming soon!', { icon: 'ℹ️' })}
          >
            {t(`login.${activeTab}_button`) || (activeTab === 'veritas' ? 'Sign in with Veritas' : 'Use Biometrics')}
          </Button>
        </div>
      );
    }

    return null;
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <p className="text-gray-600">{t('login.checking_auth') || 'Checking authentication...'}</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
          {t('login.title') || 'Sign in to your account'}
        </h2>
        <p className="mt-2 text-center text-sm text-gray-600">
          {t('login.subtitle') || 'Enter your credentials to access your account'}
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-6 px-4 shadow sm:rounded-lg sm:px-6">
          {/* Tabs */}
          <div className="border-b border-gray-200 mb-6">
            <nav className="-mb-px flex flex-wrap justify-center sm:justify-start" aria-label="Tabs">
              {loginMethods.map(method => (
                <button
                  key={method.id}
                  type="button"
                  onClick={() => setActiveTab(method.id)}
                  className={`${
                    activeTab === method.id
                      ? 'border-angola-red text-angola-red'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  } whitespace-nowrap py-3 px-2 sm:px-4 border-b-2 font-medium text-xs sm:text-sm flex items-center justify-center space-x-1 sm:space-x-2 min-w-0 flex-1 sm:flex-initial transition-colors duration-200`}
                >
                  <span className="flex-shrink-0">{method.icon}</span>
                  <span className="truncate">{method.label}</span>
                </button>
              ))}
            </nav>
          </div>

          {renderLoginForm()}
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
