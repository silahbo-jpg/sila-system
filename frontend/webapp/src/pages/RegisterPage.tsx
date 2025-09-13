import React, { useState } from 'react';
import { useNavigate, useLocation, Link } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { useAuth } from '../context/AuthContext';
import { MainLayout } from '../layouts/MainLayout';
import Button from '../components/ui/Button';
import Input from '../components/ui/Input';
import LoadingSpinner from '../components/common/LoadingSpinner';

interface RegisterFormData {
  name: string;
  email: string;
  nif: string;
  phone: string;
  password: string;
  confirmPassword: string;
  acceptTerms: boolean;
}

const RegisterPage: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { login } = useAuth();
  
  const [isLoading, setIsLoading] = useState(false);
  const [authMethod, setAuthMethod] = useState<'email' | 'nif-sms' | 'veritas'>('email');
  const [verificationStep, setVerificationStep] = useState<'form' | 'verification'>('form');
  const [verificationCode, setVerificationCode] = useState('');

  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
    setValue
  } = useForm<RegisterFormData>();

  const password = watch('password');

  const onSubmit = async (data: RegisterFormData) => {
    try {
      setIsLoading(true);
      
      if (authMethod === 'email') {
        // Registro com email/senha
        await registerWithEmail(data);
      } else if (authMethod === 'nif-sms') {
        // Enviar código SMS
        await sendSmsCode(data.nif, data.phone);
        setVerificationStep('verification');
      } else if (authMethod === 'veritas') {
        // Redirecionar para Veritas.ID
        await redirectToVeritas();
      }
    } catch (error) {
      console.error('Registration failed:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const registerWithEmail = async (data: RegisterFormData) => {
    // Implementar chamada para API de registro
    console.log('Registering with email:', data);
    
    // Simular sucesso e fazer login
    await login({
      method: 'password',
      email: data.email,
      password: data.password
    });
  };

  const sendSmsCode = async (nif: string, phone: string) => {
    // Implementar envio de código SMS
    console.log('Sending SMS code to:', phone);
  };

  const redirectToVeritas = async () => {
    // Redirecionar para Veritas.ID
    window.location.href = `${import.meta.env.VITE_API_URL}/api/auth/veritas/register`;
  };

  const verifySmsCode = async () => {
    try {
      setIsLoading(true);
      
      // Verificar código SMS
      console.log('Verifying SMS code:', verificationCode);
      
      // Se válido, fazer login
      await login({
        method: 'nif-sms',
        nif: watch('nif'),
        phone: watch('phone'),
        verificationCode
      });
    } catch (error) {
      console.error('SMS verification failed:', error);
    } finally {
      setIsLoading(false);
    }
  };

  if (verificationStep === 'verification') {
    return (
      <MainLayout>
        <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
          <div className="max-w-md w-full space-y-8">
            <div>
              <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
                Verificar telefone
              </h2>
              <p className="mt-2 text-center text-sm text-gray-600">
                Digite o código enviado para {watch('phone')}
              </p>
            </div>
            
            <div className="mt-8 space-y-6">
              <div>
                <Input
                  type="text"
                  placeholder="Código de verificação"
                  value={verificationCode}
                  onChange={(e) => setVerificationCode(e.target.value)}
                  maxLength={6}
                  className="text-center text-2xl tracking-widest"
                />
              </div>
              
              <div className="flex space-x-4">
                <Button
                  variant="outline"
                  onClick={() => setVerificationStep('form')}
                  className="flex-1"
                >
                  Voltar
                </Button>
                <Button
                  variant="primary"
                  onClick={verifySmsCode}
                  disabled={verificationCode.length !== 6 || isLoading}
                  className="flex-1"
                >
                  {isLoading ? <LoadingSpinner size="sm" /> : 'Verificar'}
                </Button>
              </div>
              
              <div className="text-center">
                <button
                  type="button"
                  className="text-sm text-blue-600 hover:text-blue-500"
                  onClick={() => sendSmsCode(watch('nif'), watch('phone'))}
                >
                  Reenviar código
                </button>
              </div>
            </div>
          </div>
        </div>
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full space-y-8">
          <div>
            <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
              Criar conta
            </h2>
            <p className="mt-2 text-center text-sm text-gray-600">
              Escolha como deseja se registrar
            </p>
          </div>
          
          {/* Métodos de autenticação */}
          <div className="space-y-4">
            <button
              type="button"
              onClick={() => setAuthMethod('email')}
              className={`w-full p-4 border rounded-lg text-left transition-colors ${
                authMethod === 'email'
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-300 hover:border-gray-400'
              }`}
            >
              <div className="flex items-center">
                <svg className="h-6 w-6 text-gray-400 mr-3" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z" />
                  <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" />
                </svg>
                <div>
                  <h3 className="font-medium text-gray-900">Email e senha</h3>
                  <p className="text-sm text-gray-500">Registre-se com email e senha</p>
                </div>
              </div>
            </button>
            
            <button
              type="button"
              onClick={() => setAuthMethod('nif-sms')}
              className={`w-full p-4 border rounded-lg text-left transition-colors ${
                authMethod === 'nif-sms'
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-300 hover:border-gray-400'
              }`}
            >
              <div className="flex items-center">
                <svg className="h-6 w-6 text-gray-400 mr-3" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z" />
                </svg>
                <div>
                  <h3 className="font-medium text-gray-900">NIF + SMS</h3>
                  <p className="text-sm text-gray-500">Registre-se com NIF e código SMS</p>
                </div>
              </div>
            </button>
            
            <button
              type="button"
              onClick={() => setAuthMethod('veritas')}
              className={`w-full p-4 border rounded-lg text-left transition-colors ${
                authMethod === 'veritas'
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-300 hover:border-gray-400'
              }`}
            >
              <div className="flex items-center">
                <svg className="h-6 w-6 text-gray-400 mr-3" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clipRule="evenodd" />
                </svg>
                <div>
                  <h3 className="font-medium text-gray-900">Veritas.ID</h3>
                  <p className="text-sm text-gray-500">Registre-se com Veritas.ID</p>
                </div>
              </div>
            </button>
          </div>
          
          {/* Formulário de registro */}
          <form className="mt-8 space-y-6" onSubmit={handleSubmit(onSubmit)}>
            {authMethod === 'email' && (
              <>
                <Input
                  label="Nome completo"
                  {...register('name', { required: 'Nome é obrigatório' })}
                  error={errors.name?.message}
                />
                
                <Input
                  label="Email"
                  type="email"
                  {...register('email', { 
                    required: 'Email é obrigatório',
                    pattern: {
                      value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                      message: 'Email inválido'
                    }
                  })}
                  error={errors.email?.message}
                />
                
                <Input
                  label="NIF"
                  {...register('nif', { 
                    required: 'NIF é obrigatório',
                    pattern: {
                      value: /^\d{9}$/,
                      message: 'NIF deve ter 9 dígitos'
                    }
                  })}
                  error={errors.nif?.message}
                />
                
                <Input
                  label="Senha"
                  type="password"
                  {...register('password', { 
                    required: 'Senha é obrigatória',
                    minLength: {
                      value: 8,
                      message: 'Senha deve ter pelo menos 8 caracteres'
                    }
                  })}
                  error={errors.password?.message}
                />
                
                <Input
                  label="Confirmar senha"
                  type="password"
                  {...register('confirmPassword', { 
                    required: 'Confirmação de senha é obrigatória',
                    validate: value => value === password || 'Senhas não coincidem'
                  })}
                  error={errors.confirmPassword?.message}
                />
              </>
            )}
            
            {authMethod === 'nif-sms' && (
              <>
                <Input
                  label="Nome completo"
                  {...register('name', { required: 'Nome é obrigatório' })}
                  error={errors.name?.message}
                />
                
                <Input
                  label="NIF"
                  {...register('nif', { 
                    required: 'NIF é obrigatório',
                    pattern: {
                      value: /^\d{9}$/,
                      message: 'NIF deve ter 9 dígitos'
                    }
                  })}
                  error={errors.nif?.message}
                />
                
                <Input
                  label="Telefone"
                  {...register('phone', { 
                    required: 'Telefone é obrigatório',
                    pattern: {
                      value: /^(\+351)?\s?9\d{8}$/,
                      message: 'Telefone inválido'
                    }
                  })}
                  error={errors.phone?.message}
                />
              </>
            )}
            
            {authMethod === 'veritas' && (
              <div className="text-center">
                <p className="text-sm text-gray-600 mb-4">
                  Você será redirecionado para o Veritas.ID para completar seu registro.
                </p>
              </div>
            )}
            
            <div className="flex items-center">
              <input
                id="accept-terms"
                type="checkbox"
                {...register('acceptTerms', { 
                  required: 'Você deve aceitar os termos'
                })}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label htmlFor="accept-terms" className="ml-2 block text-sm text-gray-900">
                Aceito os{' '}
                <a href="#" className="text-blue-600 hover:text-blue-500">
                  termos de uso
                </a>{' '}
                e{' '}
                <a href="#" className="text-blue-600 hover:text-blue-500">
                  política de privacidade
                </a>
              </label>
            </div>
            
            {errors.acceptTerms && (
              <p className="text-sm text-red-600">{errors.acceptTerms.message}</p>
            )}
            
            <Button
              type="submit"
              variant="primary"
              disabled={isLoading}
              className="w-full"
            >
              {isLoading ? <LoadingSpinner size="sm" /> : 'Criar conta'}
            </Button>
          </form>
          
          <div className="text-center">
            <p className="text-sm text-gray-600">
              Já tem uma conta?{' '}
              <Link
                to="/login"
                className="font-medium text-blue-600 hover:text-blue-500"
              >
                Fazer login
              </Link>
            </p>
          </div>
        </div>
      </div>
    </MainLayout>
  );
};

export default RegisterPage; 
