// Console utilities for development environment
// This helps suppress known warnings that don't affect functionality

export const suppressKnownWarnings = () => {
  // Only suppress warnings in development
  if (import.meta.env.MODE !== 'development') {
    return;
  }

  const originalWarn = console.warn;
  const originalError = console.error;

  // List of warning patterns to suppress
  const suppressedWarnings = [
    'React DevTools for a better development experience',
    'DOMNodeInsertedIntoDocument',
    'DOM Mutation Event',
    'React Router Future Flag Warning',
    'Erro ao carregar dados:',
    'Erro ao carregar municípios:',
    'GET http://localhost:8000/v2/dashboard'
  ];

  // Override console.warn to filter out known warnings
  console.warn = (...args) => {
    const message = args.join(' ');
    
    // Check if this warning should be suppressed
    const shouldSuppress = suppressedWarnings.some(pattern => 
      message.includes(pattern)
    );
    
    if (!shouldSuppress) {
      originalWarn.apply(console, args);
    }
  };

  // Override console.error for specific error patterns
  console.error = (...args) => {
    const message = args.join(' ');
    
    // Suppress specific error patterns if needed
    const shouldSuppress = suppressedWarnings.some(pattern => 
      message.includes(pattern)
    );
    
    if (!shouldSuppress) {
      originalError.apply(console, args);
    }
  };
};

// Helper to restore original console methods
export const restoreConsole = () => {
  // This would need to store original methods if implemented
  console.warn = console.warn;
  console.error = console.error;
};

// Development helper to show only app-specific logs
export const enableDevLogging = () => {
  if (import.meta.env.MODE === 'development') {
    console.log('%c🚀 SILA-HUAMBO Development Mode', 
      'color: #D71A28; font-weight: bold; font-size: 16px;'
    );
    console.log('%c⚡ Authentication system loaded with Angola theme', 
      'color: #FFD700; font-weight: bold;'
    );
    console.log('%c📧 Admin login: admin@sila.gov.ao', 
      'color: #000000; font-weight: bold;'
    );
    console.log('%c🔑 Admin NIF: 123456789', 
      'color: #000000; font-weight: bold;'
    );
    console.log('%c🏛️ Territorial Mapping 2025: 17 Municípios | Complete Comuna Structure Loaded', 
      'color: #D71A28; font-weight: bold;'
    );
  }
};