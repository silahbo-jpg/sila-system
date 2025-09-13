import React from 'react';
import { useAuth } from '../store/auth';
import services from '../config/services.json';
import { Link } from 'react-router-dom';
import { useState } from 'react';
import { useTranslation } from 'react-i18next';

export default function Servicos() {
  const { user, hasRole } = useAuth();
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('');

  // Filtra por papel, pesquisa e categoria
  const filtered = (services as any[]).filter(s =>
    hasRole(s.rolesAllowed) &&
    (!search || s.name.toLowerCase().includes(search.toLowerCase()) || s.description.toLowerCase().includes(search.toLowerCase())) &&
    (!category || s.category === category)
  );

  // Extrai categorias únicas
  const categories = Array.from(new Set((services as any[]).map(s => s.category)));

  const { t } = useTranslation();
  return (
    <div className="max-w-5xl mx-auto">
      <h1 className="text-2xl font-semibold mb-4">{t('service_catalog')}</h1>
      <div className="flex gap-2 mb-4">
        <input
          className="border rounded p-2 flex-1"
          placeholder={t('search_service')}
          value={search}
          onChange={e => setSearch(e.target.value)}
          aria-label={t('search_service')}
        />
        <select
          className="border rounded p-2"
          value={category}
          onChange={e => setCategory(e.target.value)}
          aria-label={t('category')}
        >
          <option value="">{t('all_categories')}</option>
          {categories.map(c => (
            <option key={c} value={c}>{c}</option>
          ))}
        </select>
      </div>
      <ul className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4" role="list" aria-label={t('service_list')}>
        {filtered.map(s => (
          <li key={s.id} className="bg-white rounded-2xl shadow p-4 flex flex-col justify-between" role="listitem">
            <div>
              <div className="text-lg font-semibold mb-1">{s.name}</div>
              <div className="text-gray-600 text-sm mb-2">{s.description}</div>
              <span className="inline-block text-xs bg-gray-200 rounded px-2 py-1 mb-2">{s.category}</span>
            </div>
            <Link to={`/servicos/${s.id}`} className="mt-2 inline-block text-blue-600 hover:underline" aria-label={t('access') + ' ' + s.name}>{t('access')}</Link>
          </li>
        ))}
        {filtered.length === 0 && <li className="col-span-full text-center text-gray-500" role="alert">{t('no_service_found')}</li>}
      </ul>
    </div>
  );
}

