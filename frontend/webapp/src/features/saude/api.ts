import api from '@/services/api';

export const createSaude = (data) => api.post('/api/health/', data);
export const getSaude = (id: number) => api.get(`/api/health/${id}`);
export const listSaude = () => api.get('/api/health/');
