# Harmonização Backend-Frontend - SILA System

## 🎯 Visão Geral

Este documento descreve a harmonização completa entre o backend Django/FastAPI e o frontend React, com foco especial na plataforma móvel e experiência do usuário.

## 🏗️ Arquitetura da Integração

### Backend (Django/FastAPI)
```
backend/
├── app/
│   ├── modules/
│   │   ├── citizenship/     # Módulo de cidadania
│   │   ├── education/       # Módulo de educação
│   │   ├── health/          # Módulo de saúde
│   │   ├── urbanism/        # Módulo de urbanismo
│   │   └── commercial/      # Módulo comercial
│   ├── auth/               # Autenticação JWT
│   ├── core/               # Configurações centrais
│   └── main.py             # Aplicação FastAPI
```

### Frontend (React/Vite)
```
frontend/webapp/
├── src/
│   ├── pages/modules/      # Páginas dos módulos
│   ├── services/           # Serviços de API
│   ├── hooks/              # Hooks personalizados
│   ├── components/         # Componentes reutilizáveis
│   └── context/            # Contextos React
```

## 🔗 Integração de APIs

### 1. Serviço de API Centralizado

```typescript
// services/api.ts
class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: 'http://localhost:8000',
      timeout: 30000,
    });
    this.setupInterceptors();
  }

  // Métodos específicos por módulo
  async createCitizen(citizenData: any) {
    return this.post('/api/citizenship/citizens/', citizenData);
  }

  async createAtestado(atestadoData: any) {
    return this.post('/api/citizenship/atestado/', atestadoData);
  }
}
```

### 2. Endpoints Mapeados

| Módulo | Endpoint Backend | Método Frontend | Descrição |
|--------|------------------|-----------------|-----------|
| Cidadania | `/api/citizenship/citizens/` | `api.createCitizen()` | CRUD de cidadãos |
| Cidadania | `/api/citizenship/atestado/` | `api.createAtestado()` | Atestados de residência |
| Educação | `/api/education/schools/` | `api.getSchools()` | Escolas municipais |
| Saúde | `/api/health/appointments/` | `api.createAppointment()` | Agendamentos |
| Urbanismo | `/api/urbanism/licenses/` | `api.createLicense()` | Licenças urbanas |

## 📱 Otimizações Mobile

### 1. Sincronização Offline

```typescript
// hooks/useMobileSync.ts
export const useMobileSync = () => {
  const [syncStatus, setSyncStatus] = useState({
    isOnline: navigator.onLine,
    isSyncing: false,
    pendingChanges: 0,
  });

  // API wrapper para operações offline
  const offlineApi = {
    post: async (endpoint: string, data: any) => {
      if (syncStatus.isOnline) {
        return await api.post(endpoint, data);
      } else {
        // Salvar offline para sincronização posterior
        addOfflineOperation({ type: 'create', endpoint, data });
      }
    }
  };
};
```

### 2. Cache Inteligente

```typescript
// Cache de dados para uso offline
const cacheData = useCallback((endpoint: string, data: any) => {
  localStorage.setItem(`cache_${endpoint}`, JSON.stringify(data));
}, []);

// Busca de dados com fallback offline
const getData = async (endpoint: string) => {
  if (syncStatus.isOnline) {
    const data = await api.get(endpoint);
    cacheData(endpoint, data); // Cache para uso offline
    return data;
  } else {
    const cached = localStorage.getItem(`cache_${endpoint}`);
    return cached ? JSON.parse(cached) : null;
  }
};
```

### 3. PWA (Progressive Web App)

```json
// public/manifest.json
{
  "name": "SILA - Sistema Integrado",
  "short_name": "SILA",
  "display": "standalone",
  "orientation": "portrait-primary",
  "shortcuts": [
    {
      "name": "Cidadania",
      "url": "/cidadania",
      "icons": [{ "src": "/icons/citizenship-96x96.png", "sizes": "96x96" }]
    }
  ]
}
```

## 🔄 Fluxo de Dados

### 1. Autenticação

```typescript
// Context de autenticação
const AuthContext = createContext({
  login: async (credentials: LoginCredentials) => {
    const response = await api.login(credentials);
    localStorage.setItem('authToken', response.access_token);
    localStorage.setItem('refreshToken', response.refresh_token);
  },
  
  logout: () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('refreshToken');
  }
});
```

### 2. Interceptors de Token

```typescript
// Auto-refresh de tokens
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      const refreshToken = localStorage.getItem('refreshToken');
      if (refreshToken) {
        const newToken = await api.refreshToken(refreshToken);
        localStorage.setItem('authToken', newToken);
        // Reenviar requisição original
        return api.request(error.config);
      }
    }
    return Promise.reject(error);
  }
);
```

## 🎨 Componentes Harmonizados

### 1. Formulários Responsivos

```typescript
// Componentes de formulário com validação
const AtestadoForm = () => {
  const { register, handleSubmit, formState: { errors } } = useForm();
  
  const onSubmit = async (data) => {
    try {
      await api.createAtestado(data);
      // Feedback de sucesso
    } catch (error) {
      // Tratamento de erro
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Input
        label="Nome Completo"
        {...register('nomeCompleto', { required: 'Nome é obrigatório' })}
        error={errors.nomeCompleto?.message}
      />
    </form>
  );
};
```

### 2. Navegação Mobile-First

```typescript
// Navegação adaptativa
const MobileNavigation = () => {
  const [isOpen, setIsOpen] = useState(false);
  
  return (
    <div className="lg:hidden">
      {/* Menu hambúrguer */}
      <button onClick={() => setIsOpen(!isOpen)}>
        <svg>...</svg>
      </button>
      
      {/* Menu lateral */}
      <div className={`${isOpen ? 'block' : 'hidden'} fixed inset-0 z-50`}>
        {/* Conteúdo do menu */}
      </div>
    </div>
  );
};
```

## 🔧 Configurações de Desenvolvimento

### 1. Variáveis de Ambiente

```bash
# .env
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=SILA System
VITE_APP_VERSION=1.0.0
```

### 2. Scripts de Build

```json
// package.json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "build:mobile": "vite build --mode mobile"
  }
}
```

### 3. Configuração Vite

```typescript
// vite.config.ts
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          modules: ['react-router-dom', 'axios'],
        }
      }
    }
  }
});
```

## 📊 Monitoramento e Performance

### 1. Métricas de Performance

```typescript
// Hook para métricas
const usePerformanceMetrics = () => {
  useEffect(() => {
    // Core Web Vitals
    const observer = new PerformanceObserver((list) => {
      list.getEntries().forEach((entry) => {
        console.log(`${entry.name}: ${entry.value}`);
      });
    });
    
    observer.observe({ entryTypes: ['navigation', 'resource'] });
  }, []);
};
```

### 2. Error Boundary

```typescript
// Tratamento de erros global
class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    // Enviar erro para serviço de monitoramento
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return <ErrorFallback />;
    }
    return this.props.children;
  }
}
```

## 🚀 Deploy e Produção

### 1. Build Otimizado

```bash
# Build para produção
npm run build

# Build específico para mobile
npm run build:mobile
```

### 2. Configuração Nginx

```nginx
# nginx.conf
server {
    listen 80;
    server_name sila.local;
    
    # Frontend
    location / {
        root /var/www/sila-frontend;
        try_files $uri $uri/ /index.html;
    }
    
    # API Backend
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 3. Docker Compose

```yaml
# docker-compose.yml
version: '3.8'
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
      
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/sila_dev
      
  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=sila
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
```

## 📋 Checklist de Harmonização

### ✅ Implementado

- [x] Serviço de API centralizado
- [x] Interceptors de autenticação
- [x] Sincronização offline
- [x] Cache inteligente
- [x] PWA configurado
- [x] Componentes responsivos
- [x] Navegação mobile-first
- [x] Error boundaries
- [x] Métricas de performance

### 🔄 Em Progresso

- [ ] Testes de integração
- [ ] Documentação de APIs
- [ ] Monitoramento em produção
- [ ] Otimizações de bundle
- [ ] Service Worker para cache

### 📋 Próximos Passos

- [ ] Implementar notificações push
- [ ] Adicionar autenticação biométrica
- [ ] Otimizar carregamento lazy
- [ ] Implementar analytics
- [ ] Configurar CI/CD

## 🎯 Resultados Esperados

### Performance
- **First Contentful Paint**: < 1.5s
- **Largest Contentful Paint**: < 2.5s
- **Cumulative Layout Shift**: < 0.1
- **Time to Interactive**: < 3.5s

### Experiência Mobile
- **Offline First**: Funcionamento sem internet
- **Touch Optimized**: Interface otimizada para toque
- **Fast Navigation**: Navegação fluida entre telas
- **Battery Efficient**: Baixo consumo de bateria

### Integração Backend
- **Real-time Sync**: Sincronização em tempo real
- **Error Handling**: Tratamento robusto de erros
- **Security**: Autenticação e autorização seguras
- **Scalability**: Arquitetura escalável

---

**Status**: ✅ Harmonização básica implementada
**Próximo**: 🔄 Otimizações avançadas e testes 
