import React from 'react'
import { useTranslation } from 'react-i18next'

function Footer() {
  const { t } = useTranslation()
  const currentYear = new Date().getFullYear()

  return (
    <footer className="bg-gray-50 border-t border-gray-200">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* About SILA */}
          <div>
            <h3 className="text-sm font-semibold text-gray-900 tracking-wider uppercase">
              SILA
            </h3>
            <p className="mt-4 text-sm text-gray-600">
              {t('app.description')}
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-sm font-semibold text-gray-900 tracking-wider uppercase">
              {t('nav.services')}
            </h3>
            <ul className="mt-4 space-y-2">
              <li>
                <a href="/services" className="text-sm text-gray-600 hover:text-gray-900">
                  {t('services.health')}
                </a>
              </li>
              <li>
                <a href="/services" className="text-sm text-gray-600 hover:text-gray-900">
                  {t('services.education')}
                </a>
              </li>
              <li>
                <a href="/services" className="text-sm text-gray-600 hover:text-gray-900">
                  {t('services.citizenship')}
                </a>
              </li>
            </ul>
          </div>

          {/* Support */}
          <div>
            <h3 className="text-sm font-semibold text-gray-900 tracking-wider uppercase">
              {t('nav.help')}
            </h3>
            <ul className="mt-4 space-y-2">
              <li>
                <a href="/training" className="text-sm text-gray-600 hover:text-gray-900">
                  {t('nav.training')}
                </a>
              </li>
              <li>
                <a href="#" className="text-sm text-gray-600 hover:text-gray-900">
                  Contacto
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-gray-200">
          <p className="text-center text-sm text-gray-600">
            © {currentYear} SILA - Sistema Integrado Local de Administração. República de Angola.
          </p>
        </div>
      </div>
    </footer>
  )
}

export default Footerimport React from 'react'
import { useTranslation } from 'react-i18next'

function Footer() {
  const { t } = useTranslation()
  const currentYear = new Date().getFullYear()

  return (
    <footer className="bg-gray-50 border-t border-gray-200">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* About SILA */}
          <div>
            <h3 className="text-sm font-semibold text-gray-900 tracking-wider uppercase">
              SILA
            </h3>
            <p className="mt-4 text-sm text-gray-600">
              {t('app.description')}
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-sm font-semibold text-gray-900 tracking-wider uppercase">
              {t('nav.services')}
            </h3>
            <ul className="mt-4 space-y-2">
              <li>
                <a href="/services" className="text-sm text-gray-600 hover:text-gray-900">
                  {t('services.health')}
                </a>
              </li>
              <li>
                <a href="/services" className="text-sm text-gray-600 hover:text-gray-900">
                  {t('services.education')}
                </a>
              </li>
              <li>
                <a href="/services" className="text-sm text-gray-600 hover:text-gray-900">
                  {t('services.citizenship')}
                </a>
              </li>
            </ul>
          </div>

          {/* Support */}
          <div>
            <h3 className="text-sm font-semibold text-gray-900 tracking-wider uppercase">
              {t('nav.help')}
            </h3>
            <ul className="mt-4 space-y-2">
              <li>
                <a href="/training" className="text-sm text-gray-600 hover:text-gray-900">
                  {t('nav.training')}
                </a>
              </li>
              <li>
                <a href="#" className="text-sm text-gray-600 hover:text-gray-900">
                  Contacto
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-gray-200">
          <p className="text-center text-sm text-gray-600">
            © {currentYear} SILA - Sistema Integrado Local de Administração. República de Angola.
          </p>
        </div>
      </div>
    </footer>
  )
}

export default Footer