import React from 'react'
import { useTranslation } from 'react-i18next'

interface ErrorFallbackProps {
  error: Error
  resetErrorBoundary: () => void
}

function ErrorFallback({ error, resetErrorBoundary }: ErrorFallbackProps) {
  const { t } = useTranslation()

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full bg-white shadow-lg rounded-lg p-6">
        <div className="flex">
          <div className="flex-shrink-0">
            <div className="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center">
              <span className="text-red-600 font-bold">!</span>
            </div>
          </div>
          <div className="ml-3">
            <h3 className="text-sm font-medium text-gray-900">
              {t('app.error')}
            </h3>
            <div className="mt-2 text-sm text-gray-500">
              <p>Ocorreu um erro inesperado. Por favor, tente novamente.</p>
              {process.env.NODE_ENV === 'development' && (
                <details className="mt-2">
                  <summary className="cursor-pointer text-xs text-gray-400">
                    Detalhes técnicos
                  </summary>
                  <pre className="mt-2 text-xs text-red-600 whitespace-pre-wrap">
                    {error.message}
                  </pre>
                </details>
              )}
            </div>
            <div className="mt-4">
              <button
                type="button"
                onClick={resetErrorBoundary}
                className="btn-primary text-sm"
              >
                Tentar novamente
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ErrorFallback