import React, { useEffect, useState } from 'react';
import Sidebar from '../components/Sidebar';
import api from '../services/api';

function Internos() {
  const [municipes, setMunicipes] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    api.get('/municipe')
      .then((response) => {
        setMunicipes(response.data);
        setLoading(false);
      })
      .catch((error) => {
        setError('Erro ao buscar munícipes.');
        setLoading(false);
      });
  }, []);

  return (
    <div className="flex h-screen">
      <Sidebar />
      <main className="flex-1 p-6 bg-gray-50">
        <h1 className="text-2xl font-bold text-blue-600 mb-4">Lista de Munícipes</h1>
        {loading ? (
          <div className="text-gray-500">Carregando...</div>
        ) : error ? (
          <div className="text-red-600">{error}</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full bg-white shadow-md rounded">
              <thead>
                <tr className="bg-gray-200">
                  <th className="p-2 text-left">Nome</th>
                  <th className="p-2 text-left">Número BI</th>
                </tr>
              </thead>
              <tbody>
                {municipes.map((m: any, idx: number) => (
                  <tr key={m.id || idx}>
                    <td className="p-2">{m.nome}</td>
                    <td className="p-2">{m.numero_bi}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </main>
    </div>
  );
}

export default Internos;

