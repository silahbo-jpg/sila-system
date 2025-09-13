import { useState } from "react";
import axios from "axios";
import { useAuth } from "../../webapp/src/context/AuthContext";

export default function CommercialPage() {
  const { token } = useAuth();
  const [licenses, setLicenses] = useState([]);
  const [form, setForm] = useState({ nome_empresa: "", cnpj: "", atividade: "" });

  const fetchLicenses = async () => {
    const res = await axios.get("/api/commercial/licenses/", {
      headers: { Authorization: `Bearer ${token}` },
    });
    setLicenses(res.data);
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    await axios.post("/api/commercial/licenses/", form, {
      headers: { Authorization: `Bearer ${token}` },
    });
    fetchLicenses();
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Comercial</h1>
      <form onSubmit={handleCreate} className="mb-4 flex gap-2">
        <input placeholder="Empresa" value={form.nome_empresa} onChange={e => setForm(f => ({ ...f, nome_empresa: e.target.value }))} className="border px-2" />
        <input placeholder="CNPJ" value={form.cnpj} onChange={e => setForm(f => ({ ...f, cnpj: e.target.value }))} className="border px-2" />
        <input placeholder="Atividade" value={form.atividade} onChange={e => setForm(f => ({ ...f, atividade: e.target.value }))} className="border px-2" />
        <button className="bg-blue-600 text-white px-3 py-1">Emitir Licença</button>
      </form>
      <button onClick={fetchLicenses} className="bg-gray-700 text-white px-3 py-1 mb-2">Listar Licenças</button>
      <ul>
        {licenses.map(l => (
          <li key={l.id}>{l.nome_empresa} - {l.cnpj} - {l.atividade}</li>
        ))}
      </ul>
    </div>
  );
}

