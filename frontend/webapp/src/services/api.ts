import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';

// Configuração base da API
const API_BASE_URL = 'http://localhost:8000';

// Interface para resposta padrão da API
interface ApiResponse<T = any> {
  data: T;
  message?: string;
  status: 'success' | 'error';
}

// Interface para erro da API
interface ApiError {
  detail: string;
  status_code: number;
  errors?: Record<string, string[]>;
}

// Classe para gerenciar a API
class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.setupInterceptors();
  }

  private setupInterceptors() {
    // Request interceptor para adicionar token de autenticação
    this.api.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('authToken');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor para tratamento de erros
    this.api.interceptors.response.use(
      (response: AxiosResponse) => {
        return response;
      },
      async (error) => {
        const originalRequest = error.config;

        // Se o erro for 401 (não autorizado) e não for uma tentativa de refresh
        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;

          try {
            // Tentar renovar o token
            const refreshToken = localStorage.getItem('refreshToken');
            if (refreshToken) {
              const response = await axios.post(`${API_BASE_URL}/api/v1/auth/refresh`, {
                refresh_token: refreshToken,
              });

              const { access_token } = response.data;
              localStorage.setItem('authToken', access_token);

              // Reenviar a requisição original com o novo token
              originalRequest.headers.Authorization = `Bearer ${access_token}`;
              return this.api(originalRequest);
            }
          } catch (refreshError) {
            // Se falhar ao renovar, limpar tokens e redirecionar para login
            localStorage.removeItem('authToken');
            localStorage.removeItem('refreshToken');
            window.location.href = '/login';
          }
        }

        return Promise.reject(error);
      }
    );
  }

  // Métodos HTTP genéricos
  async get<T = any>(url: string, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> {
    return this.api.get<T>(url, config);
  }

  async post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> {
    return this.api.post<T>(url, data, config);
  }

  async put<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> {
    return this.api.put<T>(url, data, config);
  }

  async patch<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> {
    return this.api.patch<T>(url, data, config);
  }

  async delete<T = any>(url: string, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> {
    return this.api.delete<T>(url, config);
  }

  // Métodos específicos para autenticação
  async login(credentials: { email: string; password: string }) {
    const response = await this.post('/api/v1/auth/login', credentials);
    return response.data;
  }

  async loginWithNif(data: { nif: string; phone: string; verificationCode?: string }) {
    const response = await this.post('/api/v1/auth/login/nif-sms', data);
    return response.data;
  }

  async sendVerificationCode(data: { nif: string; phone: string }) {
    const response = await this.post('/api/v1/auth/send-verification-code', data);
    return response.data;
  }

  async register(userData: any) {
    const response = await this.post('/api/v1/auth/register', userData);
    return response.data;
  }

  async getCurrentUser() {
    const response = await this.get('/api/v1/auth/me');
    return response.data;
  }

  async logout() {
    const response = await this.post('/api/v1/auth/logout');
    return response.data;
  }

  // Métodos específicos para cidadania
  async getCitizens(params?: any) {
    const response = await this.get('/api/citizenship/citizens/', { params });
    return response.data;
  }

  async createCitizen(citizenData: any) {
    const response = await this.post('/api/citizenship/citizens/', citizenData);
    return response.data;
  }

  async getCitizen(id: number) {
    const response = await this.get(`/api/citizenship/citizens/${id}`);
    return response.data;
  }

  async updateCitizen(id: number, citizenData: any) {
    const response = await this.put(`/api/citizenship/citizens/${id}`, citizenData);
    return response.data;
  }

  async deleteCitizen(id: number) {
    const response = await this.delete(`/api/citizenship/citizens/${id}`);
    return response.data;
  }

  async createAtestado(atestadoData: any) {
    const response = await this.post('/api/citizenship/atestado/', atestadoData);
    return response.data;
  }

  async getAtestado(id: number) {
    const response = await this.get(`/api/citizenship/atestado/${id}`);
    return response.data;
  }

  async downloadAtestadoPDF(id: number) {
    const response = await this.get(`/api/citizenship/atestado/${id}/pdf`, {
      responseType: 'blob',
    });
    return response.data;
  }

  // Métodos específicos para educação
  async getSchools(params?: any) {
    const response = await this.get('/api/education/schools/', { params });
    return response.data;
  }

  async createEnrollment(enrollmentData: any) {
    const response = await this.post('/api/education/enrollments/', enrollmentData);
    return response.data;
  }

  async getEnrollment(id: number) {
    const response = await this.get(`/api/education/enrollments/${id}`);
    return response.data;
  }

  async getStudentGrades(studentId: number) {
    const response = await this.get(`/api/education/students/${studentId}/grades`);
    return response.data;
  }

  // Métodos específicos para saúde
  async getHealthUnits(params?: any) {
    const response = await this.get('/api/health/units/', { params });
    return response.data;
  }

  async createAppointment(appointmentData: any) {
    const response = await this.post('/api/health/appointments/', appointmentData);
    return response.data;
  }

  async getAppointments(params?: any) {
    const response = await this.get('/api/health/appointments/', { params });
    return response.data;
  }

  // Métodos específicos para urbanismo
  async getLicenses(params?: any) {
    const response = await this.get('/api/urbanism/licenses/', { params });
    return response.data;
  }

  async createLicense(licenseData: any) {
    const response = await this.post('/api/urbanism/licenses/', licenseData);
    return response.data;
  }

  async getLicense(id: number) {
    const response = await this.get(`/api/urbanism/licenses/${id}`);
    return response.data;
  }

  // Métodos específicos para comércio
  async getBusinessLicenses(params?: any) {
    const response = await this.get('/api/commercial/licenses/', { params });
    return response.data;
  }

  async createBusinessLicense(licenseData: any) {
    const response = await this.post('/api/commercial/licenses/', licenseData);
    return response.data;
  }

  // Métodos para upload de arquivos
  async uploadFile(file: File, endpoint: string) {
    const formData = new FormData();
    formData.append('file', file);

    const response = await this.post(endpoint, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }

  // Métodos para notificações
  async getNotifications(params?: any) {
    const response = await this.get('/api/notifications/', { params });
    return response.data;
  }

  async markNotificationAsRead(id: number) {
    const response = await this.patch(`/api/notifications/${id}/read`);
    return response.data;
  }

  // Métodos para relatórios
  async getReports(params?: any) {
    const response = await this.get('/api/reports/', { params });
    return response.data;
  }

  async generateReport(reportData: any) {
    const response = await this.post('/api/reports/generate', reportData);
    return response.data;
  }

  // Métodos para estatísticas
  async getStatistics(params?: any) {
    const response = await this.get('/api/statistics/', { params });
    return response.data;
  }

  // Métodos para dashboard
  async getDashboardData() {
    const response = await this.get('/api/dashboard/');
    return response.data;
  }

  // Métodos para dashboard v2
  async getDashboardResumo(municipio_id?: number, periodo: string = 'mes') {
    const params = new URLSearchParams();
    if (municipio_id) params.append('municipio_id', municipio_id.toString());
    params.append('periodo', periodo);
    
    const response = await this.get(`/v2/dashboard/resumo?${params.toString()}`);
    return response.data;
  }

  async getDashboardMunicipios() {
    const response = await this.get('/v2/dashboard/municipios');
    return response.data;
  }

  // Métodos para configurações
  async getSettings() {
    const response = await this.get('/api/settings/');
    return response.data;
  }

  async updateSettings(settingsData: any) {
    const response = await this.put('/api/settings/', settingsData);
    return response.data;
  }

  // Métodos para logs e auditoria
  async getAuditLogs(params?: any) {
    const response = await this.get('/api/audit/logs/', { params });
    return response.data;
  }

  // Métodos para backup e restauração
  async createBackup() {
    const response = await this.post('/api/backup/create');
    return response.data;
  }

  async restoreBackup(backupId: string) {
    const response = await this.post(`/api/backup/${backupId}/restore`);
    return response.data;
  }

  // Métodos para sincronização mobile
  async syncOfflineData(data: any) {
    const response = await this.post('/api/sync/offline', data);
    return response.data;
  }

  async getSyncStatus() {
    const response = await this.get('/api/sync/status');
    return response.data;
  }

  // Métodos para PWA
  async getServiceWorkerUpdate() {
    const response = await this.get('/api/pwa/update');
    return response.data;
  }

  async registerServiceWorker() {
    const response = await this.post('/api/pwa/register');
    return response.data;
  }
}

// Instância única do serviço de API
const apiService = new ApiService();

// Exportar a instância e a classe
export default apiService;
export { ApiService, type ApiResponse, type ApiError };
