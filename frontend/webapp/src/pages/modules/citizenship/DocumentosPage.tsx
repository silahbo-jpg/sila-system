import React, { useState } from 'react';
import { useAuth } from '../../../context/AuthContext';
import { MainLayout } from '../../../layouts/MainLayout';
import Button from '../../../components/ui/Button';
import LoadingSpinner from '../../../components/common/LoadingSpinner';

const DocumentosPage: React.FC = () => {
  const { user } = useAuth();
  const [isLoading, setIsLoading] = useState(false);

  const documentTypes = [
    {
      id: 'certidao-nascimento',
      name: 'Certidão de Nascimento',
      description: 'Documento oficial de nascimento',
      icon: '👶',
      time: '3-5 dias úteis',
      price: 'Gratuito',
      requiresAuth: true
    },
    {
      id: 'certidao-casamento',
      name: 'Certidão de Casamento',
      description: 'Documento oficial de casamento',
      icon: '💒',
      time: '3-5 dias úteis',
      price: 'Gratuito',
      requiresAuth: true
    },
    {
      id: 'certidao-obito',
      name: 'Certidão de Óbito',
      description: 'Documento oficial de falecimento',
      icon: '⚰️',
      time: '2-3 dias úteis',
      price: 'Gratuito',
      requiresAuth: true
    },
    {
      id: 'segunda-via-bi',
      name: 'Segunda Via do BI',
      description: 'Segunda via do Bilhete de Identidade',
      icon: '🆔',
      time: '7-10 dias úteis',
      price: 'Taxa aplicável',
      requiresAuth: true
    },
    {
      id: 'certidao-residencia',
      name: 'Certidão de Residência',
      description: 'Comprovante oficial de residência',
      icon: '🏠',
      time: '1-2 dias úteis',
      price: 'Gratuito',
      requiresAuth: true
    },
    {
      id: 'certidao-negativa',
      name: 'Certidão Negativa',
      description: 'Certidão de inexistência de fatos',
      icon: '📋',
      time: '1-2 dias úteis',
      price: 'Gratuito',
      requiresAuth: true
    }
  ];

  const handleDocumentClick = (document: any) => {
    // Redirecionar para o formulário específico do documento
    window.location.href = `/cidadania/documentos/${document.id}`;
  };

  return (
    <MainLayout>
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="bg-white shadow rounded-lg">
          <div className="px-6 py-4 border-b border-gray-200">
            <h1 className="text-2xl font-bold text-gray-900">
              Solicitar Documentos
            </h1>
            <p className="mt-1 text-sm text-gray-600">
              Escolha o tipo de documento que deseja solicitar
            </p>
          </div>

          <div className="px-6 py-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {documentTypes.map((document) => (
                <div
                  key={document.id}
                  className="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow duration-200 cursor-pointer"
                  onClick={() => handleDocumentClick(document)}
                >
                  <div className="flex items-center mb-4">
                    <div className="flex-shrink-0 bg-blue-100 rounded-md p-3">
                      <span className="text-2xl">{document.icon}</span>
                    </div>
                    <div className="ml-4">
                      <h3 className="text-lg font-medium text-gray-900">
                        {document.name}
                      </h3>
                      <p className="text-sm text-gray-500">
                        {document.description}
                      </p>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-500">Prazo:</span>
                      <span className="font-medium text-gray-900">{document.time}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-500">Taxa:</span>
                      <span className="font-medium text-gray-900">{document.price}</span>
                    </div>
                  </div>

                  <div className="mt-4">
                    <Button
                      variant="outline"
                      size="sm"
                      className="w-full"
                    >
                      Solicitar
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Informações adicionais */}
        <div className="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
            <h3 className="text-lg font-medium text-blue-900 mb-4">
              Como solicitar
            </h3>
            <ul className="space-y-3 text-sm text-blue-800">
              <li className="flex items-start">
                <svg className="h-5 w-5 text-blue-600 mr-2 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                Escolha o tipo de documento
              </li>
              <li className="flex items-start">
                <svg className="h-5 w-5 text-blue-600 mr-2 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                Preencha os dados necessários
              </li>
              <li className="flex items-start">
                <svg className="h-5 w-5 text-blue-600 mr-2 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                Acompanhe o status do pedido
              </li>
              <li className="flex items-start">
                <svg className="h-5 w-5 text-blue-600 mr-2 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                Receba o documento por email
              </li>
            </ul>
          </div>

          <div className="bg-green-50 border border-green-200 rounded-lg p-6">
            <h3 className="text-lg font-medium text-green-900 mb-4">
              Documentos necessários
            </h3>
            <ul className="space-y-2 text-sm text-green-800">
              <li className="flex items-center">
                <svg className="h-4 w-4 text-green-600 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                Bilhete de Identidade (BI)
              </li>
              <li className="flex items-center">
                <svg className="h-4 w-4 text-green-600 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                Comprovante de residência
              </li>
              <li className="flex items-center">
                <svg className="h-4 w-4 text-green-600 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                Dados pessoais atualizados
              </li>
            </ul>
          </div>
        </div>
      </div>
    </MainLayout>
  );
};

export default DocumentosPage; 
