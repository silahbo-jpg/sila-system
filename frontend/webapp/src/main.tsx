import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { I18nextProvider } from 'react-i18next';
import App from './App';
import './index.css';
import i18n from './i18n';
import { suppressKnownWarnings, enableDevLogging } from './utils/console';

// Initialize development utilities
if (import.meta.env.MODE === 'development') {
  suppressKnownWarnings();
  enableDevLogging();
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter
      future={{
        v7_startTransition: true,
        v7_relativeSplatPath: true,
      } as any}
    >
      <I18nextProvider i18n={i18n}>
        <App />
      </I18nextProvider>
    </BrowserRouter>
  </React.StrictMode>
);

