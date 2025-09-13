import { useState } from "react";
import axios from "axios";
import { useAuth } from "../../webapp/src/context/AuthContext";

const apiPost = (url, data, token) =>
  axios.post(url, data, { headers: { Authorization: `Bearer ${token}` } });

export default function JusticePage() {
  const { token } = useAuth();
  const [certificates, setCertificates] = useState([]);
  const [processes, setProcesses] = useState([]);
  const [mediations, setMediations] = useState([]);
  const [form, setForm] = useState({ type: "", status: "", citizen_id: "" });

  const fetchCertificates = async () => {
    const res = await axios.get("/api/justice/certificates/", {
      headers: { Authorization: `Bearer ${token}` },
    });
    setCertificates(res.data);
  };

  const handleIssueCertificate = async (e) => {
    e.preventDefault();
    await apiPost("/api/justice/certificates/", form, token);
    fetchCertificates();
  };

  const fetchProcesses = async () => {
    const res = await axios.get("/api/justice/processes/", {
      headers: { Authorization: `Bearer ${token}` },
    });
    setProcesses(res.data);
  };

  const handleRequestMediation = async (e) => {
    e.preventDefault();
    await apiPost("/api/justice/mediation/", form, token);
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Justiça</h1>

      <form onSubmit={handleIssueCertificate} className="mb-4 flex gap-2">
        <input
          placeholder="Tipo"
          value={form.type}
          onChange={e => setForm(f => ({ ...f, type: e.target.value }))}
          className="border px-2"
        />
        <input
          placeholder="Status"
          value={form.status}
          onChange={e => setForm(f => ({ ...f, status: e.target.value }))}
          className="border px-2"
        />
        <input
          placeholder="ID do Cidadão"
          value={form.citizen_id}
          onChange={e => setForm(f => ({ ...f, citizen_id: e.target.value }))}
          className="border px-2"
        />
        <button className="bg-blue-600 text-white px-3 py-1">Emitir Certidão</button>
      </form>

      <button onClick={fetchCertificates} className="bg-gray-700 text-white px-3 py-1 mb-2">
        Listar Certidões
      </button>
      <ul>
        {certificates.map((c) => (
          <li key={c.id}>
            {c.type} - {c.status} - {c.citizen_id} - {c.issue_date}
          </li>
        ))}
      </ul>

      <button onClick={fetchProcesses} className="bg-gray-700 text-white px-3 py-1 mt-4 mb-2">
        Listar Processos
      </button>
      <ul>
        {processes.map((p) => (
          <li key={p.id}>
            {p.process_number} - {p.court} - {p.status} - {p.citizen_id}
          </li>
        ))}
      </ul>

      <form onSubmit={handleRequestMediation} className="mt-4 flex gap-2">
        <input
          placeholder="Tipo de Mediação"
          value={form.type}
          onChange={e => setForm(f => ({ ...f, type: e.target.value }))}
          className="border px-2"
        />
        <input
          placeholder="Status"
          value={form.status}
          onChange={e => setForm(f => ({ ...f, status: e.target.value }))}
          className="border px-2"
        />
        <input
          placeholder="Descrição"
          value={form.description || ""}
          onChange={e => setForm(f => ({ ...f, description: e.target.value }))}
          className="border px-2"
        />
        <input
          placeholder="ID do Cidadão"
          value={form.citizen_id}
          onChange={e => setForm(f => ({ ...f, citizen_id: e.target.value }))}
          className="border px-2"
        />
        <button className="bg-green-600 text-white px-3 py-1">Solicitar Mediação</button>
      </form>
    </div>
  );
}

