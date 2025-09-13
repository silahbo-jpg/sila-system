import { useState } from "react";
import axios from "axios";
import { useAuth } from "../../webapp/src/context/AuthContext";

export default function StatisticsPage() {
  const { token } = useAuth();
  const [stats, setStats] = useState([]);

  const fetchStats = async () => {
    const res = await axios.get("/api/statistics/monthly-report", {
      headers: { Authorization: `Bearer ${token}` },
    });
    setStats(res.data);
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Estatísticas</h1>
      <button onClick={fetchStats} className="bg-blue-600 text-white px-3 py-1 mb-2">Gerar Relatório Mensal</button>
      <ul>
        {stats.map((s, i) => (
          <li key={i}>{s.mes} - {s.total_atestados} atestados, {s.total_licencas} licenças, {s.total_certidoes} certidões</li>
        ))}
      </ul>
    </div>
  );
}

