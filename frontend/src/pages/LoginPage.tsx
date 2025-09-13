import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { 
  EyeIcon, 
  EyeSlashIcon, 
  LockClosedIcon,
  UserIcon,
  ExclamationTriangleIcon,
  ShieldCheckIcon
} from '@heroicons/react/24/outline';

interface LoginForm {
  email: string;
  password: string;
  remember: boolean;
}

interface LoginError {
  message: string;
  field?: string;
}

const LoginPage: React.FC = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const location = useLocation();
  
  const [form, setForm] = useState<LoginForm>({
    email: '',
    password: '',
    remember: false
  });
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<LoginError | null>(null);

  // Get the intended destination or default to dashboard
  const from = (location.state as any)?.from?.pathname || '/dashboard';

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;
    setForm(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
    
    // Clear error when user starts typing
    if (error) setError(null);
  };

  const validateForm = (): boolean => {
    if (!form.email) {
      setError({ message: t('login.errors.emailRequired'), field: 'email' });
      return false;
    }
    
    if (!form.email.includes('@')) {
      setError({ message: t('login.errors.emailInvalid'), field: 'email' });
      return false;
    }
    
    if (!form.password) {
      setError({ message: t('login.errors.passwordRequired'), field: 'password' });
      return false;
    }
    
    if (form.password.length < 6) {
      setError({ message: t('login.errors.passwordTooShort'), field: 'password' });
      return false;
    }
    
    return true;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) return;
    
    setIsLoading(true);
    setError(null);

    try {
      // Simulate API call to backend authentication endpoint
      const response = await fetch('/api/v1/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: form.email,
          password: form.password,
          remember: form.remember
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || t('login.errors.loginFailed'));
      }

      const data = await response.json();
      
      // Store JWT token
      if (form.remember) {
        localStorage.setItem('sila_token', data.access_token);
      } else {
        sessionStorage.setItem('sila_token', data.access_token);
      }
      
      // Store user info
      localStorage.setItem('sila_user', JSON.stringify(data.user));
      
      // Redirect to intended destination
      navigate(from, { replace: true });
      
    } catch (err) {
      console.error('Login error:', err);
      setError({ 
        message: err instanceof Error ? err.message : t('login.errors.networkError') 
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleForgotPassword = () => {
    // In a real app, this would navigate to password reset
    alert(t('login.forgotPassword.comingSoon'));
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-sila-primary to-sila-secondary flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        {/* Logo and Title */}
        <div className="text-center">
          <div className="mx-auto w-16 h-16 bg-white rounded-full flex items-center justify-center shadow-lg">
            <div className="w-10 h-10 bg-sila-primary rounded-full flex items-center justify-center">
              <span className="text-white font-bold text-lg">AO</span>
            </div>
          </div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-white">
            {t('login.title')}
          </h2>
          <p className="mt-2 text-center text-sm text-sila-light">
            {t('login.subtitle')}
          </p>
        </div>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow-xl rounded-lg sm:px-10">
          <form className="space-y-6" onSubmit={handleSubmit}>
            {/* Global Error */}
            {error && !error.field && (
              <div className="rounded-md bg-red-50 p-4">
                <div className="flex">
                  <ExclamationTriangleIcon className="h-5 w-5 text-red-400" />
                  <div className="ml-3">
                    <p className="text-sm text-red-800">{error.message}</p>
                  </div>
                </div>
              </div>
            )}

            {/* Email Field */}
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                {t('login.form.email')}
              </label>
              <div className="mt-1 relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <UserIcon className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  value={form.email}
                  onChange={handleInputChange}
                  className={`appearance-none block w-full pl-10 pr-3 py-2 border rounded-md placeholder-gray-400 focus:outline-none focus:ring-sila-primary focus:border-sila-primary sm:text-sm ${
                    error?.field === 'email' ? 'border-red-300' : 'border-gray-300'
                  }`}
                  placeholder={t('login.form.emailPlaceholder')}
                />
              </div>
              {error?.field === 'email' && (
                <p className="mt-1 text-sm text-red-600">{error.message}</p>
              )}
            </div>

            {/* Password Field */}
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                {t('login.form.password')}
              </label>
              <div className="mt-1 relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <LockClosedIcon className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  id="password"
                  name="password"
                  type={showPassword ? 'text' : 'password'}
                  autoComplete="current-password"
                  required
                  value={form.password}
                  onChange={handleInputChange}
                  className={`appearance-none block w-full pl-10 pr-10 py-2 border rounded-md placeholder-gray-400 focus:outline-none focus:ring-sila-primary focus:border-sila-primary sm:text-sm ${
                    error?.field === 'password' ? 'border-red-300' : 'border-gray-300'
                  }`}
                  placeholder={t('login.form.passwordPlaceholder')}
                />
                <button
                  type="button"
                  className="absolute inset-y-0 right-0 pr-3 flex items-center"
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? (
                    <EyeSlashIcon className="h-5 w-5 text-gray-400 hover:text-gray-600" />
                  ) : (
                    <EyeIcon className="h-5 w-5 text-gray-400 hover:text-gray-600" />
                  )}
                </button>
              </div>
              {error?.field === 'password' && (
                <p className="mt-1 text-sm text-red-600">{error.message}</p>
              )}
            </div>

            {/* Remember Me & Forgot Password */}
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <input
                  id="remember"
                  name="remember"
                  type="checkbox"
                  checked={form.remember}
                  onChange={handleInputChange}
                  className="h-4 w-4 text-sila-primary focus:ring-sila-primary border-gray-300 rounded"
                />
                <label htmlFor="remember" className="ml-2 block text-sm text-gray-900">
                  {t('login.form.rememberMe')}
                </label>
              </div>

              <div className="text-sm">
                <button
                  type="button"
                  onClick={handleForgotPassword}
                  className="font-medium text-sila-primary hover:text-sila-secondary"
                >
                  {t('login.form.forgotPassword')}
                </button>
              </div>
            </div>

            {/* Submit Button */}
            <div>
              <button
                type="submit"
                disabled={isLoading}
                className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-sila-primary hover:bg-sila-secondary focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-sila-primary disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <span className="absolute left-0 inset-y-0 flex items-center pl-3">
                  <ShieldCheckIcon className="h-5 w-5 text-sila-light group-hover:text-white" />
                </span>
                {isLoading ? t('common.loading') : t('login.form.submit')}
              </button>
            </div>
          </form>

          {/* Additional Options */}
          <div className="mt-6">
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-300" />
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-2 bg-white text-gray-500">
                  {t('login.or')}
                </span>
              </div>
            </div>

            <div className="mt-6 text-center">
              <p className="text-sm text-gray-600">
                {t('login.noAccount')}{' '}
                <Link
                  to="/register"
                  className="font-medium text-sila-primary hover:text-sila-secondary"
                >
                  {t('login.createAccount')}
                </Link>
              </p>
            </div>

            {/* Help Links */}
            <div className="mt-4 text-center space-y-2">
              <Link
                to="/help"
                className="text-xs text-gray-500 hover:text-sila-primary"
              >
                {t('login.help.needHelp')}
              </Link>
              <br />
              <Link
                to="/accessibility"
                className="text-xs text-gray-500 hover:text-sila-primary"
              >
                {t('login.help.accessibility')}
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="mt-8 text-center">
        <p className="text-xs text-sila-light">
          {t('login.footer.security')}
        </p>
      </div>
    </div>
  );
};

export default LoginPage;