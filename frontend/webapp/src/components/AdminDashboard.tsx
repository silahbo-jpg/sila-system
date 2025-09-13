import React, { useState, useEffect } from 'react';
import { Card, Select, Spin, Row, Col, Statistic } from 'antd';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { UserOutlined, FileTextOutlined, DollarOutlined } from '@ant-design/icons';
import api from '../services/api';

interface Municipio {
  id: number;
  nome: string;
  provincia: string;
  comunas?: Comuna[];
}

interface Comuna {
  id: number;
  nome: string;
  tipo: 'sede' | 'comuna';
  municipio_id: number;
}

interface DashboardData {
  estatisticas: {
    usuarios: number;
    atestados: number;
    taxas: number;
    denuncias: number;
    servicos_ativos?: number;
    municipio?: string;
    comuna?: string;
  };
}

const AdminDashboard = () => {
  const [loading, setLoading] = useState(true);
  const [municipios, setMunicipios] = useState<Municipio[]>([]);
  const [selectedMunicipio, setSelectedMunicipio] = useState<number | null>(null);
  const [selectedComuna, setSelectedComuna] = useState<number | null>(null);
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);

  // Load municipalities
  useEffect(() => {
    const loadMunicipios = async () => {
      try {
        // Development mock data - Complete 2025 Territorial Mapping
        if (import.meta.env.MODE === 'development') {
          console.log('🏛️ Using complete 2025 Territorial Mapping - Huambo Province');
          setMunicipios([
            { 
              id: 1, nome: 'Huambo', provincia: 'Huambo',
              comunas: [
                { id: 101, nome: 'Huambo', tipo: 'sede', municipio_id: 1 },
                { id: 102, nome: 'Calenga', tipo: 'comuna', municipio_id: 1 },
                { id: 103, nome: 'Chipipa', tipo: 'comuna', municipio_id: 1 }
              ]
            },
            { 
              id: 2, nome: 'Bailundo', provincia: 'Huambo',
              comunas: [
                { id: 201, nome: 'Bailundo', tipo: 'sede', municipio_id: 2 },
                { id: 202, nome: 'Lunge', tipo: 'comuna', municipio_id: 2 },
                { id: 203, nome: 'Luvemba', tipo: 'comuna', municipio_id: 2 },
                { id: 204, nome: 'Hengue', tipo: 'comuna', municipio_id: 2 }
              ]
            },
            { 
              id: 3, nome: 'Caála', provincia: 'Huambo',
              comunas: [
                { id: 301, nome: 'Caála', tipo: 'sede', municipio_id: 3 },
                { id: 302, nome: 'Catata', tipo: 'comuna', municipio_id: 3 }
              ]
            },
            { 
              id: 4, nome: 'Londuimbali', provincia: 'Huambo',
              comunas: [
                { id: 401, nome: 'Londuimbali', tipo: 'sede', municipio_id: 4 },
                { id: 402, nome: 'Ussoque', tipo: 'comuna', municipio_id: 4 }
              ]
            },
            { 
              id: 5, nome: 'Ecunha', provincia: 'Huambo',
              comunas: [
                { id: 501, nome: 'Ecunha', tipo: 'sede', municipio_id: 5 },
                { id: 502, nome: 'Chiumbo', tipo: 'comuna', municipio_id: 5 }
              ]
            },
            { 
              id: 6, nome: 'Cachiungo', provincia: 'Huambo',
              comunas: [
                { id: 601, nome: 'Cachiungo', tipo: 'sede', municipio_id: 6 },
                { id: 602, nome: 'Mbave', tipo: 'comuna', municipio_id: 6 },
                { id: 603, nome: 'Chinhama', tipo: 'comuna', municipio_id: 6 }
              ]
            },
            { 
              id: 7, nome: 'Ucuma', provincia: 'Huambo',
              comunas: [
                { id: 701, nome: 'Ucuma', tipo: 'sede', municipio_id: 7 },
                { id: 702, nome: 'Mundundo', tipo: 'comuna', municipio_id: 7 }
              ]
            },
            { 
              id: 8, nome: 'Chicala-Cholohanga', provincia: 'Huambo',
              comunas: [
                { id: 801, nome: 'Chicala-Cholohanga', tipo: 'sede', municipio_id: 8 },
                { id: 802, nome: 'Chiumbo', tipo: 'comuna', municipio_id: 8 }
              ]
            },
            { 
              id: 9, nome: 'Mungo', provincia: 'Huambo',
              comunas: [
                { id: 901, nome: 'Mungo', tipo: 'sede', municipio_id: 9 },
                { id: 902, nome: 'Cambuengo', tipo: 'comuna', municipio_id: 9 }
              ]
            },
            { 
              id: 10, nome: 'Chinjenje', provincia: 'Huambo',
              comunas: [
                { id: 1001, nome: 'Chinjenje', tipo: 'sede', municipio_id: 10 }
                // Note: Galanga was promoted from comuna to municipality
              ]
            },
            { 
              id: 11, nome: 'Longonjo', provincia: 'Huambo',
              comunas: [
                { id: 1101, nome: 'Longonjo', tipo: 'sede', municipio_id: 11 }
              ]
            },
            { 
              id: 12, nome: 'Bimbe', provincia: 'Huambo',
              comunas: [
                { id: 1201, nome: 'Bimbe', tipo: 'sede', municipio_id: 12 },
                { id: 1202, nome: 'Chissamba', tipo: 'comuna', municipio_id: 12 }
              ]
            },
            { 
              id: 13, nome: 'Cuima', provincia: 'Huambo',
              comunas: [
                { id: 1301, nome: 'Cuima', tipo: 'sede', municipio_id: 13 },
                { id: 1302, nome: 'Gove', tipo: 'comuna', municipio_id: 13 }
              ]
            },
            { 
              id: 14, nome: 'Galanga', provincia: 'Huambo',
              comunas: [
                { id: 1401, nome: 'Galanga', tipo: 'sede', municipio_id: 14 }
                // Note: Promoted from comuna of Chinjenje to independent municipality
              ]
            },
            { 
              id: 15, nome: 'Alto Hama', provincia: 'Huambo',
              comunas: [
                { id: 1501, nome: 'Alto Hama', tipo: 'sede', municipio_id: 15 },
                { id: 1502, nome: 'Chisseia', tipo: 'comuna', municipio_id: 15 }
              ]
            },
            { 
              id: 16, nome: 'Chilata', provincia: 'Huambo',
              comunas: [
                { id: 1601, nome: 'Chilata', tipo: 'sede', municipio_id: 16 }
              ]
            },
            { 
              id: 17, nome: 'Sambo', provincia: 'Huambo',
              comunas: [
                { id: 1701, nome: 'Sambo', tipo: 'sede', municipio_id: 17 },
                { id: 1702, nome: 'Luvemba', tipo: 'comuna', municipio_id: 17 }
                // Note: Luvemba parte desmembrada
              ]
            }
          ]);
          return;
        }
        
        const data = await api.getDashboardMunicipios();
        setMunicipios(data);
      } catch (error) {
        console.error('Erro ao carregar municípios:', error);
        // Fallback to mock data even in production if API fails
        setMunicipios([
          { id: 1, nome: 'Huambo', provincia: 'Huambo' } // Capital
        ]);
      }
    };
    loadMunicipios();
  }, []);

  // Load dashboard data
  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      try {
        // Development mock data
        if (import.meta.env.MODE === 'development') {
          console.log('📈 Using mock dashboard data for Huambo Province');
          const selectedMunicipioObj = municipios.find(m => m.id === selectedMunicipio);
          const selectedComunaObj = selectedMunicipioObj?.comunas?.find(c => c.id === selectedComuna);
          
          let displayName = 'Todos os 17 Municípios';
          if (selectedMunicipioObj) {
            displayName = selectedMunicipioObj.nome;
            if (selectedComunaObj) {
              displayName += ` - ${selectedComunaObj.nome} (${selectedComunaObj.tipo})`;
            }
          }
          
          setDashboardData({
            estatisticas: {
              usuarios: selectedComuna ? Math.floor(Math.random() * 200) + 50 : 
                       selectedMunicipio ? Math.floor(Math.random() * 500) + 200 : 2847,
              atestados: selectedComuna ? Math.floor(Math.random() * 20) + 5 :
                        selectedMunicipio ? Math.floor(Math.random() * 50) + 10 : 234,
              taxas: selectedComuna ? Math.floor(Math.random() * 40) + 10 :
                    selectedMunicipio ? Math.floor(Math.random() * 100) + 25 : 567,
              denuncias: selectedComuna ? Math.floor(Math.random() * 8) + 2 :
                        selectedMunicipio ? Math.floor(Math.random() * 20) + 5 : 89,
              servicos_ativos: 12,
              municipio: displayName,
              comuna: selectedComunaObj?.nome
            }
          });
          setLoading(false);
          return;
        }
        
        const data = await api.getDashboardResumo(selectedMunicipio || undefined);
        setDashboardData(data);
      } catch (error) {
        console.error('Erro ao carregar dados:', error);
        // Fallback to mock data if API fails
        setDashboardData({
          estatisticas: {
            usuarios: 0,
            atestados: 0,
            taxas: 0,
            denuncias: 0
          }
        });
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, [selectedMunicipio, selectedComuna, municipios]);

  // Reset commune selection when municipality changes
  useEffect(() => {
    setSelectedComuna(null);
  }, [selectedMunicipio]);

  if (loading) return <div className="flex justify-center p-8"><Spin size="large" /></div>;

  return (
    <div className="p-4">
      <div className="flex justify-between items-center mb-6 p-4 bg-angola-red rounded-lg">
        <h1 className="text-xl font-bold text-white flex items-center">
          <span className="mr-3 text-angola-gold">
            <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2L1 12h3v9h6v-6h4v6h6v-9h3L12 2zm0 2.8L18 10v9h-2v-6h-8v6H6v-9l6-7.2z" />
            </svg>
          </span>
          <div className="flex flex-col">
            <span>Painel Administrativo SILA-HUAMBO</span>
            <span className="text-sm text-angola-gold font-normal">Mapeamento Territorial 2025 - 17 Municípios + Comunas</span>
          </div>
        </h1>
        <div className="flex gap-4">
          <Select
            placeholder="Selecione o município"
            style={{ width: 250 }}
            onChange={setSelectedMunicipio}
            allowClear
            className="border-angola-gold"
          >
            {municipios.map(m => (
              <Select.Option key={m.id} value={m.id}>
                {m.nome} - {m.provincia}
              </Select.Option>
            ))}
          </Select>
          
          {selectedMunicipio && municipios.find(m => m.id === selectedMunicipio)?.comunas && (
            <Select
              placeholder="Selecione a comuna"
              style={{ width: 200 }}
              onChange={setSelectedComuna}
              allowClear
              className="border-angola-gold"
            >
              {municipios.find(m => m.id === selectedMunicipio)?.comunas?.map(c => (
                <Select.Option key={c.id} value={c.id}>
                  {c.nome} {c.tipo === 'sede' ? '(Sede)' : '(Comuna)'}
                </Select.Option>
              ))}
            </Select>
          )}
        </div>
      </div>

      <Row gutter={[16, 16]} className="mb-6">
        <Col xs={24} md={8}>
          <Card>
            <Statistic
              title="Usuários"
              value={dashboardData?.estatisticas?.usuarios || 0}
              prefix={<UserOutlined />}
            />
          </Card>
        </Col>
        <Col xs={24} md={8}>
          <Card>
            <Statistic
              title="Atestados"
              value={dashboardData?.estatisticas?.atestados || 0}
              prefix={<FileTextOutlined />}
            />
          </Card>
        </Col>
        <Col xs={24} md={8}>
          <Card>
            <Statistic
              title="Taxas"
              value={dashboardData?.estatisticas?.taxas || 0}
              prefix={<DollarOutlined />}
            />
          </Card>
        </Col>
      </Row>
      
      {/* Administrative Division Info */}
      <Row gutter={[16, 16]} className="mb-6">
        <Col xs={24}>
          <Card className="border-angola-gold/30">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold text-angola-black mb-2">
                  Província do Huambo
                  {selectedMunicipio && (
                    <span className="text-angola-red ml-2">
                      » {municipios.find(m => m.id === selectedMunicipio)?.nome}
                    </span>
                  )}
                  {selectedComuna && (
                    <span className="text-angola-gold ml-2">
                      » {municipios.find(m => m.id === selectedMunicipio)?.comunas?.find(c => c.id === selectedComuna)?.nome}
                    </span>
                  )}
                </h3>
                <p className="text-gray-600">
                  <span className="font-medium text-angola-red">17 Municípios</span> conforme a Nova Divisão Político-Administrativa
                  aprovada pela Assembleia Nacional (Mapeamento Territorial 2025)
                </p>
                
                {selectedMunicipio && (() => {
                  const selectedMunicipioObj = municipios.find(m => m.id === selectedMunicipio);
                  const comunas = selectedMunicipioObj?.comunas || [];
                  
                  return (
                    <div className="text-sm text-gray-600 mt-2 p-3 bg-angola-gold/10 rounded border-l-4 border-angola-red">
                      <strong className="text-angola-red">Município de {selectedMunicipioObj?.nome}:</strong>
                      <div className="mt-1 grid grid-cols-1 gap-1">
                        {comunas.map((comuna, index) => (
                          <div key={comuna.id} className="flex items-center">
                            <span className="text-angola-gold mr-2">•</span>
                            <span className="font-medium">{comuna.nome}</span>
                            <span className="ml-1 text-xs text-gray-500">
                              ({comuna.tipo === 'sede' ? 'sede municipal' : 'comuna'})
                            </span>
                          </div>
                        ))}
                      </div>
                      <div className="mt-2 text-xs text-angola-black">
                        Total: <strong>{comunas.length} {comunas.length === 1 ? 'comuna' : 'comunas'}</strong>
                      </div>
                    </div>
                  );
                })()}
                
                <p className="text-sm text-gray-500 mt-1">
                  Capital: <span className="font-medium text-angola-gold">Huambo</span> | 
                  Sistema: <span className="font-medium">SILA - Sistema Integrado Local de Administração</span>
                </p>
              </div>
              <div className="text-right">
                <div className="text-2xl font-bold text-angola-red">17</div>
                <div className="text-sm text-gray-500">Municípios</div>
                {selectedMunicipio && (() => {
                  const selectedMunicipioObj = municipios.find(m => m.id === selectedMunicipio);
                  const comunaCount = selectedMunicipioObj?.comunas?.length || 0;
                  
                  return (
                    <div className="mt-2">
                      <div className="text-lg font-semibold text-angola-gold">{comunaCount}</div>
                      <div className="text-xs text-gray-400">{comunaCount === 1 ? 'Comuna' : 'Comunas'}</div>
                    </div>
                  );
                })()}
              </div>
            </div>
          </Card>
        </Col>
      </Row>

      <Card title="Distribuição de Serviços" className="mb-6">
        <div style={{ height: 300 }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={[
              { name: 'Atestados', value: dashboardData?.estatisticas?.atestados || 0 },
              { name: 'Taxas', value: dashboardData?.estatisticas?.taxas || 0 },
              { name: 'Denúncias', value: dashboardData?.estatisticas?.denuncias || 0 },
            ]}>
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#D71A28" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </Card>
    </div>
  );
};

export default AdminDashboard;

