// src/App.tsx

import * as React from 'react';
import { lazy, Suspense, ReactNode } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import LoadingSpinner from './components/common/LoadingSpinner';

// Lazy load pages for better performance
const HomePage = lazy(() => import('./pages/HomePage'));
const LoginPage = lazy(() => import('./pages/LoginPage'));
const RegisterPage = lazy(() => import('./pages/RegisterPage'));
const ModulePage = lazy(() => import('./pages/ModulePage'));
const ServiceDetails = lazy(() => import('./pages/ServiceDetails'));
const Servicos = lazy(() => import('./pages/Servicos'));
const ServiceView = lazy(() => import('./services/ServiceView'));
const CitizenDashboard = lazy(() => import('./pages/citizen/Dashboard'));
const AdminLogin = lazy(() => import('./pages/admin/Login'));
const UnauthorizedPage = lazy(() => import('./pages/UnauthorizedPage'));

// Admin components
const AdminDashboard = lazy(() => import('./components/AdminDashboard'));
const AdminUsers = lazy(() => import('./pages/admin/Users'));
const AdminRequests = lazy(() => import('./pages/admin/Requests'));
const AdminReports = lazy(() => import('./pages/admin/Reports'));

// Module pages
const CidadaniaPage = lazy(() => import('./pages/modules/CidadaniaPage'));
const EducacaoPage = lazy(() => import('./pages/modules/EducacaoPage'));
const UrbanismoPage = lazy(() => import('./pages/modules/UrbanismoPage'));
const SaudePage = lazy(() => import('./pages/modules/SaudePage'));
const ComercioPage = lazy(() => import('./pages/modules/ComercioPage'));

// Import the ProtectedRoute component
import ProtectedRoute from './routes/ProtectedRoute';

// Fallback component for Suspense
const LoadingFallback = () => (
  <div className="flex items-center justify-center min-h-screen">
    <LoadingSpinner size="lg" />
  </div>
);

// Public route wrapper - redirects to dashboard if already authenticated
const PublicRoute = ({ children }: { children: ReactNode }) => {
  const { isAuthenticated, user } = useAuth();
  
  if (isAuthenticated && user) {
    if (user.role === 'admin' || user.role === 'manager' || user.role === 'auditor') {
      return <Navigate to="/admin/dashboard" replace />;
    } else {
      return <Navigate to="/dashboard" replace />;
    }
  }
  
  return <>{children}</>;
};

// Private route wrapper for citizens
const PrivateRoute = ({ children }: { children: ReactNode }) => {
  const { isAuthenticated, isLoading } = useAuth();
  
  if (isLoading) {
    return <LoadingFallback />;
  }
  
  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: window.location.pathname }} replace />;
  }
  
  return <>{children}</>;
};

// Admin route wrapper
const AdminRoute = ({ children }: { children: ReactNode }) => {
  const { isAuthenticated, user, isLoading } = useAuth();
  
  if (isLoading) {
    return <LoadingFallback />;
  }
  
  if (!isAuthenticated || !user || (user.role !== 'admin' && user.role !== 'manager' && user.role !== 'auditor')) {
    return <Navigate to="/unauthorized" replace />;
  }
  
  return <>{children}</>;
};

// Service route wrapper - requires authentication for specific actions
const ServiceRoute = ({ children }: { children: ReactNode }) => {
  const { isAuthenticated, isLoading } = useAuth();
  
  if (isLoading) {
    return <LoadingFallback />;
  }
  
  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: window.location.pathname }} replace />;
  }
  
  return <>{children}</>;
};

function App() {
  return (
    <AuthProvider>
      <Suspense fallback={<LoadingFallback />}>
      <Routes>
        {/* Public Routes */}
        <Route path="/login" element={
          <PublicRoute>
            <LoginPage />
          </PublicRoute>
        } />
        <Route path="/registro" element={
          <PublicRoute>
            <RegisterPage />
          </PublicRoute>
        } />
        <Route path="/unauthorized" element={<UnauthorizedPage />} />

        {/* Admin Routes */}
        <Route path="/admin/login" element={
          <PublicRoute>
            <AdminLogin />
          </PublicRoute>
        } />
        <Route path="/admin/*" element={
          <AdminRoute>
            <Routes>
              <Route index element={<Navigate to="dashboard" replace />} />
              <Route path="*" element={
                <div className="p-6">
                  <h1 className="text-2xl font-bold text-blue-600 mb-6">Dashboard SILA-HBO</h1>
                  <div className="mb-4">
                    <a href="/servicos" className="text-blue-700 underline hover:text-blue-900">Acessar Catálogo de Serviços</a>
                  </div>
                  <AdminDashboard />
                </div>
              } />
            </Routes>
          </AdminRoute>
        }>
          <Route index element={<Navigate to="dashboard" replace />} />
          <Route path="dashboard" element={
            <ProtectedRoute>
              <AdminDashboard />
            </ProtectedRoute>
          } />
          <Route path="usuarios" element={
            <ProtectedRoute>
              <AdminUsers />
            </ProtectedRoute>
          } />
          <Route path="solicitacoes" element={
            <ProtectedRoute>
              <AdminRequests />
            </ProtectedRoute>
          } />
          <Route path="relatorios" element={
            <ProtectedRoute>
              <AdminReports />
            </ProtectedRoute>
          } />
        </Route>

        {/* Module Routes */}
        <Route path="/modulos/:moduleId" element={
          <PrivateRoute>
            <ModulePage />
          </PrivateRoute>
        } />
        <Route path="/cidadania/*" element={
          <ServiceRoute>
            <CidadaniaPage />
          </ServiceRoute>
        } />
        <Route path="/educacao/*" element={
          <ServiceRoute>
            <EducacaoPage />
          </ServiceRoute>
        } />
        <Route path="/urbanismo/*" element={
          <ServiceRoute>
            <UrbanismoPage />
          </ServiceRoute>
        } />
        <Route path="/saude/*" element={
          <ServiceRoute>
            <SaudePage />
          </ServiceRoute>
        } />
        <Route path="/comercio/*" element={
          <ServiceRoute>
            <ComercioPage />
          </ServiceRoute>
        } />

        {/* Service Routes */}
        <Route path="/servicos" element={
          <ServiceRoute>
            <Servicos />
          </ServiceRoute>
        } />
        <Route path="/servico/:serviceId" element={
          <ServiceRoute>
            <ServiceView />
          </ServiceRoute>
        } />
        <Route path="/servicos/:serviceId" element={
          <ServiceRoute>
            <ServiceDetails />
          </ServiceRoute>
        } />

        {/* Citizen Dashboard */}
        <Route path="/dashboard" element={
          <PrivateRoute>
            <CitizenDashboard />
          </PrivateRoute>
        } />

        {/* Home/Default Route */}
        <Route path="/" element={
          <PublicRoute>
            <HomePage />
          </PublicRoute>
        } />

        {/* 404 Not Found */}
        <Route path="*" element={
          <div className="flex items-center justify-center min-h-screen">
            <div className="text-center">
              <h1 className="text-4xl font-bold text-gray-800">404</h1>
              <p className="text-gray-600">Página não encontrada</p>
            </div>
          </div>
        } />
      </Routes>
    </Suspense>
    </AuthProvider>
  );
}

export default App;
