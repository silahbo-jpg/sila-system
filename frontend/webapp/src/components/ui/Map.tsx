import React, { useEffect, useRef, useState, useCallback } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap, useMapEvents } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { useLeafletGeoSearch } from '../../hooks/useLeafletGeoSearch';
import { GeoSearchResultWithAddress } from '../../types/leaflet-geosearch';

// Tipos para camadas temáticas
export type MapLayer = {
  id: string;
  name: string;
  type: 'tile' | 'geojson' | 'wms' | 'vector';
  url: string;
  attribution?: string;
  visible?: boolean;
  opacity?: number;
  zIndex?: number;
  // Para camadas GeoJSON
  data?: any;
  style?: (feature: any) => any;
  // Para camadas WMS
  layers?: string;
  format?: string;
  transparent?: boolean;
  version?: string;
};

// Corrigindo ícones padrão do Leaflet que não são carregados corretamente com webpack/vite
const defaultIcon = new L.Icon({
  iconUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png',
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon-2x.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

interface MarkerType {
  position: [number, number];
  title?: string;
  description?: string;
  id?: string | number;
  icon?: L.Icon | L.DivIcon;
  draggable?: boolean;
}

// Componente para gerenciar camadas do mapa
const MapLayers: React.FC<{
  map: L.Map | null;
  layers: MapLayer[];
  activeLayers: string[];
  onLayerChange?: (activeLayers: string[]) => void;
  onLayerClick?: (layerId: string, feature: any) => void;
}> = ({ map, layers, activeLayers, onLayerChange, onLayerClick }) => {
  const layerRefs = useRef<Record<string, L.Layer | null>>({});
  const [hoveredFeature, setHoveredFeature] = useState<any>(null);

  useEffect(() => {
    if (!map) return;

    // Cria ou remove camadas com base no estado ativo
    layers.forEach(layer => {
      const isActive = activeLayers.includes(layer.id);
      const layerExists = layerRefs.current[layer.id] !== undefined;

      if (isActive && !layerExists) {
        // Cria uma nova camada
        let newLayer: L.Layer | null = null;
        
        switch (layer.type) {
          case 'tile':
            newLayer = L.tileLayer(layer.url, {
              attribution: layer.attribution,
              opacity: layer.opacity || 1,
              zIndex: layer.zIndex || 1,
            });
            break;
            
          case 'wms':
            newLayer = L.tileLayer.wms(layer.url, {
              layers: layer.layers,
              format: layer.format || 'image/png',
              transparent: layer.transparent !== false,
              version: layer.version || '1.1.0',
              attribution: layer.attribution,
              opacity: layer.opacity || 1,
              zIndex: layer.zIndex || 1,
            });
            break;
            
          case 'geojson':
            if (layer.data) {
              newLayer = L.geoJSON(layer.data, {
                style: layer.style || {
                  color: '#3388ff',
                  weight: 2,
                  opacity: 1,
                  fillOpacity: 0.2,
                },
                onEachFeature: (feature, layer) => {
                  if (onLayerClick) {
                    layer.on({
                      click: () => onLayerClick(layer.id, feature),
                      mouseover: () => setHoveredFeature(feature),
                      mouseout: () => setHoveredFeature(null),
                    });
                  }
                },
              });
            }
            break;
        }

        if (newLayer) {
          newLayer.addTo(map);
          layerRefs.current[layer.id] = newLayer;
        }
      } else if (!isActive && layerExists && layerRefs.current[layer.id]) {
        // Remove a camada
        map.removeLayer(layerRefs.current[layer.id]!);
        delete layerRefs.current[layer.id];
      }
    });

    // Limpeza ao desmontar
    return () => {
      Object.values(layerRefs.current).forEach(layer => {
        if (layer && map.hasLayer(layer)) {
          map.removeLayer(layer);
        }
      });
      layerRefs.current = {};
    };
  }, [map, layers, activeLayers, onLayerClick]);

  // Atualiza a opacidade das camadas quando necessário
  useEffect(() => {
    layers.forEach(layer => {
      const layerInstance = layerRefs.current[layer.id];
      if (layerInstance && 'setOpacity' in layerInstance) {
        (layerInstance as L.TileLayer).setOpacity(layer.opacity || 1);
      }
    });
  }, [layers]);

  // Renderiza informações do recurso destacado
  if (hoveredFeature) {
    return (
      <div className="absolute bottom-4 left-4 z-[1000] bg-white dark:bg-gray-800 p-3 rounded shadow-md max-w-xs">
        <h4 className="font-bold text-sm mb-1">
          {hoveredFeature.properties?.name || 'Detalhes'}
        </h4>
        {Object.entries(hoveredFeature.properties || {}).map(([key, value]) => (
          <div key={key} className="text-xs">
            <span className="font-semibold">{key}:</span> {String(value)}
          </div>
        ))}
      </div>
    );
  }

  return null;
};

type MapProps = {
  /**
   * Coordenadas iniciais do mapa [latitude, longitude]
   * @default [-12.35, 17.35] // Luanda, Angola
   */
  center?: [number, number];
  /**
   * Nível de zoom inicial
   * @default 6
   */
  zoom?: number;
  /**
   * Marcadores a serem exibidos no mapa
   */
  markers?: MarkerType[];
  /**
   * Classe CSS adicional para o container do mapa
   */
  className?: string;
  /**
   * Estilo inline para o container do mapa
   */
  style?: React.CSSProperties;
  /**
   * Se a busca geográfica deve ser habilitada
   * @default true
   */
  enableSearch?: boolean;
  /**
   * Se deve permitir adicionar marcadores ao clicar no mapa
   * @default false
   */
  enableClickToAddMarker?: boolean;
  /**
   * Callback chamado quando um marcador é adicionado ao clicar no mapa
   */
  onMarkerAdded?: (marker: { position: [number, number] }) => void;
  /**
   * Callback chamado quando um local é encontrado através da busca
   */
  onLocationFound?: (result: GeoSearchResultWithAddress) => void;
  /**
   * Se deve mostrar o popup ao clicar em um marcador
   * @default true
   */
  showPopupOnClick?: boolean;
  /**
   * Estilo personalizado para o container da busca
   */
  searchControlStyle?: React.CSSProperties;
  /**
   * Placeholder para o campo de busca
   * @default 'Buscar local...'
   */
  searchPlaceholder?: string;
  
  /**
   * Camadas temáticas para exibir no mapa
   */
  layers?: MapLayer[];
  
  /**
   * IDs das camadas ativas por padrão
   */
  defaultActiveLayers?: string[];
  
  /**
   * Callback quando as camadas ativas mudam
   */
  onActiveLayersChange?: (activeLayers: string[]) => void;
  
  /**
   * Callback quando um recurso de uma camada é clicado
   */
  onLayerFeatureClick?: (layerId: string, feature: any) => void;
  
  /**
   * Se deve mostrar o painel de controle de camadas
   * @default true
   */
  showLayerControl?: boolean;
  
  /**
   * Posição do controle de camadas
   * @default 'topright'
   */
  layerControlPosition?: 'topleft' | 'topright' | 'bottomleft' | 'bottomright';
  
  /**
   * Estilo personalizado para o painel de controle de camadas
   */
  layerControlStyle?: React.CSSProperties;
};

// Componente interno para lidar com atualizações do mapa
const MapUpdater = ({ 
  center, 
  zoom, 
  onMarkerAdded,
  enableClickToAddMarker = false,
  showPopupOnClick = true
}: { 
  center: [number, number]; 
  zoom: number;
  onMarkerAdded?: (marker: { position: [number, number] }) => void;
  enableClickToAddMarker?: boolean;
  showPopupOnClick?: boolean;
}) => {
  const map = useMap();
  const [temporaryMarker, setTemporaryMarker] = useState<L.Marker | null>(null);
  
  // Atualiza a visualização do mapa quando as coordenadas mudam
  useEffect(() => {
    map.setView(center, zoom);
  }, [center, zoom, map]);
  
  // Adiciona um marcador temporário ao clicar no mapa
  const handleMapClick = useCallback((e: L.LeafletMouseEvent) => {
    if (!enableClickToAddMarker || !onMarkerAdded) return;
    
    const { lat, lng } = e.latlng;
    const position = [lat, lng] as [number, number];
    
    // Remove o marcador temporário anterior, se existir
    if (temporaryMarker) {
      map.removeLayer(temporaryMarker);
    }
    
    // Cria um novo marcador temporário
    const newMarker = L.marker([lat, lng], {
      icon: new L.Icon({
        iconUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png',
        iconRetinaUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon-2x.png',
        shadowUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41],
      }),
      draggable: true,
    });
    
    // Adiciona o popup se necessário
    if (showPopupOnClick) {
      newMarker.bindPopup(`<div class="p-2">
        <p class="font-semibold">Novo Marcador</p>
        <p class="text-sm">Lat: ${lat.toFixed(4)}, Lng: ${lng.toFixed(4)}</p>
      </div>`);
    }
    
    newMarker.addTo(map);
    setTemporaryMarker(newMarker);
    
    // Chama o callback com a posição do marcador
    onMarkerAdded({ position });
    
  }, [map, enableClickToAddMarker, onMarkerAdded, temporaryMarker, showPopupOnClick]);
  
  // Adiciona o evento de clique ao mapa
  useEffect(() => {
    if (enableClickToAddMarker) {
      map.on('click', handleMapClick);
    }
    
    return () => {
      map.off('click', handleMapClick);
      if (temporaryMarker) {
        map.removeLayer(temporaryMarker);
      }
    };
  }, [map, enableClickToAddMarker, handleMapClick, temporaryMarker]);
  
  return null;
};

/**
 * Componente de mapa interativo usando react-leaflet com suporte a busca geográfica
 * 
 * @example
 * ```tsx
 * // Exemplo básico
 * <Map 
 *   center={[-12.35, 17.35]} 
 *   zoom={6}
 *   markers={[
 *     { 
 *       position: [-12.35, 17.35], 
 *       title: 'Luanda', 
 *       description: 'Capital de Angola' 
 *     }
 *   ]}
 * />
 * 
 * // Com busca geográfica e clique para adicionar marcadores
 * <Map
 *   center={[-12.35, 17.35]}
 *   zoom={6}
 *   enableSearch={true}
 *   enableClickToAddMarker={true}
 *   onMarkerAdded={({ position }) => console.log('Novo marcador:', position)}
 *   onLocationFound={(result) => console.log('Local encontrado:', result)}
 *   searchPlaceholder="Buscar em Angola..."
 * />
 * ```
 */
const Map: React.FC<MapProps> = ({
  center = [-12.35, 17.35], // Luanda, Angola
  zoom = 6,
  markers = [],
  className = '',
  style = { height: '400px', width: '100%' },
  enableSearch = true,
  enableClickToAddMarker = false,
  onMarkerAdded,
  onLocationFound,
  showPopupOnClick = true,
  searchControlStyle,
  searchPlaceholder = 'Buscar local...',
}) => {
  const mapRef = useRef<L.Map>(null);
  const [currentCenter, setCurrentCenter] = useState<[number, number]>(center);
  const [currentZoom, setCurrentZoom] = useState(zoom);
  const [activeLayers, setActiveLayers] = useState<string[]>(defaultActiveLayers || []);
  const [showLayerPanel, setShowLayerPanel] = useState(showLayerControl !== false);
  
  // Atualiza as camadas ativas quando a prop mudar
  useEffect(() => {
    if (defaultActiveLayers) {
      setActiveLayers(defaultActiveLayers);
    }
  }, [defaultActiveLayers]);
  
  // Notifica quando as camadas ativas mudam
  useEffect(() => {
    if (onActiveLayersChange) {
      onActiveLayersChange(activeLayers);
    }
  }, [activeLayers, onActiveLayersChange]);
  
  // Alterna uma camada específica
  const toggleLayer = (layerId: string) => {
    setActiveLayers(prev => 
      prev.includes(layerId)
        ? prev.filter(id => id !== layerId)
        : [...prev, layerId]
    );
  };
  
  // Configura a busca geográfica
  const { searchControl } = useLeafletGeoSearch({
    map: mapRef.current,
    enabled: enableSearch,
    onLocationFound: (result) => {
      setCurrentCenter([result.y, result.x]);
      setCurrentZoom(15); // Zoom mais próximo ao encontrar um local
      if (onLocationFound) {
        onLocationFound(result);
      }
    },
    style: searchControlStyle,
  });
  
  // Atualiza o centro e zoom atuais quando o mapa é movido
  const handleMoveEnd = useCallback(() => {
    if (mapRef.current) {
      const newCenter = mapRef.current.getCenter();
      setCurrentCenter([newCenter.lat, newCenter.lng]);
      setCurrentZoom(mapRef.current.getZoom());
    }
  }, []);
  
  // Adiciona o controle de busca ao mapa quando disponível
  useEffect(() => {
    if (searchControl && mapRef.current) {
      // Remove o controle existente se houver
      mapRef.current.eachControl((control) => {
        if (control.getPosition() === 'topright') {
          mapRef.current?.removeControl(control);
        }
      });
      
      // Adiciona o novo controle
      mapRef.current.addControl(searchControl);
    }
  }, [searchControl]);
  
  return (
    <div className={`map-container ${className} relative`} style={style}>
      <MapContainer
        center={currentCenter}
        zoom={currentZoom}
        style={{ height: '100%', width: '100%' }}
        zoomControl={true}
        ref={mapRef}
        whenCreated={(map) => {
          mapRef.current = map;
          map.on('moveend', handleMoveEnd);
        }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        />
        
        {/* Atualizador de visualização */}
        <MapUpdater 
          center={currentCenter} 
          zoom={currentZoom} 
          onMarkerAdded={onMarkerAdded}
          enableClickToAddMarker={enableClickToAddMarker}
          showPopupOnClick={showPopupOnClick}
        />
        
        {/* Camadas temáticas */}
        {layers && layers.length > 0 && (
          <MapLayers
            map={mapRef.current}
            layers={layers}
            activeLayers={activeLayers}
            onLayerChange={onActiveLayersChange}
            onLayerClick={onLayerFeatureClick}
          />
        )}
        
        {/* Marcadores */}
        {markers.map((marker, index) => (
          <Marker 
            key={`marker-${marker.id || index}`} 
            position={marker.position}
            icon={marker.icon || defaultIcon}
            draggable={marker.draggable}
            eventHandlers={{
              click: () => {
                if (marker.title || marker.description) {
                  // Abre o popup automaticamente
                  const markerInstance = L.marker(marker.position).addTo(mapRef.current!);
                  markerInstance.bindPopup(
                    `<div class="p-2">
                      ${marker.title ? `<h3 class="font-bold mb-1">${marker.title}</h3>` : ''}
                      ${marker.description ? `<p class="text-sm">${marker.description}</p>` : ''}
                    </div>`
                  ).openPopup();
                  
                  // Remove o marcador temporário após 3 segundos
                  setTimeout(() => {
                    markerInstance.remove();
                  }, 3000);
                }
              },
            }}
          >
            {(marker.title || marker.description) && (
              <Popup>
                {marker.title && <h3 className="font-bold mb-1">{marker.title}</h3>}
                {marker.description && <p className="text-sm">{marker.description}</p>}
              </Popup>
            )}
          </Marker>
        ))}
      </MapContainer>
      
      {/* Painel de informações e controles */}
      <div className="absolute top-2 right-2 z-[1000] flex flex-col space-y-2">
        {/* Indicador de coordenadas */}
        {enableSearch && (
          <div className="bg-white dark:bg-gray-800 p-2 rounded shadow text-xs text-gray-600 dark:text-gray-300">
            {currentCenter[0].toFixed(4)}, {currentCenter[1].toFixed(4)} (zoom: {currentZoom})
          </div>
        )}
        
        {/* Controle de camadas */}
        {showLayerControl && layers && layers.length > 0 && (
          <div className="bg-white dark:bg-gray-800 rounded shadow overflow-hidden">
            <div 
              className="px-3 py-2 bg-gray-100 dark:bg-gray-700 font-medium text-sm cursor-pointer flex justify-between items-center"
              onClick={() => setShowLayerPanel(!showLayerPanel)}
            >
              <span>Camadas</span>
              <svg 
                className={`w-4 h-4 transition-transform ${showLayerPanel ? 'rotate-180' : ''}`}
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24" 
                xmlns="http://www.w3.org/2000/svg"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </div>
            
            {showLayerPanel && (
              <div className="p-2 max-h-60 overflow-y-auto">
                {layers.map(layer => (
                  <div key={layer.id} className="flex items-center mb-1">
                    <input
                      type="checkbox"
                      id={`layer-${layer.id}`}
                      checked={activeLayers.includes(layer.id)}
                      onChange={() => toggleLayer(layer.id)}
                      className="mr-2"
                    />
                    <label 
                      htmlFor={`layer-${layer.id}`}
                      className="text-sm cursor-pointer"
                    >
                      {layer.name}
                    </label>
                    
                    {activeLayers.includes(layer.id) && layer.opacity !== undefined && (
                      <input
                        type="range"
                        min="0"
                        max="1"
                        step="0.1"
                        value={layer.opacity}
                        onChange={(e) => {
                          const newOpacity = parseFloat(e.target.value);
                          const updatedLayers = layers.map(l => 
                            l.id === layer.id ? { ...l, opacity: newOpacity } : l
                          );
                          // Atualiza as camadas através das props se fornecido
                          if (onActiveLayersChange) {
                            onActiveLayersChange(activeLayers);
                          }
                        }}
                        className="ml-2 w-16"
                      />
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Map;

