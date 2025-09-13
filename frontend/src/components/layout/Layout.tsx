import React from 'react'
import { Outlet } from 'react-router-dom'
import Header from './Header'
import Footer from './Footer'

/**
 * Main Layout Component
 * 
 * Provides the overall structure for all pages in the SILA application.
 * Includes header, main content area, and footer.
 */
function Layout() {
  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      {/* Skip to content link for accessibility */}
      <a 
        href="#main-content" 
        className="skip-link sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 bg-primary-600 text-white px-4 py-2 rounded-md z-50"
      >
        Saltar para o conteúdo principal
      </a>
      
      {/* Header */}
      <Header />
      
      {/* Main Content */}
      <main 
        id="main-content" 
        className="flex-1 focus:outline-none" 
        tabIndex={-1}
      >
        <Outlet />
      </main>
      
      {/* Footer */}
      <Footer />
    </div>
  )
}

export default Layout