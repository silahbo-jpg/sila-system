// Configurações da aplicação
const config = {
  // Configurações da API
  api: {
    baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
    timeout: 30000,
    enableLogging: import.meta.env.VITE_ENABLE_LOGGING === 'true',
    version: import.meta.env.VITE_APP_VERSION || '1.0.0',
  },
  
  // Configurações de monitoramento
  monitoring: {
    sentry: {
      dsn: import.meta.env.VITE_SENTRY_DSN || '',
      environment: import.meta.env.MODE || 'development',
      release: `frontend@${import.meta.env.VITE_APP_VERSION || '1.0.0'}`,
      tracesSampleRate: 1.0,
    },
    googleAnalytics: {
      id: import.meta.env.VITE_GOOGLE_ANALYTICS_ID || '',
    },
  },
  
  // Configurações de recursos
  features: {
    // Habilita/desabilita funcionalidades específicas
    enableAnalytics: false,
    enableErrorTracking: true,
    enablePerformanceMonitoring: true,
  },
};

export default config;

