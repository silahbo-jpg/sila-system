import React from 'react';
import { formatMoney, formatDate, formatId } from '../utils/formatters';

interface CitizenInfoCardProps {
  citizen: {
    fullName: string;
    birthDate: string;
    biNumber?: string;
    cpfNumber?: string;
    monthlyIncome?: number;
    lastPaymentDate?: string;
    lastPaymentAmount?: number;
  };
}

const CitizenInfoCard: React.FC<CitizenInfoCardProps> = ({ citizen }) => {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-6">
      <h2 className="text-xl font-semibold mb-4 text-gray-800">Informações do Cidadão</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Nome Completo */}
        <div className="mb-4">
          <p className="text-sm font-medium text-gray-500">Nome Completo</p>
          <p className="mt-1 text-gray-900">{citizen.fullName}</p>
        </div>

        {/* Data de Nascimento */}
        <div className="mb-4">
          <p className="text-sm font-medium text-gray-500">Data de Nascimento</p>
          <p className="mt-1 text-gray-900">
            {formatDate(citizen.birthDate)}
          </p>
        </div>

        {/* Documentos */}
        {citizen.biNumber && (
          <div className="mb-4">
            <p className="text-sm font-medium text-gray-500">Bilhete de Identidade</p>
            <p className="mt-1 text-gray-900 font-mono">
              {formatId(citizen.biNumber)}
            </p>
          </div>
        )}

        {citizen.cpfNumber && (
          <div className="mb-4">
            <p className="text-sm font-medium text-gray-500">CPF</p>
            <p className="mt-1 text-gray-900 font-mono">
              {formatId(undefined, citizen.cpfNumber)}
            </p>
          </div>
        )}

        {/* Renda Mensal */}
        {citizen.monthlyIncome !== undefined && (
          <div className="mb-4">
            <p className="text-sm font-medium text-gray-500">Renda Mensal</p>
            <p className="mt-1 text-gray-900">
              {formatMoney(citizen.monthlyIncome)}
            </p>
          </div>
        )}

        {/* Último Pagamento */}
        {citizen.lastPaymentDate && citizen.lastPaymentAmount !== undefined && (
          <div className="mb-4">
            <p className="text-sm font-medium text-gray-500">Último Pagamento</p>
            <div className="flex justify-between items-center mt-1">
              <span className="text-gray-900">
                {formatDate(citizen.lastPaymentDate)}
              </span>
              <span className="text-green-600 font-medium">
                {formatMoney(citizen.lastPaymentAmount)}
              </span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default CitizenInfoCard;

