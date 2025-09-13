import React, { useState } from 'react';
import { Meta, StoryObj } from '@storybook/react';
import Map from './Map';
import { GeoSearchResultWithAddress } from '../../types/leaflet-geosearch';

const meta: Meta<typeof Map> = {
  title: 'Components/Map',
  component: Map,
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component: 'Um componente de mapa interativo usando react-leaflet com suporte a busca geográfica, marcadores e popups.',
      },
    },
  },
  argTypes: {
    center: {
      description: 'Coordenadas iniciais do mapa [latitude, longitude]',
      control: 'object',
    },
    zoom: {
      description: 'Nível de zoom inicial',
      control: { type: 'number', min: 1, max: 18, step: 1 },
    },
    markers: {
      description: 'Lista de marcadores a serem exibidos no mapa',
      control: 'object',
    },
    className: {
      description: 'Classe CSS adicional para o container do mapa',
      control: 'text',
    },
    style: {
      description: 'Estilo inline para o container do mapa',
      control: 'object',
    },
  },
};

export default {
  ...meta,
  decorators: [
    (Story) => (
      <MemoryRouter>
        <Story />
      </MemoryRouter>
    ),
  ],
};

type Story = StoryObj<typeof Map>;

export const Default: Story = {
  args: {
    center: [-12.35, 17.35], // Luanda, Angola
    zoom: 6,
    style: { height: '500px' },
    enableSearch: true,
    searchPlaceholder: 'Buscar em Angola...',
  },
};

export const WithMarkers: Story = {
  args: {
    center: [-12.35, 17.35], // Luanda, Angola
    zoom: 6,
    style: { height: '500px' },
    markers: [
      {
        position: [-12.35, 17.35],
        title: 'Luanda',
        description: 'Capital de Angola',
      },
      {
        position: [-8.83, 13.23],
        title: 'Luanda',
        description: 'Província de Luanda',
      },
      {
        position: [-12.57, 16.15],
        title: 'Huambo',
        description: 'Cidade do Huambo',
      },
    ],
    enableSearch: true,
    searchPlaceholder: 'Buscar local...',
  },
};

export const CustomStyle: Story = {
  args: {
    center: [-12.35, 17.35],
    zoom: 6,
    className: 'border-2 border-gray-300 rounded-lg overflow-hidden',
    style: { height: '400px', width: '90%', margin: '0 auto' },
    markers: [
      {
        position: [-12.35, 17.35],
        title: 'Luanda',
        description: 'Capital de Angola',
      },
    ],
    enableSearch: true,
    searchPlaceholder: 'Buscar em Luanda...',
    searchControlStyle: {
      position: 'topright',
      autoClose: true,
      style: 'button',
      searchLabel: 'Buscar',
    },
  },
};

export const WithClickToAddMarker: Story = {
  render: () => {
    const [markers, setMarkers] = useState([
      {
        position: [-12.35, 17.35] as [number, number],
        title: 'Luanda',
        description: 'Capital de Angola',
      },
    ]);

    const handleMarkerAdded = ({ position }: { position: [number, number] }) => {
      setMarkers(prev => [
        ...prev,
        {
          position,
          title: `Marcador ${prev.length + 1}`,
          description: `Adicionado em ${new Date().toLocaleTimeString()}`,
        },
      ]);
    };

    return (
      <div className="space-y-4">
        <div className="p-4 bg-blue-50 dark:bg-blue-900/30 rounded-lg">
          <h3 className="font-bold mb-2">Instruções:</h3>
          <p className="text-sm mb-2">
            Clique em qualquer lugar do mapa para adicionar um novo marcador.
            Você também pode usar a busca no canto superior direito.
          </p>
          <p className="text-xs text-gray-600 dark:text-gray-400">
            Marcadores adicionados: {markers.length}
          </p>
        </div>
        <Map
          center={[-12.35, 17.35]}
          zoom={6}
          style={{ height: '500px' }}
          markers={markers}
          enableSearch={true}
          enableClickToAddMarker={true}
          onMarkerAdded={handleMarkerAdded}
          onLocationFound={(result) => {
            console.log('Local encontrado:', result);
          }}
          searchPlaceholder="Buscar local..."
        />
      </div>
    );
  },
};

export const WithLocationSearch: Story = {
  render: () => {
    const [selectedLocation, setSelectedLocation] = useState<{
      position: [number, number];
      address?: string;
    } | null>(null);

    const handleLocationFound = (result: GeoSearchResultWithAddress) => {
      setSelectedLocation({
        position: [result.y, result.x],
        address: result.raw.display_name || 'Endereço não disponível',
      });
    };

    return (
      <div className="space-y-4">
        <Map
          center={[-12.35, 17.35]}
          zoom={6}
          style={{ height: '500px' }}
          markers={
            selectedLocation
              ? [
                  {
                    position: selectedLocation.position,
                    title: 'Local Selecionado',
                    description: selectedLocation.address,
                  },
                ]
              : []
          }
          enableSearch={true}
          onLocationFound={handleLocationFound}
          searchPlaceholder="Buscar endereço..."
        />
        
        {selectedLocation && (
          <div className="p-4 bg-green-50 dark:bg-green-900/30 rounded-lg">
            <h3 className="font-bold mb-1">Localização Selecionada:</h3>
            <p className="text-sm">
              <span className="font-semibold">Coordenadas:</span>{' '}
              {selectedLocation.position[0].toFixed(4)}, {selectedLocation.position[1].toFixed(4)}
            </p>
            <p className="text-sm">
              <span className="font-semibold">Endereço:</span>{' '}
              {selectedLocation.address}
            </p>
          </div>
        )}
      </div>
    );
  },
};

export const WithThematicLayers: Story = {
  render: () => {
    // Dados de exemplo para camadas temáticas
    const [activeLayers, setActiveLayers] = useState<string[]>(['satellite', 'provinces']);
    const [clickedFeature, setClickedFeature] = useState<any>(null);

    // Camadas de exemplo
    const layers = [
      {
        id: 'satellite',
        name: 'Satélite',
        type: 'tile' as const,
        url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
        opacity: 0.8,
      },
      {
        id: 'terrain',
        name: 'Relevo',
        type: 'tile' as const,
        url: 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
        attribution: 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)',
        opacity: 0.7,
      },
      {
        id: 'provinces',
        name: 'Províncias de Angola',
        type: 'geojson' as const,
        url: 'https://raw.githubusercontent.com/dadosabertosdefeira/geodata-brasil/master/geojson/geojs-31-mun.json', // URL de exemplo, substituir por dados reais de Angola
        style: (feature: any) => ({
          color: '#4f46e5',
          weight: 2,
          opacity: 1,
          fillColor: '#818cf8',
          fillOpacity: 0.3,
        }),
        // Dados estáticos de exemplo (seriam carregados via URL em produção)
        data: {
          type: 'FeatureCollection',
          features: [
            {
              type: 'Feature',
              properties: { name: 'Luanda' },
              geometry: {
                type: 'Polygon',
                coordinates: [
                  [
                    [12.3, -9.2],
                    [14.5, -9.2],
                    [14.5, -7.9],
                    [12.3, -7.9],
                    [12.3, -9.2],
                  ],
                ],
              },
            },
            // Adicione mais províncias conforme necessário
          ],
        },
      },
    ];

    // Função para lidar com clique em um recurso de camada
    const handleLayerFeatureClick = (layerId: string, feature: any) => {
      console.log('Recurso clicado:', { layerId, feature });
      setClickedFeature({
        layerId,
        properties: feature.properties,
        geometry: feature.geometry.type,
      });
    };

    return (
      <div className="space-y-4">
        <div className="p-4 bg-blue-50 dark:bg-blue-900/30 rounded-lg">
          <h3 className="font-bold mb-2">Camadas Temáticas</h3>
          <p className="text-sm">
            Use o painel de camadas no canto superior direito para ativar/desativar diferentes camadas.
            Clique em qualquer área do mapa para ver detalhes.
          </p>
        </div>

        <Map
          center={[-12.35, 17.35]}
          zoom={6}
          style={{ height: '600px' }}
          enableSearch={true}
          searchPlaceholder="Buscar em Angola..."
          layers={layers}
          defaultActiveLayers={activeLayers}
          onActiveLayersChange={setActiveLayers}
          onLayerFeatureClick={handleLayerFeatureClick}
          showLayerControl={true}
        />

        {clickedFeature && (
          <div className="p-4 bg-white dark:bg-gray-800 rounded-lg shadow">
            <h3 className="font-bold mb-2">Detalhes do Recurso</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <h4 className="font-semibold text-sm">Camada:</h4>
                <p className="text-sm">
                  {layers.find(l => l.id === clickedFeature.layerId)?.name || clickedFeature.layerId}
                </p>
              </div>
              <div>
                <h4 className="font-semibold text-sm">Tipo:</h4>
                <p className="text-sm">{clickedFeature.geometry}</p>
              </div>
              <div className="md:col-span-2">
                <h4 className="font-semibold text-sm mb-1">Propriedades:</h4>
                <div className="bg-gray-50 dark:bg-gray-700 p-3 rounded text-sm overflow-x-auto">
                  <pre className="text-xs">
                    {JSON.stringify(clickedFeature.properties, null, 2)}
                  </pre>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    );
  },
};

export const WithReverseGeocoding: Story = {
  render: () => {
    const [selectedLocation, setSelectedLocation] = useState<{
      position: [number, number];
      address?: string;
      loading: boolean;
    } | null>(null);

    // Função para buscar endereço a partir de coordenadas (geocodificação reversa)
    const reverseGeocode = async (lat: number, lng: number): Promise<string> => {
      try {
        const response = await fetch(
          `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&zoom=18&addressdetails=1`
        );
        const data = await response.json();
        return data.display_name || 'Endereço não encontrado';
      } catch (error) {
        console.error('Erro na geocodificação reversa:', error);
        return 'Não foi possível obter o endereço';
      }
    };

    // Manipulador de clique no mapa
    const handleMapClick = async (e: L.LeafletMouseEvent) => {
      const { lat, lng } = e.latlng;
      
      setSelectedLocation({
        position: [lat, lng],
        address: 'Buscando endereço...',
        loading: true,
      });

      // Busca o endereço para as coordenadas clicadas
      const address = await reverseGeocode(lat, lng);
      
      setSelectedLocation({
        position: [lat, lng],
        address,
        loading: false,
      });
    };

    return (
      <div className="space-y-4">
        <div className="p-4 bg-blue-50 dark:bg-blue-900/30 rounded-lg">
          <h3 className="font-bold mb-2">Geocodificação Reversa</h3>
          <p className="text-sm">
            Clique em qualquer lugar do mapa para ver as coordenadas e o endereço correspondente.
            O endereço será obtido através do serviço de geocodificação reversa do OpenStreetMap.
          </p>
        </div>

        <Map
          center={[-12.35, 17.35]}
          zoom={6}
          style={{ height: '500px' }}
          enableSearch={true}
          searchPlaceholder="Buscar local..."
          onClick={handleMapClick}
          markers={
            selectedLocation
              ? [
                  {
                    position: selectedLocation.position,
                    title: 'Local Selecionado',
                    description: selectedLocation.address,
                  },
                ]
              : []
          }
        />

        {selectedLocation && (
          <div className="p-4 bg-white dark:bg-gray-800 rounded-lg shadow">
            <h3 className="font-bold mb-2">Localização Selecionada</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <h4 className="font-semibold text-sm">Coordenadas:</h4>
                <p className="text-sm font-mono">
                  {selectedLocation.position[0].toFixed(6)}, {selectedLocation.position[1].toFixed(6)}
                </p>
              </div>
              <div>
                <h4 className="font-semibold text-sm">Endereço:</h4>
                {selectedLocation.loading ? (
                  <div className="flex items-center space-x-2">
                    <div className="animate-spin h-4 w-4 border-2 border-blue-500 border-t-transparent rounded-full"></div>
                    <span className="text-sm">Carregando...</span>
                  </div>
                ) : (
                  <p className="text-sm">{selectedLocation.address}</p>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    );
  },
};

