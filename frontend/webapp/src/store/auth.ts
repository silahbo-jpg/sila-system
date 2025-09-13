import { create } from 'zustand';
import api from '../services/api';

export type Role = 'admin' | 'operador' | 'cidadao';

interface User {
  id: string; name: string; email: string; roles: Role[]; status: 'active'|'inactive';
}

interface AuthState {
  user: User | null;
  accessToken: string | null;
  refreshToken: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  hasRole: (roles: Role|Role[]) => boolean;
}

export const useAuth = create<AuthState>((set, get) => ({
  user: null,
  accessToken: localStorage.getItem('auth:accessToken'),
  refreshToken: localStorage.getItem('auth:refreshToken'),
  async login(email, password) {
    const { data } = await api.post('/auth/login', { email, password });
    localStorage.setItem('auth:accessToken', data.access_token);
    localStorage.setItem('auth:refreshToken', data.refresh_token);
    set({ accessToken: data.access_token, refreshToken: data.refresh_token });
    const me = await api.get('/auth/me');
    set({ user: me.data });
  },
  logout() {
    localStorage.removeItem('auth:accessToken');
    localStorage.removeItem('auth:refreshToken');
    set({ user: null, accessToken: null, refreshToken: null });
    window.location.href = '/login';
  },
  hasRole(roles) {
    const u = get().user; if (!u) return false;
    const want = Array.isArray(roles) ? roles : [roles];
    return u.roles.some(r => want.includes(r));
  }
}));

