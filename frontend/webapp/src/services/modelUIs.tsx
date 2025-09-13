import React, { useEffect, useState } from 'react';
import api from './api';

// 1. Modelo GET: Tabela de consultas médicas
export function ListaConsultasMarcadas() {
  const [consultas, setConsultas] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api.get('/api/servicos/consultas')
      .then(res => setConsultas(res.data))
      .catch(e => setError(e?.response?.data?.detail || e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Carregando...</div>;
  if (error) return <div className="text-red-600">Erro: {error}</div>;

  if (!consultas.length) return <div>Nenhuma consulta encontrada.</div>;

  return (
    <table className="min-w-full bg-white rounded shadow">
      <thead>
        <tr>
          <th className="px-4 py-2">Paciente</th>
          <th className="px-4 py-2">Data</th>
          <th className="px-4 py-2">Especialidade</th>
        </tr>
      </thead>
      <tbody>
        {consultas.map((c, i) => (
          <tr key={i} className="border-t">
            <td className="px-4 py-2">{c.paciente}</td>
            <td className="px-4 py-2">{c.data}</td>
            <td className="px-4 py-2">{c.especialidade}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

// 2. Modelo POST: Formulário de inscrição escolar
export function FormInscricaoEscolar() {
  const [form, setForm] = useState({ nome: '', idade: '', escola: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);
    setLoading(true);
    try {
      await api.post('/api/servicos/inscricao-escolar', form);
      setSuccess('Inscrição realizada com sucesso!');
    } catch (e: any) {
      setError(e?.response?.data?.detail || e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-3 bg-white p-4 rounded shadow max-w-lg mx-auto">
      <h2 className="text-lg font-semibold mb-2">Inscrição Escolar</h2>
      <input name="nome" placeholder="Nome da criança" className="w-full border rounded p-2" onChange={handleChange} />
      <input name="idade" placeholder="Idade" className="w-full border rounded p-2" onChange={handleChange} />
      <input name="escola" placeholder="Escola desejada" className="w-full border rounded p-2" onChange={handleChange} />
      <button className="bg-blue-600 text-white rounded px-4 py-2" disabled={loading}>{loading ? 'Enviando...' : 'Enviar'}</button>
      {error && <div className="text-red-600 mt-2">Erro: {error}</div>}
      {success && <div className="text-green-600 mt-2">{success}</div>}
    </form>
  );
}

// 3. Modelo POST: Solicitação de ambulância
export function FormSolicitarAmbulancia() {
  const [form, setForm] = useState({ nome: '', endereco: '', motivo: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);
    setLoading(true);
    try {
      await api.post('/api/servicos/ambulancia', form);
      setSuccess('Solicitação enviada com sucesso!');
    } catch (e: any) {
      setError(e?.response?.data?.detail || e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-3 bg-white p-4 rounded shadow max-w-lg mx-auto">
      <h2 className="text-lg font-semibold mb-2">Solicitar Ambulância</h2>
      <input name="nome" placeholder="Nome do solicitante" className="w-full border rounded p-2" onChange={handleChange} />
      <input name="endereco" placeholder="Endereço" className="w-full border rounded p-2" onChange={handleChange} />
      <input name="motivo" placeholder="Motivo" className="w-full border rounded p-2" onChange={handleChange} />
      <button className="bg-blue-600 text-white rounded px-4 py-2" disabled={loading}>{loading ? 'Enviando...' : 'Enviar'}</button>
      {error && <div className="text-red-600 mt-2">Erro: {error}</div>}
      {success && <div className="text-green-600 mt-2">{success}</div>}
    </form>
  );
}

