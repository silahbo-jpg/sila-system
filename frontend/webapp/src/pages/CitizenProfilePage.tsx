import React from 'react';
import CitizenInfoCard from '../components/CitizenInfoCard';

const CitizenProfilePage: React.FC = () => {
  // Dados de exemplo - em uma aplicação real, isso viria de uma API
  const citizenData = {
    fullName: 'Maria dos Santos',
    birthDate: '1985-04-15',
    biNumber: '1234567890AB12',
    cpfNumber: '12345678901',
    monthlyIncome: 125000, // Em centavos (1250,00 Kz)
    lastPaymentDate: '2025-07-15',
    lastPaymentAmount: 25000, // 250,00 Kz
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Perfil do Cidadão</h1>
      
      <div className="max-w-3xl mx-auto">
        <CitizenInfoCard citizen={citizenData} />
        
        <div className="bg-white rounded-lg shadow-md p-6 mt-6">
          <h2 className="text-lg font-semibold mb-4 text-gray-800">Histórico de Transações</h2>
          
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Data</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Descrição</th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Valor</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                <tr>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {formatDate('2025-07-15')}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    Taxa de Licenciamento
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-right font-medium text-red-600">
                    {formatMoney(25000, 'AOA')}
                  </td>
                </tr>
                <tr>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {formatDate('2025-06-10')}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    Imposto Predial
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-right font-medium text-red-600">
                    {formatMoney(42500, 'AOA')}
                  </td>
                </tr>
                <tr>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {formatDate('2025-05-05')}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    Taxa de Saneamento
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-right font-medium text-red-600">
                    {formatMoney(18000, 'AOA')}
                  </td>
                </tr>
              </tbody>
              <tfoot className="bg-gray-50">
                <tr>
                  <td colSpan={2} className="px-6 py-3 text-right text-sm font-medium text-gray-900">
                    Total Pago (Últimos 3 meses):
                  </td>
                  <td className="px-6 py-3 text-right text-sm font-bold text-gray-900">
                    {formatMoney(25000 + 42500 + 18000, 'AOA')}
                  </td>
                </tr>
              </tfoot>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CitizenProfilePage;

