import React from 'react';
import { useListSaude } from './hooks';

export default function SaudeList() {
  const { data, isLoading } = useListSaude();

  if (isLoading) return <p>Carregando...</p>;

  return (
    <ul>
      {data?.data.map((item) => (
        <li key={item.id}>
          {item.paciente_nome} - {item.unidade_sanitaria}
        </li>
      ))}
    </ul>
  );
} 
