import { Link } from "react-router-dom";
export default function Menu() {
  return (
    <nav className="flex gap-4 p-2 bg-gray-100">
      <Link to="/servicos" className="font-bold text-blue-600">Portal de Serviços</Link>
      <Link to="/cidadania">Cidadania</Link>
      <Link to="/comercial">Comercial</Link>
      <Link to="/sanitario">Sanitário</Link>
      <Link to="/estatisticas">Estatísticas</Link>
      <Link to="/relatorios">Relatórios</Link>
      <Link to="/justica">Justiça</Link>
    </nav>
  );
}

