import React, { useEffect, useState } from 'react';
import Sidebar from '../components/Sidebar';
import api from '../services/api';

function Dashboard() {
  const [resumo, setResumo] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    api.get('/dashboard/resumo')
      .then((res) => {
        setResumo(res.data);
        setLoading(false);
      })
      .catch(() => {
        setError("Erro ao buscar dados do backend.");
        setLoading(false);
      });
  }, []);

  return (
    <div className="flex h-screen">
      <Sidebar />
      <main className="flex-1 p-6 bg-gray-50">
        <h1 className="text-2xl font-bold text-blue-600 mb-6">Dashboard SILA-HBO</h1>
        {loading ? (
          <div className="text-gray-500">Carregando...</div>
        ) : error ? (
          <div className="text-red-600">{error}</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-white rounded shadow p-6 flex flex-col items-center">
              <span className="text-4xl font-bold text-blue-700">{resumo.municipes}</span>
              <span className="mt-2 text-gray-500">Munícipes</span>
            </div>
            <div className="bg-white rounded shadow p-6 flex flex-col items-center">
              <span className="text-4xl font-bold text-green-700">{resumo.ambulantes}</span>
              <span className="mt-2 text-gray-500">Ambulantes</span>
            </div>
            <div className="bg-white rounded shadow p-6 flex flex-col items-center">
              <span className="text-4xl font-bold text-purple-700">{resumo.documentos}</span>
              <span className="mt-2 text-gray-500">Documentos</span>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default Dashboard;

