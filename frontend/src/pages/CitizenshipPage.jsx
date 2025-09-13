import { useState, useEffect } from "react";
import axios from "axios";
import { useAuth } from "../../webapp/src/context/AuthContext";

// Componente para formatar a data no formato dd/mm/yyyy
const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('pt-BR');
};\n
export default function CitizenshipPage() {
  const { token } = useAuth();
  const [citizens, setCitizens] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [form, setForm] = useState({ 
    nomeCompleto: "", 
    numeroBi: "", 
    cpf: "",
    dataNascimento: "",
    naturalidade: "",
    residencia: ""
  });

  // Configura o axios para incluir o token em todas as requisições
  const api = axios.create({
    baseURL: "/api/citizenship",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    }
  });

  // Carrega a lista de cidadãos ao montar o componente
  useEffect(() => {
    fetchCitizens();
  }, []);

  // Busca a lista de cidadãos
  const fetchCitizens = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await api.get("/citizens");
      setCitizens(response.data);
    } catch (err) {
      console.error("Erro ao buscar cidadãos:", err);
      setError("Erro ao carregar a lista de cidadãos. Tente novamente mais tarde.");
    } finally {
      setLoading(false);
    }
  };

  // Manipula a criação de um novo cidadão
  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      setError(null);
      
      // Formata os dados para enviar ao servidor
      const citizenData = {
        ...form,
        dataNascimento: form.dataNascimento ? new Date(form.dataNascimento).toISOString() : null
      };
      
      await api.post("/citizens", citizenData);
      
      // Limpa o formulário e atualiza a lista
      setForm({ 
        nomeCompleto: "", 
        numeroBi: "", 
        cpf: "",
        dataNascimento: "",
        naturalidade: "",
        residencia: ""
      });
      
      fetchCitizens();
    } catch (err) {
      console.error("Erro ao criar cidadão:", err);
      setError(
        err.response?.data?.detail || 
        "Erro ao criar o registro de cidadão. Verifique os dados e tente novamente."
      );
    } finally {
      setLoading(false);
    }
  };

  // Manipula a exclusão de um cidadão
  const handleDelete = async (id) => {
    if (window.confirm("Tem certeza que deseja excluir este cidadão?")) {
      try {
        setLoading(true);
        await api.delete(`/citizens/${id}`);
        fetchCitizens();
      } catch (err) {
        console.error("Erro ao excluir cidadão:", err);
        setError("Erro ao excluir o registro. Tente novamente mais tarde.");
      } finally {
        setLoading(false);
      }
    }
  };

  // Manipula mudanças nos campos do formulário
  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm(prev => ({
      ...prev,
      [name]: value
    }));
  };

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-6 text-gray-800">Gestão de Cidadãos</h1>
      
      {/* Mensagem de erro */}
      {error && (
        <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
          {error}
        </div>
      )}
      
      {/* Formulário de cadastro */}
      <div className="bg-white p-6 rounded-lg shadow-md mb-8">
        <h2 className="text-xl font-semibold mb-4 text-gray-700">Cadastrar Novo Cidadão</h2>
        <form onSubmit={handleCreate} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Nome Completo *
              </label>
              <input
                type="text"
                name="nomeCompleto"
                value={form.nomeCompleto}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Número do BI *
              </label>
              <input
                type="text"
                name="numeroBi"
                value={form.numeroBi}
                onChange={handleChange}
                placeholder="999999999LA999"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                CPF
              </label>
              <input
                type="text"
                name="cpf"
                value={form.cpf}
                onChange={handleChange}
                placeholder="000.000.000-00"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Data de Nascimento
              </label>
              <input
                type="date"
                name="dataNascimento"
                value={form.dataNascimento}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Naturalidade
              </label>
              <input
                type="text"
                name="naturalidade"
                value={form.naturalidade}
                onChange={handleChange}
                placeholder="Cidade/Estado"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Endereço de Residência
              </label>
              <input
                type="text"
                name="residencia"
                value={form.residencia}
                onChange={handleChange}
                placeholder="Rua, Número, Bairro, Cidade"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
          
          <div className="flex justify-end pt-2">
            <button
              type="submit"
              disabled={loading}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50"
            >
              {loading ? 'Salvando...' : 'Cadastrar Cidadão'}
            </button>
          </div>
        </form>
      </div>
      
      {/* Lista de cidadãos */}
      <div className="bg-white p-6 rounded-lg shadow-md">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold text-gray-700">Lista de Cidadãos</h2>
          <button
            onClick={fetchCitizens}
            disabled={loading}
            className="px-3 py-1 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 disabled:opacity-50 text-sm"
          >
            {loading ? 'Atualizando...' : 'Atualizar Lista'}
          </button>
        </div>
        
        {loading && citizens.length === 0 ? (
          <div className="text-center py-8">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500 mx-auto"></div>
            <p className="mt-2 text-gray-600">Carregando cidadãos...</p>
          </div>
        ) : citizens.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            Nenhum cidadão cadastrado ainda.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nome</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">BI</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">CPF</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nascimento</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Naturalidade</th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Ações</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {citizens.map((citizen) => (
                  <tr key={citizen.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {citizen.nomeCompleto}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {citizen.numeroBi}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {citizen.cpf || '—'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {formatDate(citizen.dataNascimento) || '—'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {citizen.naturalidade || '—'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <button
                        onClick={() => handleDelete(citizen.id)}
                        className="text-red-600 hover:text-red-900 mr-4"
                        disabled={loading}
                      >
                        Excluir
                      </button>
                      <button className="text-blue-600 hover:text-blue-900">
                        Editar
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

