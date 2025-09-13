import React, { useState } from 'react';
import ServiceHub from '../components/ServiceHub';
import Menu from '../components/Menu';

const ServiceHubPage: React.FC = () => {
  const [filter, setFilter] = useState<{
    departamento: string | null;
    categoria: string | null;
  }>({
    departamento: null,
    categoria: null
  });

  const [showMyRequests, setShowMyRequests] = useState<boolean>(false);

  // Lista de departamentos disponíveis
  const departamentos = [
    { id: 'cidadania', nome: 'Cidadania' },
    { id: 'comercial', nome: 'Comercial' },
    { id: 'sanitario', nome: 'Sanitário' },
    { id: 'justica', nome: 'Justiça' },
    { id: 'educacao', nome: 'Educação' },
    { id: 'saude', nome: 'Saúde' },
    { id: 'urbanismo', nome: 'Urbanismo' },
    { id: 'social', nome: 'Assistência Social' }
  ];

  // Lista de categorias disponíveis
  const categorias = [
    { id: 'documentos', nome: 'Documentos' },
    { id: 'licencas', nome: 'Licenças' },
    { id: 'certidoes', nome: 'Certidões' },
    { id: 'registros', nome: 'Registros' },
    { id: 'consultas', nome: 'Consultas' },
    { id: 'agendamentos', nome: 'Agendamentos' },
    { id: 'reclamacoes', nome: 'Reclamações' },
    { id: 'outros', nome: 'Outros' }
  ];

  // Limpa os filtros
  const handleClearFilters = () => {
    setFilter({
      departamento: null,
      categoria: null
    });
  };

  // Alterna entre mostrar todos os serviços e minhas solicitações
  const toggleMyRequests = () => {
    setShowMyRequests(!showMyRequests);
  };

  return (
    <div className="service-hub-page">
      <Menu />
      
      <div className="container mx-auto px-4 py-8">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold">Portal de Serviços</h1>
          
          <button
            className={`px-4 py-2 rounded ${showMyRequests ? 'bg-gray-200 text-gray-800' : 'bg-blue-500 text-white'}`}
            onClick={toggleMyRequests}
          >
            {showMyRequests ? 'Ver Todos os Serviços' : 'Minhas Solicitações'}
          </button>
        </div>
        
        {!showMyRequests && (
          <div className="filters bg-gray-50 p-4 rounded mb-6">
            <h2 className="text-lg font-semibold mb-2">Filtrar Serviços</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Departamento</label>
                <select
                  className="block w-full rounded-md border-gray-300 shadow-sm"
                  value={filter.departamento || ''}
                  onChange={(e) => setFilter(prev => ({
                    ...prev,
                    departamento: e.target.value || null
                  }))}
                >
                  <option value="">Todos os departamentos</option>
                  {departamentos.map(dep => (
                    <option key={dep.id} value={dep.id}>{dep.nome}</option>
                  ))}
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Categoria</label>
                <select
                  className="block w-full rounded-md border-gray-300 shadow-sm"
                  value={filter.categoria || ''}
                  onChange={(e) => setFilter(prev => ({
                    ...prev,
                    categoria: e.target.value || null
                  }))}
                >
                  <option value="">Todas as categorias</option>
                  {categorias.map(cat => (
                    <option key={cat.id} value={cat.id}>{cat.nome}</option>
                  ))}
                </select>
              </div>
            </div>
            
            <div className="mt-3 flex justify-end">
              <button
                className="px-3 py-1 bg-gray-200 text-gray-800 rounded hover:bg-gray-300"
                onClick={handleClearFilters}
              >
                Limpar Filtros
              </button>
            </div>
          </div>
        )}
        
        <ServiceHub 
          departamento={filter.departamento || undefined}
          categoria={filter.categoria || undefined}
          showRequests={showMyRequests}
        />
      </div>
    </div>
  );
};

export default ServiceHubPage;
