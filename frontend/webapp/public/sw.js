// Service Worker para SILA System
const CACHE_NAME = 'postgres-v1.0.0';
const STATIC_CACHE = 'sila-static-v1.0.0';
const DYNAMIC_CACHE = 'sila-dynamic-v1.0.0';

// Arquivos para cache estático
const STATIC_FILES = [
  '/',
  '/index.html',
  '/manifest.json',
  '/static/js/bundle.js',
  '/static/css/main.css',
  '/icons/icon-192x192.png',
  '/icons/icon-512x512.png'
];

// Endpoints da API para cache
const API_CACHE_PATTERNS = [
  '/api/citizenship/',
  '/api/education/',
  '/api/health/',
  '/api/urbanism/',
  '/api/commercial/'
];

// Instalação do Service Worker
self.addEventListener('install', (event) => {
  console.log('Service Worker: Instalando...');
  
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then((cache) => {
        console.log('Service Worker: Cacheando arquivos estáticos');
        return cache.addAll(STATIC_FILES);
      })
      .then(() => {
        console.log('Service Worker: Instalação concluída');
        return self.skipWaiting();
      })
      .catch((error) => {
        console.error('Service Worker: Erro na instalação', error);
      })
  );
});

// Ativação do Service Worker
self.addEventListener('activate', (event) => {
  console.log('Service Worker: Ativando...');
  
  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => {
            if (cacheName !== STATIC_CACHE && cacheName !== DYNAMIC_CACHE) {
              console.log('Service Worker: Removendo cache antigo', cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      })
      .then(() => {
        console.log('Service Worker: Ativação concluída');
        return self.clients.claim();
      })
  );
});

// Interceptação de requisições
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Estratégia para arquivos estáticos
  if (request.method === 'GET' && isStaticFile(url.pathname)) {
    event.respondWith(cacheFirst(request));
  }
  
  // Estratégia para APIs
  else if (request.method === 'GET' && isApiRequest(url.pathname)) {
    event.respondWith(networkFirst(request));
  }
  
  // Estratégia para outras requisições
  else if (request.method === 'GET') {
    event.respondWith(networkFirst(request));
  }
  
  // Para requisições POST/PUT/DELETE, sempre usar network
  else {
    event.respondWith(networkOnly(request));
  }
});

// Estratégia: Cache First (para arquivos estáticos)
async function cacheFirst(request) {
  try {
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }
    
    const networkResponse = await fetch(request);
    if (networkResponse.ok) {
      const cache = await caches.open(STATIC_CACHE);
      cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    console.error('Cache First Error:', error);
    return new Response('Offline - Arquivo não disponível', {
      status: 503,
      statusText: 'Service Unavailable'
    });
  }
}

// Estratégia: Network First (para APIs)
async function networkFirst(request) {
  try {
    const networkResponse = await fetch(request);
    
    if (networkResponse.ok) {
      const cache = await caches.open(DYNAMIC_CACHE);
      cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    console.log('Network First: Fallback para cache', error);
    
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }
    
    // Retornar resposta offline personalizada para APIs
    if (isApiRequest(request.url)) {
      return new Response(JSON.stringify({
        error: 'offline',
        message: 'Serviço temporariamente indisponível. Tente novamente quando estiver online.',
        timestamp: new Date().toISOString()
      }), {
        status: 503,
        statusText: 'Service Unavailable',
        headers: {
          'Content-Type': 'application/json'
        }
      });
    }
    
    return new Response('Offline - Conteúdo não disponível', {
      status: 503,
      statusText: 'Service Unavailable'
    });
  }
}

// Estratégia: Network Only (para operações críticas)
async function networkOnly(request) {
  try {
    return await fetch(request);
  } catch (error) {
    console.error('Network Only Error:', error);
    throw error;
  }
}

// Verificar se é arquivo estático
function isStaticFile(pathname) {
  return pathname.match(/\.(js|css|png|jpg|jpeg|gif|svg|ico|woff|woff2|ttf|eot)$/);
}

// Verificar se é requisição da API
function isApiRequest(pathname) {
  return API_CACHE_PATTERNS.some(pattern => pathname.includes(pattern));
}

// Sincronização em background
self.addEventListener('sync', (event) => {
  console.log('Service Worker: Sincronização em background', event.tag);
  
  if (event.tag === 'background-sync') {
    event.waitUntil(backgroundSync());
  }
});

// Sincronização de dados offline
async function backgroundSync() {
  try {
    // Buscar dados offline do IndexedDB
    const offlineData = await getOfflineData();
    
    if (offlineData.length > 0) {
      console.log('Background Sync: Sincronizando', offlineData.length, 'operações');
      
      for (const operation of offlineData) {
        try {
          await syncOperation(operation);
          await removeOfflineData(operation.id);
        } catch (error) {
          console.error('Background Sync: Erro ao sincronizar operação', operation.id, error);
        }
      }
    }
  } catch (error) {
    console.error('Background Sync: Erro geral', error);
  }
}

// Notificações push
self.addEventListener('push', (event) => {
  console.log('Service Worker: Notificação push recebida');
  
  const options = {
    body: event.data ? event.data.text() : 'Nova notificação do SILA',
    icon: '/icons/icon-192x192.png',
    badge: '/icons/icon-72x72.png',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    },
    actions: [
      {
        action: 'explore',
        title: 'Ver detalhes',
        icon: '/icons/icon-72x72.png'
      },
      {
        action: 'close',
        title: 'Fechar',
        icon: '/icons/icon-72x72.png'
      }
    ]
  };

  event.waitUntil(
    self.registration.showNotification('SILA System', options)
  );
});

// Clique em notificação
self.addEventListener('notificationclick', (event) => {
  console.log('Service Worker: Notificação clicada', event.action);
  
  event.notification.close();

  if (event.action === 'explore') {
    event.waitUntil(
      clients.openWindow('/dashboard')
    );
  }
});

// Funções auxiliares para IndexedDB (simuladas)
async function getOfflineData() {
  // Em implementação real, buscar do IndexedDB
  return [];
}

async function syncOperation(operation) {
  // Em implementação real, sincronizar com o servidor
  console.log('Sincronizando operação:', operation);
}

async function removeOfflineData(id) {
  // Em implementação real, remover do IndexedDB
  console.log('Removendo operação offline:', id);
}

// Mensagens do cliente
self.addEventListener('message', (event) => {
  console.log('Service Worker: Mensagem recebida', event.data);
  
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  
  if (event.data && event.data.type === 'GET_VERSION') {
    event.ports[0].postMessage({ version: CACHE_NAME });
  }
});

console.log('Service Worker: Carregado'); 
