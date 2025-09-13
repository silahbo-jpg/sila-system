// Serviço de análise e métricas para o frontend
import * as Sentry from '@sentry/react';
import config from '../../config';

/**
 * Inicializa os serviços de monitoramento (Sentry, Google Analytics, etc.)
 */
export function initializeMonitoring() {
  // Inicializa o Sentry para rastreamento de erros e desempenho
  if (config.monitoring.sentry.dsn) {
    Sentry.init({
      dsn: config.monitoring.sentry.dsn,
      environment: config.monitoring.sentry.environment,
      release: config.monitoring.sentry.release,
      tracesSampleRate: config.monitoring.sentry.tracesSampleRate,
      integrations: [
        new Sentry.BrowserTracing({
          // Opções adicionais de rastreamento
        }),
      ],
    });
    
    console.log('Monitoramento Sentry inicializado');
  }

  // Inicializa o Google Analytics, se configurado
  if (config.monitoring.googleAnalytics.id) {
    // Adiciona o script do Google Analytics
    const script = document.createElement('script');
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtag/js?id=${config.monitoring.googleAnalytics.id}`;
    document.head.appendChild(script);

    // Inicializa o objeto gtag
    window.dataLayer = window.dataLayer || [];
    function gtag() {
      // @ts-ignore
      window.dataLayer.push(arguments);
    }
    // @ts-ignore
    window.gtag = gtag;
    // @ts-ignore
    gtag('js', new Date());
    // @ts-ignore
    gtag('config', config.monitoring.googleAnalytics.id);
    
    console.log('Google Analytics inicializado');
  }
}

/**
 * Registra um erro no serviço de monitoramento
 * @param error - O erro a ser registrado
 * @param context - Contexto adicional para o erro
 */
export function captureError(error: Error, context: Record<string, any> = {}) {
  console.error('Erro capturado:', error, context);
  
  if (config.monitoring.sentry.dsn) {
    Sentry.withScope((scope) => {
      Object.entries(context).forEach(([key, value]) => {
        scope.setExtra(key, value);
      });
      Sentry.captureException(error);
    });
  }
}

/**
 * Registra um evento de negócio
 * @param name - Nome do evento
 * @param properties - Propriedades adicionais do evento
 */
export function trackEvent(name: string, properties: Record<string, any> = {}) {
  if (config.monitoring.googleAnalytics.id) {
    // @ts-ignore
    window.gtag('event', name, properties);
  }
  
  if (config.monitoring.sentry.dsn) {
    Sentry.addBreadcrumb({
      category: 'event',
      message: name,
      level: 'info',
      data: properties,
    });
  }
  
  if (config.api.enableLogging) {
    console.log(`[Evento] ${name}`, properties);
  }
}

/**
 * Registra uma métrica de desempenho
 * @param name - Nome da métrica
 * @param value - Valor da métrica
 * @param tags - Tags adicionais para classificação
 */
export function trackMetric(
  name: string, 
  value: number, 
  tags: Record<string, string> = {}
) {
  if (config.monitoring.sentry.dsn) {
    Sentry.metrics.distribution(name, value, {
      unit: 'millisecond',
      tags,
    });
  }
  
  if (config.api.enableLogging) {
    console.log(`[Métrica] ${name}: ${value}ms`, tags);
  }
}

/**
 * Define o usuário atual para rastreamento
 * @param user - Dados do usuário
 */
export function setUser(user: {
  id: string | number;
  email?: string;
  username?: string;
  [key: string]: any;
}) {
  if (config.monitoring.sentry.dsn) {
    Sentry.setUser({
      id: String(user.id),
      email: user.email,
      username: user.username,
    });
  }
  
  if (config.monitoring.googleAnalytics.id) {
    // @ts-ignore
    window.gtag('set', 'user_properties', {
      user_id: user.id,
      email: user.email,
      username: user.username,
    });
  }
}

/**
 * Limpa os dados do usuário (para logout)
 */
export function clearUser() {
  if (config.monitoring.sentry.dsn) {
    Sentry.setUser(null);
  }
  
  if (config.monitoring.googleAnalytics.id) {
    // @ts-ignore
    window.gtag('set', 'user_properties', null);
  }
}

// Exporta o objeto Sentry para uso direto, se necessário
export { Sentry };

