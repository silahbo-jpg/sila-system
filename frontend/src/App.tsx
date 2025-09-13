import React from 'react'
import { Routes, Route } from 'react-router-dom'
import { Helmet } from 'react-helmet-async'
import { useTranslation } from 'react-i18next'
import { Toaster } from 'react-hot-toast'
import Layout from './components/layout/Layout'
import HomePage from './pages/HomePage'
import ServicesPage from './pages/ServicesPage'
import LoginPage from './pages/LoginPage'
import DashboardPage from './pages/DashboardPage'
import TrainingPage from './pages/TrainingPage'
import NotFoundPage from './pages/NotFoundPage'

/**
 * Main Application Component
 * 
 * Provides routing, layout, and global configuration for the SILA system.
 * Includes internationalization, accessibility features, and error handling.
 */
function App() {
  const { t, i18n } = useTranslation()

  return (
    <div className="App">
      <Helmet>
        <html lang={i18n.language} />
        <title>{t('app.title', 'SILA - Sistema Integrado Local de Administração')}</title>
        <meta 
          name="description" 
          content={t('app.description', 'Digital Government Platform for Angola - Citizen Services Portal')} 
        />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <meta name="theme-color" content="#2563eb" />
        
        {/* Open Graph / Social Media */}
        <meta property="og:type" content="website" />
        <meta property="og:title" content={t('app.title', 'SILA System')} />
        <meta property="og:description" content={t('app.description', 'Digital Government Platform for Angola')} />
        <meta property="og:locale" content={i18n.language === 'pt' ? 'pt_AO' : 'en_US'} />
        
        {/* Accessibility */}
        <meta name="color-scheme" content="light dark" />
      </Helmet>

      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<Layout />}>
          <Route index element={<HomePage />} />
          <Route path="services" element={<ServicesPage />} />
          <Route path="login" element={<LoginPage />} />
          <Route path="training" element={<TrainingPage />} />
          
          {/* Protected Routes */}
          <Route path="dashboard" element={<DashboardPage />} />
          
          {/* Service-specific routes */}
          <Route path="services/:serviceId" element={<ServicesPage />} />
          
          {/* 404 - Keep this last */}
          <Route path="*" element={<NotFoundPage />} />
        </Route>
      </Routes>

      {/* Global Toast Notifications */}
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#363636',
            color: '#fff',
          },
          success: {
            style: {
              background: '#22c55e',
            },
          },
          error: {
            style: {
              background: '#ef4444',
            },
          },
        }}
      />
    </div>
  )
}

export default App