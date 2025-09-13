import React, { createContext, useContext, useEffect, useState, useCallback } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { toast } from 'react-hot-toast';
import api from '../services/api';

type UserRole = 'citizen' | 'admin' | 'manager' | 'auditor' | null;

interface User {
  id: string;
  name: string;
  email: string;
  phone?: string;
  nif: string;
  role: UserRole;
  familyMembers?: string[]; // Array of family member IDs
  avatar?: string;
  notifications: number;
  permissions: string[];
}

interface AuthContextType {
  isAuthenticated: boolean;
  isLoading: boolean;
  user: User | null;
  token: string | null;
  login: (credentials: LoginCredentials) => Promise<void>;
  loginWithNif: (nif: string, phone: string) => Promise<void>;
  loginWithVeritas: () => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
  hasPermission: (permission: string) => boolean;
  hasAnyPermission: (permissions: string[]) => boolean;
  hasAllPermissions: (permissions: string[]) => boolean;
}

interface LoginCredentials {
  email?: string;
  password?: string;
  nif?: string;
  phone?: string;
  verificationCode?: string;
  method: 'password' | 'nif-sms' | 'veritas';
}

const AuthContext = createContext<AuthContextType>({} as AuthContextType);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(() => {
    return localStorage.getItem('authToken');
  });
  
  const navigate = useNavigate();
  const location = useLocation();

  // Initialize auth state
  useEffect(() => {
    const initializeAuth = async () => {
      const storedToken = localStorage.getItem('authToken');
      
      if (storedToken) {
        try {
          // The ApiService automatically adds the token from localStorage
          // via interceptors, so we just need to fetch user data
          const userData = await fetchUserData();
          setUser(userData);
        } catch (error) {
          console.error('Failed to authenticate with stored token', error);
          localStorage.removeItem('authToken');
        }
      }
      
      setIsLoading(false);
    };
    
    initializeAuth();
  }, []);

  // Fetch user data
  const fetchUserData = useCallback(async (): Promise<User> => {
    try {
      // Use the correct backend endpoint
      const response = await api.get('/api/v1/auth/me');
      return response.data;
    } catch (error) {
      console.error('Failed to fetch user data', error);
      throw error;
    }
  }, []);

  // Handle login with email/password
  const login = useCallback(async (credentials: LoginCredentials) => {
    try {
      setIsLoading(true);
      
      // Debug logging for development
      if (import.meta.env.MODE === 'development') {
        console.log('🔐 Login attempt with credentials:', {
          email: credentials.email,
          nif: credentials.nif,
          method: credentials.method,
          hasPassword: !!credentials.password
        });
      }
      
      // Development fallback - Check for admin credentials
      const isAdminEmail = credentials.email?.trim().toLowerCase() === 'admin@sila.gov.ao';
      const isAdminNif = credentials.nif?.trim() === '123456789';
      const isCorrectPassword = credentials.password?.trim() === 'Truman1_Marcelo1_1985';
      
      if (import.meta.env.MODE === 'development') {
        console.log('🧪 Development credential check:', {
          isAdminEmail,
          isAdminNif,
          isCorrectPassword,
          willUseMock: (isAdminEmail || isAdminNif) && isCorrectPassword
        });
      }
      
      if ((isAdminEmail || isAdminNif) && isCorrectPassword) {
        // Simulate successful admin login
        console.log('✅ Using development mock login for admin');
        const mockToken = 'mock-admin-token-' + Date.now();
        const mockUser: User = {
          id: 'admin-001',
          name: 'Administrator',
          email: 'admin@sila.gov.ao',
          nif: '123456789',
          role: 'admin',
          notifications: 3,
          permissions: ['read:all', 'write:all', 'delete:all', 'admin:access']
        };
        
        // Store token (ApiService will automatically use it via interceptors)
        localStorage.setItem('authToken', mockToken);
        
        // Update state
        setToken(mockToken);
        setUser(mockUser);
        
        // Redirect based on role or previous location
        const from = location.state?.from?.pathname || getDefaultRoute(mockUser.role);
        navigate(from, { replace: true });
        
        toast.success('Login realizado com sucesso!');
        return;
      }
      
      let response;
      
      if (credentials.method === 'password' && credentials.email && credentials.password) {
        // Use the login endpoint with JSON data
        response = await api.post('/api/v1/auth/login', {
          email: credentials.email,
          password: credentials.password
        });
      } else if (credentials.method === 'password' && credentials.nif && credentials.password) {
        // Use the login endpoint with NIF
        response = await api.post('/api/v1/auth/login', {
          nif: credentials.nif,
          password: credentials.password
        });
      } else if (credentials.method === 'nif-sms' && credentials.nif && credentials.phone) {
        response = await api.post('/api/v1/auth/nif-sms', {
          nif: credentials.nif,
          phone: credentials.phone,
          verificationCode: credentials.verificationCode,
        });
      } else {
        throw new Error('Invalid login method or missing credentials');
      }
      
      const { access_token, user } = response.data;
      
      // Store token (ApiService will automatically use it via interceptors)
      localStorage.setItem('authToken', access_token);
      
      // Update state
      setToken(access_token);
      setUser(user);
      
      // Redirect based on role or previous location
      const from = location.state?.from?.pathname || getDefaultRoute(user.role);
      navigate(from, { replace: true });
      
      toast.success('Login realizado com sucesso!');
    } catch (error) {
      console.error('Login failed:', error);
      
      // Enhanced error handling for development
      if (import.meta.env.MODE === 'development') {
        console.log('🚫 API login failed, this is normal if backend is not running');
        console.log('💡 To use mock login, ensure you use the correct admin credentials:');
        console.log('   Email: admin@sila.gov.ao');
        console.log('   NIF: 123456789');
        console.log('   Password: Truman1_Marcelo1_1985');
        
        // Check if it's a network error (backend not running)
        if ((error as any)?.code === 'ERR_NETWORK' || (error as any)?.code === 'ERR_BAD_REQUEST') {
          toast.error('Backend não está rodando. Use as credenciais de desenvolvimento: admin@sila.gov.ao');
        } else {
          toast.error('Falha no login. Verifique suas credenciais e tente novamente.');
        }
      } else {
        toast.error('Falha no login. Verifique suas credenciais e tente novamente.');
      }
      throw error;
    } finally {
      setIsLoading(false);
    }
  }, [navigate, location.state]);

  // Login with NIF + SMS
  const loginWithNif = useCallback(async (nif: string, phone: string) => {
    try {
      setIsLoading(true);
      // Send verification code via SMS
      await api.post('/api/v1/auth/send-verification-code', { nif, phone });
      toast.success('Código de verificação enviado para o seu telefone');
    } catch (error) {
      console.error('Failed to send verification code:', error);
      toast.error('Falha ao enviar código de verificação');
      throw error;
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Login with Veritas.ID
  const loginWithVeritas = useCallback(async () => {
    try {
      setIsLoading(true);
      // Initiate Veritas.ID flow
      window.location.href = `${import.meta.env.VITE_API_URL}/api/v1/auth/veritas`;
    } catch (error) {
      console.error('Veritas login failed:', error);
      toast.error('Falha ao iniciar autenticação Veritas.ID');
      throw error;
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Logout
  const logout = useCallback(() => {
    // ApiService will automatically handle token removal via interceptors
    localStorage.removeItem('authToken');
    setToken(null);
    setUser(null);
    navigate('/login');
    toast('Até logo!', { icon: '👋' });
  }, [navigate]);

  // Refresh user data
  const refreshUser = useCallback(async () => {
    if (!token) return;
    
    try {
      const userData = await fetchUserData();
      setUser(userData);
    } catch (error) {
      console.error('Failed to refresh user data', error);
      logout();
    }
  }, [token, fetchUserData, logout]);

  // Check if user has a specific permission
  const hasPermission = useCallback((permission: string): boolean => {
    if (!user) return false;
    return user.permissions.includes(permission);
  }, [user]);

  // Check if user has any of the specified permissions
  const hasAnyPermission = useCallback((permissions: string[]): boolean => {
    if (!user) return false;
    return permissions.some(permission => user.permissions.includes(permission));
  }, [user]);

  // Check if user has all the specified permissions
  const hasAllPermissions = useCallback((permissions: string[]): boolean => {
    if (!user) return false;
    return permissions.every(permission => user.permissions.includes(permission));
  }, [user]);

  // Get default route based on user role
  const getDefaultRoute = (role: UserRole): string => {
    switch (role) {
      case 'admin':
      case 'manager':
        return '/admin/dashboard';
      case 'auditor':
        return '/admin/audits';
      case 'citizen':
      default:
        return '/dashboard';
    }
  };

  const value = {
    isAuthenticated: !!user,
    isLoading,
    user,
    token,
    login,
    loginWithNif,
    loginWithVeritas,
    logout,
    refreshUser,
    hasPermission,
    hasAnyPermission,
    hasAllPermissions,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
