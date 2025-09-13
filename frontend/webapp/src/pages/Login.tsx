import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';
import { loginSchema, LoginFormData } from '../validations/loginSchema';
import { Form, Input, Button } from '../components/ui';

function Login() {
  const navigate = useNavigate();
  const { setToken, setRole } = useAuth();
  const [loading, setLoading] = useState(false);
  const [apiError, setApiError] = useState('');
  
  const {
    register,
    handleSubmit,
    formState: { errors },
    setError: setFormError,
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
    mode: 'onChange',
  });

  const onSubmit = async (data: LoginFormData) => {
    setLoading(true);
    setApiError('');
    
    try {
      const params = new URLSearchParams();
      params.append('username', data.username);
      params.append('password', data.password);
      
      const res = await api.post('/auth/login', params, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      });
      
      console.log('Resposta do login:', res.data);
      const token = res.data.token || res.data.access_token;
      
      if (res.data && token) {
        localStorage.setItem('token', token);
        setToken(token);
        setRole(res.data.role || null);
        navigate('/dashboard');
      } else {
        setApiError('Login falhou: token não recebido na resposta.');
      }
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Erro ao conectar com o servidor. Verifique se o backend está rodando.';
      setApiError(errorMessage);
      console.error('Erro no login:', err.response?.data || err);
      
      // Define erros específicos de validação para os campos
      if (err.response?.data?.detail === 'Incorrect username or password') {
        setFormError('password', {
          type: 'manual',
          message: 'Nome de usuário ou senha incorretos',
        });
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-screen flex items-center justify-center bg-gray-100 p-4">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800">SILA-HBO</h1>
          <p className="text-gray-600 mt-2">Sistema Integrado de Licenciamento e Apoio</p>
        </div>

        {/* Mensagem de erro da API */}
        {apiError && (
          <div className="mb-6 p-4 bg-red-50 border-l-4 border-red-500 text-red-700 rounded-r">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-500" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm">{apiError}</p>
              </div>
            </div>
          </div>
        )}

        <Form methods={methods} onSubmit={onSubmit}>
          <Input
            label="Nome de Usuário"
            id="username"
            type="text"
            placeholder="Digite seu nome de usuário"
            error={errors.username}
            register={register('username')}
            disabled={loading}
            autoComplete="username"
            required
          />

          <div className="mb-6">
            <Input
              label="Senha"
              id="password"
              type="password"
              placeholder="••••••••"
              error={errors.password}
              register={register('password')}
              disabled={loading}
              autoComplete="current-password"
              required
            />
            <div className="flex justify-end mt-1">
              <a
                href="#"
                className="text-sm text-blue-600 hover:text-blue-800 hover:underline"
                onClick={(e) => {
                  e.preventDefault();
                  // Adicionar lógica de recuperação de senha aqui
                }}
              >
                Esqueceu a senha?
              </a>
            </div>
          </div>

          <div className="flex flex-col space-y-4">
            <Button
              type="submit"
              variant="primary"
              size="lg"
              isLoading={loading}
              fullWidth
            >
              Entrar na plataforma
            </Button>
          </div>
        </Form>
      </div>
    </div>
  );
}

export default Login;
