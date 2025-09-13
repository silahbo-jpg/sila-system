import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../../webapp/src/context/AuthContext';

interface Service {
  id: number;
  slug: string;
  nome: string;
  descricao: string;
  departamento: string;
  categoria: string;
  sla_horas: number;
  requer_autenticacao: boolean;
  requer_documentos: string[];
  eventos: string[];
  ativo: boolean;
}

interface ServiceRequest {
  id: number;
  servico_id: number;
  cidadao_id: number;
  data_solicitacao: string;
  status: string;
  dados: Record<string, any>;
  documentos: string[];
  observacoes: string;
}

interface ServiceHubProps {
  departamento?: string;
  categoria?: string;
  showRequests?: boolean;
}

const ServiceHub: React.FC<ServiceHubProps> = ({ 
  departamento, 
  categoria, 
  showRequests = false 
}) => {
  const { token, user } = useAuth();
  const [services, setServices] = useState<Service[]>([]);
  const [requests, setRequests] = useState<ServiceRequest[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedService, setSelectedService] = useState<Service | null>(null);
  const [requestForm, setRequestForm] = useState<{
    dados: Record<string, any>;
    documentos: string[];
    observacoes: string;
  }>({
    dados: {},
    documentos: [],
    observacoes: ''
  });

  // Configura o axios para incluir o token em todas as requisições
  const api = axios.create({
    baseURL: '/api/service_hub',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    }
  });

  // Carrega a lista de serviços disponíveis
  useEffect(() => {
    fetchServices();
    if (showRequests && user) {
      fetchUserRequests();
    }
  }, [departamento, categoria, showRequests, user]);

  // Busca a lista de serviços
  const fetchServices = async () => {
    try {
      setLoading(true);
      setError(null);
      
      let url = '/available';
      if (departamento) {
        url = `/department/${departamento}`;
      } else if (categoria) {
        url = `/category/${categoria}`;
      }
      
      const response = await api.get(url);
      setServices(response.data);
    } catch (err) {
      console.error('Erro ao buscar serviços:', err);
      setError('Erro ao carregar a lista de serviços. Tente novamente mais tarde.');
    } finally {
      setLoading(false);
    }
  };

  // Busca as solicitações do usuário
  const fetchUserRequests = async () => {
    if (!user) return;
    
    try {
      const response = await api.get(`/requests/citizen/${user.id}`);
      setRequests(response.data);
    } catch (err) {
      console.error('Erro ao buscar solicitações:', err);
      // Não exibimos erro aqui para não atrapalhar a experiência do usuário
    }
  };

  // Seleciona um serviço para solicitar
  const handleSelectService = (service: Service) => {
    setSelectedService(service);
    // Reinicia o formulário
    setRequestForm({
      dados: {},
      documentos: [],
      observacoes: ''
    });
  };

  // Atualiza o formulário de solicitação
  const handleFormChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    
    if (name.startsWith('dados.')) {
      const fieldName = name.replace('dados.', '');
      setRequestForm(prev => ({
        ...prev,
        dados: {
          ...prev.dados,
          [fieldName]: value
        }
      }));
    } else if (name === 'observacoes') {
      setRequestForm(prev => ({
        ...prev,
        observacoes: value
      }));
    }
  };

  // Adiciona um documento à solicitação
  const handleAddDocument = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const file = e.target.files[0];
      // Em uma implementação real, você faria upload do arquivo para o servidor
      // Aqui apenas adicionamos o nome do arquivo à lista
      setRequestForm(prev => ({
        ...prev,
        documentos: [...prev.documentos, file.name]
      }));
    }
  };

  // Envia a solicitação de serviço
  const handleSubmitRequest = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!selectedService || !user) return;
    
    try {
      setLoading(true);
      setError(null);
      
      const requestData = {
        servico_id: selectedService.id,
        cidadao_id: user.id,
        dados: requestForm.dados,
        documentos: requestForm.documentos,
        observacoes: requestForm.observacoes
      };
      
      await api.post('/requests', requestData);
      
      // Limpa o formulário e atualiza a lista de solicitações
      setSelectedService(null);
      setRequestForm({
        dados: {},
        documentos: [],
        observacoes: ''
      });
      
      if (showRequests) {
        fetchUserRequests();
      }
      
      alert('Solicitação enviada com sucesso!');
    } catch (err) {
      console.error('Erro ao enviar solicitação:', err);
      setError('Erro ao enviar a solicitação. Tente novamente mais tarde.');
    } finally {
      setLoading(false);
    }
  };

  // Formata a data no formato dd/mm/yyyy
  const formatDate = (dateString: string) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR');
  };

  // Traduz o status da solicitação
  const translateStatus = (status: string) => {
    const statusMap: Record<string, string> = {
      'pendente': 'Pendente',
      'em_analise': 'Em Análise',
      'aprovado': 'Aprovado',
      'rejeitado': 'Rejeitado',
      'concluido': 'Concluído',
      'cancelado': 'Cancelado'
    };
    
    return statusMap[status] || status;
  };

  return (
    <div className="service-hub">
      {error && (
        <div className="error-message bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}
      
      {/* Lista de Serviços */}
      {!selectedService && (
        <div className="services-list">
          <h2 className="text-xl font-bold mb-4">Serviços Disponíveis</h2>
          
          {loading ? (
            <p>Carregando serviços...</p>
          ) : services.length === 0 ? (
            <p>Nenhum serviço disponível.</p>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {services.map(service => (
                <div 
                  key={service.id} 
                  className="service-card border rounded p-4 cursor-pointer hover:bg-gray-50"
                  onClick={() => handleSelectService(service)}
                >
                  <h3 className="font-bold text-lg">{service.nome}</h3>
                  <p className="text-sm text-gray-600">{service.descricao}</p>
                  <div className="mt-2 text-xs text-gray-500">
                    <p>Departamento: {service.departamento}</p>
                    <p>Categoria: {service.categoria}</p>
                    <p>Tempo estimado: {service.sla_horas} horas</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
      
      {/* Formulário de Solicitação */}
      {selectedService && (
        <div className="request-form">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-bold">Solicitar: {selectedService.nome}</h2>
            <button 
              className="text-blue-500 hover:text-blue-700"
              onClick={() => setSelectedService(null)}
            >
              Voltar para a lista
            </button>
          </div>
          
          <p className="mb-4">{selectedService.descricao}</p>
          
          <form onSubmit={handleSubmitRequest} className="space-y-4">
            {/* Campos dinâmicos baseados no serviço */}
            <div className="form-fields">
              <h3 className="font-bold mb-2">Informações Necessárias</h3>
              
              {/* Aqui você pode adicionar campos dinâmicos com base no serviço selecionado */}
              {/* Este é apenas um exemplo */}
              <div className="mb-2">
                <label className="block text-sm font-medium text-gray-700">Nome Completo</label>
                <input
                  type="text"
                  name="dados.nomeCompleto"
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                  onChange={handleFormChange}
                  required
                />
              </div>
              
              {/* Documentos */}
              {selectedService.requer_documentos && selectedService.requer_documentos.length > 0 && (
                <div className="mt-4">
                  <h3 className="font-bold mb-2">Documentos Necessários</h3>
                  <ul className="list-disc pl-5 mb-2">
                    {selectedService.requer_documentos.map((doc, index) => (
                      <li key={index}>{doc}</li>
                    ))}
                  </ul>
                  
                  <div className="mt-2">
                    <label className="block text-sm font-medium text-gray-700">Anexar Documento</label>
                    <input
                      type="file"
                      className="mt-1 block w-full"
                      onChange={handleAddDocument}
                    />
                  </div>
                  
                  {requestForm.documentos.length > 0 && (
                    <div className="mt-2">
                      <p className="text-sm font-medium">Documentos Anexados:</p>
                      <ul className="list-disc pl-5">
                        {requestForm.documentos.map((doc, index) => (
                          <li key={index} className="text-sm">{doc}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              )}
              
              {/* Observações */}
              <div className="mt-4">
                <label className="block text-sm font-medium text-gray-700">Observações</label>
                <textarea
                  name="observacoes"
                  rows={3}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                  onChange={handleFormChange}
                  value={requestForm.observacoes}
                />
              </div>
            </div>
            
            <div className="flex justify-end">
              <button
                type="submit"
                className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                disabled={loading}
              >
                {loading ? 'Enviando...' : 'Enviar Solicitação'}
              </button>
            </div>
          </form>
        </div>
      )}
      
      {/* Lista de Solicitações do Usuário */}
      {showRequests && requests.length > 0 && !selectedService && (
        <div className="user-requests mt-8">
          <h2 className="text-xl font-bold mb-4">Minhas Solicitações</h2>
          
          <div className="overflow-x-auto">
            <table className="min-w-full bg-white">
              <thead>
                <tr className="bg-gray-100 text-gray-600 uppercase text-sm leading-normal">
                  <th className="py-3 px-6 text-left">Serviço</th>
                  <th className="py-3 px-6 text-left">Data</th>
                  <th className="py-3 px-6 text-left">Status</th>
                  <th className="py-3 px-6 text-left">Observações</th>
                </tr>
              </thead>
              <tbody className="text-gray-600 text-sm">
                {requests.map(request => {
                  const service = services.find(s => s.id === request.servico_id);
                  return (
                    <tr key={request.id} className="border-b border-gray-200 hover:bg-gray-50">
                      <td className="py-3 px-6 text-left">
                        {service ? service.nome : `Serviço #${request.servico_id}`}
                      </td>
                      <td className="py-3 px-6 text-left">
                        {formatDate(request.data_solicitacao)}
                      </td>
                      <td className="py-3 px-6 text-left">
                        <span className={`px-2 py-1 rounded-full text-xs ${request.status === 'aprovado' || request.status === 'concluido' ? 'bg-green-100 text-green-800' : request.status === 'rejeitado' || request.status === 'cancelado' ? 'bg-red-100 text-red-800' : 'bg-yellow-100 text-yellow-800'}`}>
                          {translateStatus(request.status)}
                        </span>
                      </td>
                      <td className="py-3 px-6 text-left">
                        {request.observacoes || '-'}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

export default ServiceHub;
