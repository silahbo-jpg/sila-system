import React, { useState } from 'react';
import { useCreateSaude } from './hooks';

export default function SaudeForm() {
  const [data, setData] = useState({
    paciente_nome: '',
    unidade_sanitaria: '',
    atendimento_data: '',
    descricao: '',
  });

  const mutation = useCreateSaude();

  const handleSubmit = (e) => {
    e.preventDefault();
    mutation.mutate(data);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <input
        type="text"
        placeholder="Nome do paciente"
        value={data.paciente_nome}
        onChange={(e) => setData({ ...data, paciente_nome: e.target.value })}
      />
      <input
        type="text"
        placeholder="Unidade sanitária"
        value={data.unidade_sanitaria}
        onChange={(e) => setData({ ...data, unidade_sanitaria: e.target.value })}
      />
      <input
        type="date"
        value={data.atendimento_data}
        onChange={(e) => setData({ ...data, atendimento_data: e.target.value })}
      />
      <textarea
        placeholder="Descrição"
        value={data.descricao}
        onChange={(e) => setData({ ...data, descricao: e.target.value })}
      />
      <button type="submit" className="btn btn-primary">Salvar</button>
    </form>
  );
} 
