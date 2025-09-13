import React from 'react'
import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'

function HomePage() {
  const { t } = useTranslation()

  return (
    <div className="bg-white">
      {/* Hero Section */}
      <div className="relative isolate px-6 pt-14 lg:px-8">
        <div className="mx-auto max-w-2xl py-32 sm:py-48 lg:py-56">
          <div className="text-center">
            <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
              {t('app.title')}
            </h1>
            <p className="mt-6 text-lg leading-8 text-gray-600">
              {t('app.description')}
            </p>
            <div className="mt-10 flex items-center justify-center gap-x-6">
              <Link
                to="/services"
                className="btn-primary"
              >
                {t('nav.services')}
              </Link>
              <Link
                to="/training"
                className="text-sm font-semibold leading-6 text-gray-900 hover:text-primary-600"
              >
                {t('nav.training')} <span aria-hidden="true">→</span>
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-24 sm:py-32">
        <div className="mx-auto max-w-7xl px-6 lg:px-8">
          <div className="mx-auto max-w-2xl lg:text-center">
            <h2 className="text-base font-semibold leading-7 text-primary-600">
              Serviços Digitais
            </h2>
            <p className="mt-2 text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
              {t('services.title')}
            </p>
          </div>
          <div className="mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-4xl">
            <dl className="grid max-w-xl grid-cols-1 gap-x-8 gap-y-10 lg:max-w-none lg:grid-cols-2 lg:gap-y-16">
              {[
                {
                  name: t('services.health'),
                  description: 'Agendamento de consultas e acompanhamento médico',
                  icon: '🏥',
                },
                {
                  name: t('services.citizenship'),
                  description: 'Documentos de identificação e certidões',
                  icon: '🆔',
                },
                {
                  name: t('services.education'),
                  description: 'Matrículas escolares e certificados',
                  icon: '🎓',
                },
                {
                  name: t('services.finance'),
                  description: 'Consultas fiscais e pagamentos',
                  icon: '💰',
                },
              ].map((feature) => (
                <div key={feature.name} className="relative pl-16">
                  <dt className="text-base font-semibold leading-7 text-gray-900">
                    <div className="absolute left-0 top-0 flex h-10 w-10 items-center justify-center text-2xl">
                      {feature.icon}
                    </div>
                    {feature.name}
                  </dt>
                  <dd className="mt-2 text-base leading-7 text-gray-600">
                    {feature.description}
                  </dd>
                </div>
              ))}
            </dl>
          </div>
        </div>
      </div>
    </div>
  )
}

export default HomePage