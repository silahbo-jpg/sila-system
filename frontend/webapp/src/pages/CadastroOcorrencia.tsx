import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Map, MapMarker } from '../components/ui/Map';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { Select } from '../components/ui/Select';

type OcorrenciaTipo = 'buraco' | 'iluminacao' | 'limpeza' | 'outro';

interface OcorrenciaFormData {
  titulo: string;
  descricao: string;
  tipo: OcorrenciaTipo;
  endereco: string;
  coordenadas: [number, number] | null;
}

const CadastroOcorrencia: React.FC = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState<OcorrenciaFormData>({
    titulo: '',
    descricao: '',
    tipo: 'outro',
    endereco: '',
    coordenadas: null,
  });
  
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [mapCenter] = useState<[number, number]>([-12.35, 17.35]); // Luanda
  const [markers, setMarkers] = useState<Array<{ position: [number, number]; title: string }>>([]);

  // Tipos de ocorrência disponíveis
  const tiposOcorrencia = [
    { value: 'buraco', label: 'Buraco na via' },
    { value: 'iluminacao', label: 'Falta de iluminação' },
    { value: 'limpeza', label: 'Falta de limpeza' },
    { value: 'outro', label: 'Outro' },
  ];

  // Atualiza os dados do formulário
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  // Manipula a seleção de localização no mapa
  const handleMapClick = (e: L.LeafletMouseEvent) => {
    const { lat, lng } = e.latlng;
    const newMarker = {
      position: [lat, lng] as [number, number],
      title: 'Local da ocorrência',
    };
    
    setMarkers([newMarker]);
    setFormData(prev => ({
      ...prev,
      coordenadas: [lat, lng],
    }));
  };

  // Atualiza o endereço quando a localização é encontrada via busca
  const handleLocationFound = (result: any) => {
    setFormData(prev => ({
      ...prev,
      endereco: result.raw.display_name || 'Endereço não disponível',
    }));
  };

  // Validação do formulário
  const isFormValid = () => {
    return (
      formData.titulo.trim() !== '' &&
      formData.descricao.trim() !== '' &&
      formData.tipo !== '' &&
      formData.coordenadas !== null
    );
  };

  // Envia o formulário
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!isFormValid()) {
      alert('Por favor, preencha todos os campos obrigatórios e selecione um local no mapa.');
      return;
    }

    setIsSubmitting(true);
    
    try {
      // Aqui você faria a chamada para a API
      console.log('Dados da ocorrência:', formData);
      
      // Simulando uma requisição assíncrona
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      alert('Ocorrência registrada com sucesso!');
      navigate('/dashboard');
    } catch (error) {
      console.error('Erro ao registrar ocorrência:', error);
      alert('Ocorreu um erro ao registrar a ocorrência. Tente novamente.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-2xl font-bold text-gray-800 dark:text-white mb-6">
          Registrar Nova Ocorrência
        </h1>
        
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 space-y-6">
            <h2 className="text-lg font-semibold text-gray-700 dark:text-gray-200">
              Dados da Ocorrência
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label htmlFor="titulo" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Título <span className="text-red-500">*</span>
                </label>
                <Input
                  id="titulo"
                  name="titulo"
                  type="text"
                  value={formData.titulo}
                  onChange={handleChange}
                  placeholder="Ex.: Buraco na avenida principal"
                  required
                />
              </div>
              
              <div>
                <label htmlFor="tipo" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Tipo de Ocorrência <span className="text-red-500">*</span>
                </label>
                <Select
                  id="tipo"
                  name="tipo"
                  value={formData.tipo}
                  onChange={handleChange}
                  options={tiposOcorrencia}
                  required
                />
              </div>
            </div>
            
            <div>
              <label htmlFor="descricao" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Descrição <span className="text-red-500">*</span>
              </label>
              <textarea
                id="descricao"
                name="descricao"
                rows={4}
                value={formData.descricao}
                onChange={handleChange}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                placeholder="Descreva detalhadamente a ocorrência..."
                required
              />
            </div>
          </div>
          
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 space-y-4">
            <h2 className="text-lg font-semibold text-gray-700 dark:text-gray-200">
              Localização
            </h2>
            
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Selecione no mapa abaixo a localização exata da ocorrência.
              Você pode usar a busca no canto superior direito do mapa.
            </p>
            
            <div className="h-96 rounded-lg overflow-hidden border border-gray-200 dark:border-gray-700">
              <Map
                center={mapCenter}
                zoom={14}
                enableSearch
                searchPlaceholder="Buscar endereço..."
                onClick={handleMapClick}
                markers={markers}
                onLocationFound={handleLocationFound}
                style={{ height: '100%', width: '100%' }}
              />
            </div>
            
            <div className="mt-4">
              <label htmlFor="endereco" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Endereço <span className="text-red-500">*</span>
              </label>
              <Input
                id="endereco"
                name="endereco"
                type="text"
                value={formData.endereco}
                onChange={handleChange}
                placeholder="Endereço será preenchido automaticamente ao selecionar no mapa"
                readOnly
                required
              />
              {formData.coordenadas && (
                <p className="mt-1 text-xs text-gray-500 dark:text-gray-400">
                  Coordenadas: {formData.coordenadas[0].toFixed(6)}, {formData.coordenadas[1].toFixed(6)}
                </p>
              )}
            </div>
          </div>
          
          <div className="flex justify-end space-x-4 pt-4">
            <Button
              type="button"
              variant="outline"
              onClick={() => navigate(-1)}
              disabled={isSubmitting}
            >
              Cancelar
            </Button>
            <Button
              type="submit"
              disabled={!isFormValid() || isSubmitting}
            >
              {isSubmitting ? 'Registrando...' : 'Registrar Ocorrência'}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CadastroOcorrencia;

