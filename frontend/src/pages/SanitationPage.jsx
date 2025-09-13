import { useState } from "react";
import axios from "axios";
import { useAuth } from "../../webapp/src/context/AuthContext";

export default function SanitationPage() {
  const { token } = useAuth();
  const [certidoes, setCertidoes] = useState([]);
  const [form, setForm] = useState({ titular: "", local_atividade: "", finalidade: "" });

  const fetchCertidoes = async () => {
    const res = await axios.get("/api/sanitation/certidoes/", {
      headers: { Authorization: `Bearer ${token}` },
    });
    setCertidoes(res.data);
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    await axios.post("/api/sanitation/certidoes/", form, {
      headers: { Authorization: `Bearer ${token}` },
    });
    fetchCertidoes();
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Sanitário</h1>
      <form onSubmit={handleCreate} className="mb-4 flex gap-2">
        <input placeholder="Titular" value={form.titular} onChange={e => setForm(f => ({ ...f, titular: e.target.value }))} className="border px-2" />
        <input placeholder="Local" value={form.local_atividade} onChange={e => setForm(f => ({ ...f, local_atividade: e.target.value }))} className="border px-2" />
        <input placeholder="Finalidade" value={form.finalidade} onChange={e => setForm(f => ({ ...f, finalidade: e.target.value }))} className="border px-2" />
        <button className="bg-blue-600 text-white px-3 py-1">Emitir Certidão</button>
      </form>
      <button onClick={fetchCertidoes} className="bg-gray-700 text-white px-3 py-1 mb-2">Listar Certidões</button>
      <ul>
        {certidoes.map(c => (
          <li key={c.id}>{c.titular} - {c.local_atividade} - {c.finalidade}</li>
        ))}
      </ul>
    </div>
  );
}

