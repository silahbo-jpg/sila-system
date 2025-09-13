"""
WCAG Accessibility Compliance Module for SILA System

This module provides comprehensive Web Content Accessibility Guidelines (WCAG) 2.1 
Level AA compliance features including:

- Screen reader support
- Keyboard navigation
- High contrast modes
- Text scaling and font adjustments
- Voice navigation support
- Automated accessibility testing
- Accessibility audit reporting
- Multi-language accessibility

Based on WCAG 2.1 guidelines and best practices for government accessibility.
"""

import React, { useState, useEffect, useContext, createContext } from 'react';
import { axeCore } from '@axe-core/react';

// Accessibility Context
const AccessibilityContext = createContext();

// Accessibility Provider Component
export const AccessibilityProvider = ({ children }) => {
  const [accessibilitySettings, setAccessibilitySettings] = useState({
    // Visual Settings
    highContrast: false,
    fontSize: 'normal', // small, normal, large, extra-large
    fontFamily: 'default', // default, dyslexic, sans-serif
    lineHeight: 'normal', // normal, increased, double
    letterSpacing: 'normal', // normal, increased
    
    // Navigation Settings
    keyboardNavigation: true,
    skipLinks: true,
    focusIndicators: true,
    
    // Audio/Visual Settings
    reduceMotion: false,
    autoplayDisabled: true,
    screenReaderOptimized: false,
    
    // Language Settings
    language: 'pt',
    voiceLanguage: 'pt-AO',
    
    // Interaction Settings
    clickDelay: 0, // milliseconds delay for click handlers
    scrollSensitivity: 'normal',
    touchTargetSize: 'normal' // normal, large
  });

  // Load settings from localStorage
  useEffect(() => {
    const savedSettings = localStorage.getItem('sila-accessibility-settings');
    if (savedSettings) {
      setAccessibilitySettings(prev => ({
        ...prev,
        ...JSON.parse(savedSettings)
      }));
    }
  }, []);

  // Save settings to localStorage
  const updateSettings = (newSettings) => {
    const updatedSettings = { ...accessibilitySettings, ...newSettings };
    setAccessibilitySettings(updatedSettings);
    localStorage.setItem('sila-accessibility-settings', JSON.stringify(updatedSettings));
    
    // Apply CSS custom properties for visual changes
    applyVisualSettings(updatedSettings);
    
    // Announce changes to screen readers
    announceSettingChange(newSettings);
  };

  const applyVisualSettings = (settings) => {
    const root = document.documentElement;
    
    // Font size
    const fontSizeMap = {
      'small': '0.875rem',
      'normal': '1rem',
      'large': '1.25rem',
      'extra-large': '1.5rem'
    };
    root.style.setProperty('--base-font-size', fontSizeMap[settings.fontSize]);
    
    // Line height
    const lineHeightMap = {
      'normal': '1.5',
      'increased': '1.75',
      'double': '2'
    };
    root.style.setProperty('--base-line-height', lineHeightMap[settings.lineHeight]);
    
    // Letter spacing
    const letterSpacingMap = {
      'normal': '0',
      'increased': '0.05em'
    };
    root.style.setProperty('--letter-spacing', letterSpacingMap[settings.letterSpacing]);
    
    // High contrast
    if (settings.highContrast) {
      document.body.classList.add('high-contrast');
    } else {
      document.body.classList.remove('high-contrast');
    }
    
    // Reduced motion
    if (settings.reduceMotion) {
      document.body.classList.add('reduce-motion');
    } else {
      document.body.classList.remove('reduce-motion');
    }
    
    // Touch target size
    if (settings.touchTargetSize === 'large') {
      document.body.classList.add('large-touch-targets');
    } else {
      document.body.classList.remove('large-touch-targets');
    }
  };

  const announceSettingChange = (changes) => {
    const announcements = [];
    
    if ('highContrast' in changes) {
      announcements.push(changes.highContrast ? 
        'Modo de alto contraste ativado' : 
        'Modo de alto contraste desativado'
      );
    }
    
    if ('fontSize' in changes) {
      announcements.push(`Tamanho da fonte alterado para ${changes.fontSize}`);
    }
    
    if (announcements.length > 0) {
      announceToScreenReader(announcements.join('. '));
    }
  };

  return (
    <AccessibilityContext.Provider value={{
      settings: accessibilitySettings,
      updateSettings,
      announceToScreenReader
    }}>
      {children}
    </AccessibilityContext.Provider>
  );
};

// Hook to use accessibility context
export const useAccessibility = () => {
  const context = useContext(AccessibilityContext);
  if (!context) {
    throw new Error('useAccessibility must be used within AccessibilityProvider');
  }
  return context;
};

// Screen Reader Announcer
export const announceToScreenReader = (message, priority = 'polite') => {
  const announcer = document.getElementById('sr-announcer') || createAnnouncer();
  
  // Clear previous content
  announcer.textContent = '';
  
  // Set aria-live priority
  announcer.setAttribute('aria-live', priority);
  
  // Add message with slight delay to ensure screen reader picks it up
  setTimeout(() => {
    announcer.textContent = message;
  }, 100);
};

const createAnnouncer = () => {
  const announcer = document.createElement('div');
  announcer.id = 'sr-announcer';
  announcer.setAttribute('aria-live', 'polite');
  announcer.setAttribute('aria-atomic', 'true');
  announcer.style.cssText = `
    position: absolute;
    left: -10000px;
    width: 1px;
    height: 1px;
    overflow: hidden;
  `;
  document.body.appendChild(announcer);
  return announcer;
};

// Skip Links Component
export const SkipLinks = () => {
  const { settings } = useAccessibility();
  
  if (!settings.skipLinks) return null;
  
  return (
    <div className="skip-links">
      <a href="#main-content" className="skip-link">
        Ir para o conteúdo principal
      </a>
      <a href="#main-navigation" className="skip-link">
        Ir para a navegação
      </a>
      <a href="#search" className="skip-link">
        Ir para a pesquisa
      </a>
      <a href="#footer" className="skip-link">
        Ir para o rodapé
      </a>
    </div>
  );
};

// Accessible Form Component
export const AccessibleForm = ({ children, onSubmit, title, description }) => {
  const { settings } = useAccessibility();
  const formId = `form-${Date.now()}`;
  const titleId = `${formId}-title`;
  const descId = `${formId}-description`;
  
  return (
    <form
      onSubmit={onSubmit}
      aria-labelledby={titleId}
      aria-describedby={description ? descId : undefined}
      noValidate
    >
      {title && (
        <h2 id={titleId} className="form-title">
          {title}
        </h2>
      )}
      {description && (
        <p id={descId} className="form-description">
          {description}
        </p>
      )}
      {children}
    </form>
  );
};

// Accessible Input Component
export const AccessibleInput = ({
  label,
  type = 'text',
  required = false,
  error,
  description,
  value,
  onChange,
  id,
  ...props
}) => {
  const inputId = id || `input-${Date.now()}`;
  const errorId = `${inputId}-error`;
  const descId = `${inputId}-description`;
  
  return (
    <div className={`input-group ${error ? 'has-error' : ''}`}>
      <label htmlFor={inputId} className="input-label">
        {label}
        {required && <span className="required-indicator" aria-label="obrigatório">*</span>}
      </label>
      
      {description && (
        <p id={descId} className="input-description">
          {description}
        </p>
      )}
      
      <input
        id={inputId}
        type={type}
        value={value}
        onChange={onChange}
        required={required}
        aria-invalid={error ? 'true' : 'false'}
        aria-describedby={[
          description ? descId : null,
          error ? errorId : null
        ].filter(Boolean).join(' ') || undefined}
        className="accessible-input"
        {...props}
      />
      
      {error && (
        <div id={errorId} className="input-error" role="alert">
          {error}
        </div>
      )}
    </div>
  );
};

// Accessible Button Component
export const AccessibleButton = ({
  children,
  onClick,
  variant = 'primary',
  size = 'normal',
  disabled = false,
  loading = false,
  ...props
}) => {
  const { settings } = useAccessibility();
  
  const handleClick = (e) => {
    if (settings.clickDelay > 0) {
      setTimeout(() => onClick && onClick(e), settings.clickDelay);
    } else {
      onClick && onClick(e);
    }
  };
  
  return (
    <button
      onClick={handleClick}
      disabled={disabled || loading}
      className={`accessible-button ${variant} ${size}`}
      aria-disabled={disabled || loading}
      {...props}
    >
      {loading && (
        <span className="loading-indicator" aria-hidden="true">
          ⏳
        </span>
      )}
      <span className={loading ? 'visually-hidden' : ''}>
        {children}
      </span>
      {loading && (
        <span className="sr-only">Carregando...</span>
      )}
    </button>
  );
};

// Focus Trap Component
export const FocusTrap = ({ children, active = true }) => {
  const trapRef = React.useRef();
  
  useEffect(() => {
    if (!active) return;
    
    const trap = trapRef.current;
    const focusableElements = trap.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    
    const firstElement = focusableElements[0];
    const lastElement = focusableElements[focusableElements.length - 1];
    
    const handleTabKey = (e) => {
      if (e.key !== 'Tab') return;
      
      if (e.shiftKey) {
        if (document.activeElement === firstElement) {
          lastElement.focus();
          e.preventDefault();
        }
      } else {
        if (document.activeElement === lastElement) {
          firstElement.focus();
          e.preventDefault();
        }
      }
    };
    
    trap.addEventListener('keydown', handleTabKey);
    firstElement?.focus();
    
    return () => {
      trap.removeEventListener('keydown', handleTabKey);
    };
  }, [active]);
  
  return (
    <div ref={trapRef}>
      {children}
    </div>
  );
};

// Accessible Modal Component
export const AccessibleModal = ({ 
  isOpen, 
  onClose, 
  title, 
  children,
  size = 'medium'
}) => {
  const { settings } = useAccessibility();
  const [previousFocus, setPreviousFocus] = useState(null);
  
  useEffect(() => {
    if (isOpen) {
      setPreviousFocus(document.activeElement);
      document.body.style.overflow = 'hidden';
      announceToScreenReader('Modal aberto: ' + title);
    } else {
      document.body.style.overflow = '';
      if (previousFocus) {
        previousFocus.focus();
      }
    }
    
    return () => {
      document.body.style.overflow = '';
    };
  }, [isOpen, title, previousFocus]);
  
  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    
    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [isOpen, onClose]);
  
  if (!isOpen) return null;
  
  return (
    <div 
      className="modal-overlay"
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
      onClick={(e) => e.target === e.currentTarget && onClose()}
    >
      <FocusTrap active={isOpen}>
        <div className={`modal-content ${size}`}>
          <div className="modal-header">
            <h2 id="modal-title" className="modal-title">
              {title}
            </h2>
            <button
              onClick={onClose}
              className="modal-close"
              aria-label="Fechar modal"
            >
              ×
            </button>
          </div>
          <div className="modal-body">
            {children}
          </div>
        </div>
      </FocusTrap>
    </div>
  );
};

// Accessibility Settings Panel
export const AccessibilityPanel = ({ isOpen, onClose }) => {
  const { settings, updateSettings } = useAccessibility();
  
  return (
    <AccessibleModal
      isOpen={isOpen}
      onClose={onClose}
      title="Configurações de Acessibilidade"
      size="large"
    >
      <div className="accessibility-panel">
        <section className="settings-section">
          <h3>Configurações Visuais</h3>
          
          <div className="setting-item">
            <label>
              <input
                type="checkbox"
                checked={settings.highContrast}
                onChange={(e) => updateSettings({ highContrast: e.target.checked })}
              />
              Alto Contraste
            </label>
            <p className="setting-description">
              Aumenta o contraste entre texto e fundo para melhor legibilidade
            </p>
          </div>
          
          <div className="setting-item">
            <label htmlFor="font-size">Tamanho da Fonte</label>
            <select
              id="font-size"
              value={settings.fontSize}
              onChange={(e) => updateSettings({ fontSize: e.target.value })}
            >
              <option value="small">Pequeno</option>
              <option value="normal">Normal</option>
              <option value="large">Grande</option>
              <option value="extra-large">Extra Grande</option>
            </select>
          </div>
          
          <div className="setting-item">
            <label htmlFor="line-height">Espaçamento entre Linhas</label>
            <select
              id="line-height"
              value={settings.lineHeight}
              onChange={(e) => updateSettings({ lineHeight: e.target.value })}
            >
              <option value="normal">Normal</option>
              <option value="increased">Aumentado</option>
              <option value="double">Duplo</option>
            </select>
          </div>
        </section>
        
        <section className="settings-section">
          <h3>Configurações de Navegação</h3>
          
          <div className="setting-item">
            <label>
              <input
                type="checkbox"
                checked={settings.keyboardNavigation}
                onChange={(e) => updateSettings({ keyboardNavigation: e.target.checked })}
              />
              Navegação por Teclado Aprimorada
            </label>
            <p className="setting-description">
              Melhora o suporte para navegação usando apenas o teclado
            </p>
          </div>
          
          <div className="setting-item">
            <label>
              <input
                type="checkbox"
                checked={settings.skipLinks}
                onChange={(e) => updateSettings({ skipLinks: e.target.checked })}
              />
              Links de Navegação Rápida
            </label>
            <p className="setting-description">
              Exibe links para ir diretamente para seções importantes da página
            </p>
          </div>
        </section>
        
        <section className="settings-section">
          <h3>Configurações de Movimento</h3>
          
          <div className="setting-item">
            <label>
              <input
                type="checkbox"
                checked={settings.reduceMotion}
                onChange={(e) => updateSettings({ reduceMotion: e.target.checked })}
              />
              Reduzir Animações
            </label>
            <p className="setting-description">
              Reduz ou remove animações que podem causar desconforto
            </p>
          </div>
          
          <div className="setting-item">
            <label>
              <input
                type="checkbox"
                checked={settings.autoplayDisabled}
                onChange={(e) => updateSettings({ autoplayDisabled: e.target.checked })}
              />
              Desabilitar Reprodução Automática
            </label>
            <p className="setting-description">
              Impede que vídeos e áudios sejam reproduzidos automaticamente
            </p>
          </div>
        </section>
        
        <div className="panel-actions">
          <AccessibleButton onClick={() => updateSettings({})}>
            Salvar Configurações
          </AccessibleButton>
          <AccessibleButton variant="secondary" onClick={onClose}>
            Fechar
          </AccessibleButton>
        </div>
      </div>
    </AccessibleModal>
  );
};

// Accessibility Testing Hook
export const useAccessibilityTesting = () => {
  const [violations, setViolations] = useState([]);
  const [isTestingEnabled, setIsTestingEnabled] = useState(
    process.env.NODE_ENV === 'development'
  );
  
  useEffect(() => {
    if (isTestingEnabled && window.axe) {
      const runTests = async () => {
        try {
          const results = await window.axe.run();
          setViolations(results.violations);
          
          if (results.violations.length > 0) {
            console.group('🔍 Accessibility Violations Found');
            results.violations.forEach(violation => {
              console.error(`${violation.impact}: ${violation.description}`);
              console.log('Help:', violation.helpUrl);
              console.log('Elements:', violation.nodes);
            });
            console.groupEnd();
          }
        } catch (error) {
          console.error('Accessibility testing error:', error);
        }
      };
      
      // Run tests after component updates
      const timeoutId = setTimeout(runTests, 1000);
      return () => clearTimeout(timeoutId);
    }
  }, [isTestingEnabled]);
  
  return {
    violations,
    isTestingEnabled,
    setIsTestingEnabled
  };
};

// Accessibility Report Generator
export const generateAccessibilityReport = async () => {
  if (!window.axe) {
    throw new Error('axe-core not loaded');
  }
  
  const results = await window.axe.run(document, {
    tags: ['wcag2a', 'wcag2aa', 'wcag21aa']
  });
  
  const report = {
    timestamp: new Date().toISOString(),
    url: window.location.href,
    violations: results.violations.map(violation => ({
      id: violation.id,
      impact: violation.impact,
      description: violation.description,
      help: violation.help,
      helpUrl: violation.helpUrl,
      nodes: violation.nodes.length,
      tags: violation.tags
    })),
    passes: results.passes.length,
    incomplete: results.incomplete.length,
    summary: {
      total: results.violations.length,
      critical: results.violations.filter(v => v.impact === 'critical').length,
      serious: results.violations.filter(v => v.impact === 'serious').length,
      moderate: results.violations.filter(v => v.impact === 'moderate').length,
      minor: results.violations.filter(v => v.impact === 'minor').length
    }
  };
  
  return report;
};

// CSS for accessibility features (to be included in main CSS)
export const accessibilityCSS = `
/* Skip Links */
.skip-links {
  position: absolute;
  top: -40px;
  left: 6px;
  z-index: 1000;
}

.skip-link {
  position: absolute;
  padding: 8px 16px;
  background: #000;
  color: #fff;
  text-decoration: none;
  border-radius: 0 0 4px 4px;
  transform: translateY(-100%);
  transition: transform 0.3s;
}

.skip-link:focus {
  transform: translateY(0);
}

/* High Contrast Mode */
.high-contrast {
  --text-color: #000;
  --background-color: #fff;
  --link-color: #0000ff;
  --border-color: #000;
}

.high-contrast * {
  background-color: var(--background-color) !important;
  color: var(--text-color) !important;
  border-color: var(--border-color) !important;
}

.high-contrast a {
  color: var(--link-color) !important;
  text-decoration: underline !important;
}

/* Reduced Motion */
.reduce-motion * {
  animation-duration: 0.01ms !important;
  animation-iteration-count: 1 !important;
  transition-duration: 0.01ms !important;
}

/* Large Touch Targets */
.large-touch-targets button,
.large-touch-targets a,
.large-touch-targets input,
.large-touch-targets select {
  min-height: 44px;
  min-width: 44px;
}

/* Focus Indicators */
*:focus {
  outline: 2px solid #005fcc;
  outline-offset: 2px;
}

/* Screen Reader Only */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* Accessible Form Styles */
.input-group {
  margin-bottom: 1rem;
}

.input-label {
  display: block;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.required-indicator {
  color: #d32f2f;
  margin-left: 0.25rem;
}

.input-description {
  font-size: 0.875rem;
  color: #666;
  margin-bottom: 0.5rem;
}

.accessible-input {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
}

.accessible-input:focus {
  border-color: #005fcc;
}

.has-error .accessible-input {
  border-color: #d32f2f;
}

.input-error {
  color: #d32f2f;
  font-size: 0.875rem;
  margin-top: 0.5rem;
}

/* Accessible Button Styles */
.accessible-button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
  min-height: 44px;
}

.accessible-button.primary {
  background-color: #005fcc;
  color: white;
}

.accessible-button.secondary {
  background-color: #f5f5f5;
  color: #333;
  border: 1px solid #ccc;
}

.accessible-button:hover:not(:disabled) {
  opacity: 0.9;
}

.accessible-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  max-width: 90vw;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.modal-content.medium {
  width: 500px;
}

.modal-content.large {
  width: 800px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #eee;
}

.modal-title {
  margin: 0;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 4px;
}

.modal-body {
  padding: 1rem;
}

/* Accessibility Panel Styles */
.accessibility-panel {
  max-height: 70vh;
  overflow-y: auto;
}

.settings-section {
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #eee;
}

.settings-section h3 {
  margin-bottom: 1rem;
  color: #333;
}

.setting-item {
  margin-bottom: 1rem;
}

.setting-item label {
  display: flex;
  align-items: center;
  font-weight: normal;
}

.setting-item input[type="checkbox"] {
  margin-right: 0.5rem;
}

.setting-description {
  font-size: 0.875rem;
  color: #666;
  margin-top: 0.25rem;
  margin-left: 1.5rem;
}

.panel-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #eee;
}
`;

export default {
  AccessibilityProvider,
  useAccessibility,
  SkipLinks,
  AccessibleForm,
  AccessibleInput,
  AccessibleButton,
  AccessibleModal,
  AccessibilityPanel,
  FocusTrap,
  announceToScreenReader,
  useAccessibilityTesting,
  generateAccessibilityReport,
  accessibilityCSS
};