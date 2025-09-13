import React, { useEffect } from "react";

const SessionExpired = () => {
  useEffect(() => {
    const timer = setTimeout(() => {
      window.location.href = "/login";
    }, 2000); // tempo antes do redirecionamento

    return () => clearTimeout(timer);
  }, []);

  return (
    <div style={{ textAlign: "center", marginTop: "20vh" }}>
      <h2 className="text-xl font-bold text-red-600">Sessão expirada</h2>
      <p className="text-gray-700">Redirecionando para login...</p>
    </div>
  );
};

export default SessionExpired;

