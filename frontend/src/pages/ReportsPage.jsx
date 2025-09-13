import { useState } from "react";
import axios from "axios";
import { useAuth } from "../../webapp/src/context/AuthContext";

export default function ReportsPage() {
  const { token } = useAuth();
  const [csvUrl, setCsvUrl] = useState("");
  const [pdfUrl, setPdfUrl] = useState("");

  const handleExportCsv = async () => {
    const res = await axios.get("/api/reports/exportar-csv", {
      headers: { Authorization: `Bearer ${token}` },
      responseType: "blob",
    });
    const url = window.URL.createObjectURL(new Blob([res.data]));
    setCsvUrl(url);
  };

  const handleExportPdf = async () => {
    const res = await axios.get("/api/reports/exportar-pdf", {
      headers: { Authorization: `Bearer ${token}` },
      responseType: "blob",
    });
    const url = window.URL.createObjectURL(new Blob([res.data]));
    setPdfUrl(url);
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Relatórios</h1>
      <button onClick={handleExportCsv} className="bg-blue-600 text-white px-3 py-1 mr-2">Exportar CSV</button>
      <button onClick={handleExportPdf} className="bg-green-600 text-white px-3 py-1">Exportar PDF</button>
      <div className="mt-4">
        {csvUrl && <a href={csvUrl} download="relatorio.csv" className="text-blue-700 underline">Baixar CSV</a>}
        {pdfUrl && <a href={pdfUrl} download="relatorio.pdf" className="text-green-700 underline ml-4">Baixar PDF</a>}
      </div>
    </div>
  );
}

