import React from 'react';
import { useParams } from 'react-router-dom';
import services from '../config/services.json';
import api from './api';
import { useAuth } from '../store/auth';
import { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';

export default function ServiceView() {
  const { id } = useParams();
  const { hasRole } = useAuth();
  const { t } = useTranslation();
  const service = (services as any[]).find(s => s.id === id);
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [form, setForm] = useState<any>({});

  useEffect(() => {
    if (!service) return;
    if (service.method === 'GET') {
      setLoading(true);
      api.get(service.endpoint)
        .then(res => setData(res.data))
        .catch(e => setError(e?.response?.data?.detail || e.message))
        .finally(() => setLoading(false));
    }
  }, [id]);

  if (!service) return <div role="alert">{t('service_not_found')}</div>;
  if (!hasRole(service.rolesAllowed)) return <div role="alert">{t('access_denied')}</div>;

  if (service.method === 'GET') {
    if (loading) return <div role="status">{t('loading')}</div>;
    if (error) return <div className="text-red-600" role="alert">{t('error')}: {error}</div>;
    return (
      <div className="bg-white p-4 rounded-2xl shadow">
        <h1 className="text-xl font-semibold mb-4">{service.name}</h1>
        <div className="mb-2 text-gray-700">{service.description}</div>
        <pre className="text-sm overflow-auto bg-gray-50 p-2 rounded" aria-label={t('service_data')}>{JSON.stringify(data, null, 2)}</pre>
      </div>
    );
  }

  // POST: formulário dinâmico
  const handleChange = (e: any) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };
  const handleSubmit = async (e: any) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const res = await api.post(service.endpoint, form);
      setData(res.data);
    } catch (e: any) {
      setError(e?.response?.data?.detail || e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white p-4 rounded-2xl shadow max-w-xl mx-auto">
      <h1 className="text-xl font-semibold mb-4">{service.name}</h1>
      <div className="mb-2 text-gray-700">{service.description}</div>
      <form onSubmit={handleSubmit} className="space-y-3">
        {/* Renderiza campos dinamicamente a partir do endpoint ou um mock para demo */}
        <input
          name="campo1"
          className="w-full border rounded p-2"
          placeholder="Campo 1"
          onChange={handleChange}
        />
        <input
          name="campo2"
          className="w-full border rounded p-2"
          placeholder="Campo 2"
          onChange={handleChange}
        />
        <button className="bg-blue-600 text-white rounded px-4 py-2" disabled={loading}>
          {loading ? 'Enviando...' : 'Enviar'}
        </button>
      </form>
      {error && <div className="text-red-600 mt-2">Erro: {error}</div>}
      {data && <pre className="bg-green-50 border mt-4 p-2 rounded text-sm">{JSON.stringify(data, null, 2)}</pre>}
    </div>
  );
}

