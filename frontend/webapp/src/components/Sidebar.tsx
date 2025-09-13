import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

function Sidebar() {
  const { role } = useAuth();
  return (
    <aside className="w-64 bg-gray-800 text-white p-4 space-y-4">
      <h2 className="text-xl font-bold">SILA - HUAMBO</h2>
      <nav className="flex flex-col space-y-2">
        <Link to="/dashboard" className="hover:bg-gray-700 p-2 rounded">Dashboard</Link>
        <Link to="/internos" className="hover:bg-gray-700 p-2 rounded">Internos</Link>
        {role === 'admin' || role === 'secretario' || role === 'atendente' ? (
          <Link to="/cidadania" className="hover:bg-gray-700 p-2 rounded">Cidadania</Link>
        ) : null}
        {role === 'admin' || role === 'secretario' ? (
          <Link to="/comercial" className="hover:bg-gray-700 p-2 rounded">Comercial</Link>
        ) : null}
        {role === 'admin' || role === 'secretario' ? (
          <Link to="/sanitario" className="hover:bg-gray-700 p-2 rounded">Sanitário</Link>
        ) : null}
        {role === 'admin' || role === 'secretario' ? (
          <Link to="/estatisticas" className="hover:bg-gray-700 p-2 rounded">Estatísticas</Link>
        ) : null}
        {role === 'admin' || role === 'secretario' ? (
          <Link to="/relatorios" className="hover:bg-gray-700 p-2 rounded">Relatórios</Link>
        ) : null}
        {role === 'admin' ? (
          <Link to="/justica" className="hover:bg-gray-700 p-2 rounded">Justiça</Link>
        ) : null}
        <button
          onClick={() => {
            localStorage.removeItem('token');
            window.location.href = '/login';
          }}
          className="mt-4 bg-red-600 hover:bg-red-700 p-2 rounded"
        >
          Sair
        </button>
      </nav>
    </aside>
  );
}

export default Sidebar;

