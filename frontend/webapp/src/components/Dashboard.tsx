import { useEffect, useState, useMemo } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
    const [data, setData] = useState({ atestados_emitidos: 0, usuarios_registrados: 0, taxas_pagas: 0, denuncias_recebidas: 0, matriculas_registradas: 0, inscricoes_faculdade_concurso: 0, status: '' });
    const [token, setToken] = useState(localStorage.getItem('token') || '');
    const navigate = useNavigate();
    
    // Create authenticated axios instance
    const authAxios = useMemo(() => {
        return axios.create({
            baseURL: 'http://localhost:8000',
            headers: { Authorization: `Bearer ${token}` }
        });
    }, [token]);

    useEffect(() => {
        if (!token) {
            navigate('/login');
            return;
        }
        axios.get('http://localhost:8000/api/dashboard/resumo', {
            headers: { Authorization: `Bearer ${token}` }
        })
            .then(res => setData(res.data))
            .catch(err => {
                if (err.response?.status === 401) {
                    localStorage.removeItem('token');
                    navigate('/login');
                }
                setData({ atestados_emitidos: 0, usuarios_registrados: 0, taxas_pagas: 0, denuncias_recebidas: 0, matriculas_registradas: 0, inscricoes_faculdade_concurso: 0, status: 'error' });
            });
    }, [token, navigate]);

    const handleAtestado = async () => {
        try {
            const res = await authAxios.post('http://localhost:8000/api/dashboard/cidadania/atestado', 
                { user_id: 1, data: new Date().toISOString() }
            );
            alert('Atestado criado: ' + res.data.atestado_id);
        } catch {
            alert('Erro ao criar atestado');
        }
    };

    const handleTaxa = async () => {
        try {
            const res = await authAxios.post('http://localhost:8000/api/dashboard/tributacao/taxa', 
                { valor: 1000, tipo: 'mercado' }
            );
            alert('Taxa registrada: ' + res.data.taxa_id);
        } catch {
            alert('Erro ao registrar taxa');
        }
    };

    const handleDenuncia = async () => {
        try {
            const res = await authAxios.post('http://localhost:8000/api/dashboard/denuncias', 
                { descricao: 'Lixo acumulado', localizacao: 'Rua Principal' }
            );
            alert('Denúncia registrada: ' + res.data.denuncia_id);
        } catch {
            alert('Erro ao registrar denúncia');
        }
    };

    const handleMatricula = async () => {
        try {
            const res = await authAxios.post('http://localhost:8000/api/dashboard/educacao/matricula', 
                { escola: 'Escola Municipal', ano_letivo: '2025' }
            );
            alert('Matrícula registrada: ' + res.data.matricula_id);
        } catch {
            alert('Erro ao registrar matrícula');
        }
    };

    const handleInscricao = async () => {
        try {
            const res = await authAxios.post('http://localhost:8000/api/dashboard/educacao/inscricao', 
                { tipo: 'faculdade', instituicao: 'Universidade Agostinho Neto' }
            );
            alert('Inscrição registrada: ' + res.data.inscricao_id);
        } catch {
            alert('Erro ao registrar inscrição');
        }
    };


    return (
        <div className="page-container py-6 md:py-8">
            <h1 className="text-2xl md:text-3xl font-bold text-gray-800 mb-6">SILA-HBO Dashboard</h1>
            
            {data.status === 'error' ? (
                <div className="bg-red-50 border-l-4 border-red-400 p-4 mb-6 rounded-md">
                    <div className="flex items-center">
                        <div className="flex-shrink-0">
                            <svg className="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                            </svg>
                        </div>
                        <div className="ml-3">
                            <p className="text-sm text-red-700">
                                Erro ao buscar dados do dashboard. Tente novamente mais tarde.
                            </p>
                        </div>
                    </div>
                </div>
            ) : (
                <div className="space-y-6">
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6">
                        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                            <h3 className="text-lg font-medium text-gray-900 mb-2">Atestados Emitidos</h3>
                            <p className="text-3xl font-semibold text-primary-600">{data.atestados_emitidos}</p>
                        </div>
                        
                        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                            <h3 className="text-lg font-medium text-gray-900 mb-2">Usuários Registrados</h3>
                            <p className="text-3xl font-semibold text-primary-600">{data.usuarios_registrados}</p>
                        </div>
                        
                        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                            <h3 className="text-lg font-medium text-gray-900 mb-2">Taxas Pagas</h3>
                            <p className="text-3xl font-semibold text-primary-600">{data.taxas_pagas}</p>
                        </div>
                        
                        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                            <h3 className="text-lg font-medium text-gray-900 mb-2">Denúncias Recebidas</h3>
                            <p className="text-3xl font-semibold text-primary-600">{data.denuncias_recebidas}</p>
                        </div>
                        
                        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                            <h3 className="text-lg font-medium text-gray-900 mb-2">Matrículas Registradas</h3>
                            <p className="text-3xl font-semibold text-primary-600">{data.matriculas_registradas}</p>
                        </div>
                        
                        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                            <h3 className="text-lg font-medium text-gray-900 mb-2">Inscrições</h3>
                            <p className="text-3xl font-semibold text-primary-600">{data.inscricoes_faculdade_concurso}</p>
                            <p className="text-xs text-gray-500 mt-1">(Faculdade/Concurso)</p>
                        </div>
                    </div>
                    
                    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                        <h2 className="text-xl font-semibold text-gray-800 mb-4">Ações Rápidas</h2>
                        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4" role="group" aria-label="Ações rápidas">
                            <button 
                                type="button" 
                                onClick={handleAtestado} 
                                className="flex items-center justify-center py-3 px-4 bg-blue-500 text-white hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 rounded-md transition-colors shadow-sm"
                            >
                                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"></path>
                                </svg>
                                Emitir Atestado
                            </button>
                            <button 
                                type="button" 
                                onClick={handleTaxa} 
                                className="flex items-center justify-center py-3 px-4 bg-green-500 text-white hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 rounded-md transition-colors shadow-sm"
                            >
                                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                </svg>
                                Pagar Taxa
                            </button>
                            <button 
                                type="button" 
                                onClick={handleDenuncia} 
                                className="flex items-center justify-center py-3 px-4 bg-red-500 text-white hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 rounded-md transition-colors shadow-sm"
                            >
                                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
                                </svg>
                                Registrar Denúncia
                            </button>
                            <button 
                                type="button" 
                                onClick={handleMatricula} 
                                className="flex items-center justify-center py-3 px-4 bg-purple-500 text-white hover:bg-purple-600 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 rounded-md transition-colors shadow-sm"
                            >
                                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
                                </svg>
                                Registrar Matrícula
                            </button>
                            <button 
                                type="button" 
                                onClick={handleInscricao} 
                                className="flex items-center justify-center py-3 px-4 bg-yellow-500 text-white hover:bg-yellow-600 focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:ring-offset-2 rounded-md transition-colors shadow-sm"
                            >
                                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                                </svg>
                                Registrar Inscrição
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Dashboard;

