import { useEffect, useRef } from 'react';
import { GeoSearchControl, OpenStreetMapProvider } from 'leaflet-geosearch';
import L from 'leaflet';
import 'leaflet-geosearch/dist/geosearch.css';

interface UseLeafletGeoSearchOptions {
  /**
   * Instância do mapa Leaflet
   */
  map: L.Map | null;
  /**
   * Se a busca deve ser habilitada
   * @default true
   */
  enabled?: boolean;
  /**
   * Estilo do controle de busca
   * @default 'bar'
   */
  style?: 'bar' | 'button';
  /**
   * Se deve mostrar o marcador no local pesquisado
   * @default true
   */
  showMarker?: boolean;
  /**
   * Se deve manter o nível de zoom ao pesquisar
   * @default false
   */
  retainZoomLevel?: boolean;
  /**
   * Se deve animar o zoom ao pesquisar
   * @default true
   */
  animateZoom?: boolean;
  /**
   * Se deve fechar o popup de resultados automaticamente
   * @default true
   */
  autoClose?: boolean;
  /**
   * Se deve manter o resultado da pesquisa no mapa
   * @default true
   */
  keepResult?: boolean;
  /**
   * Callback chamado quando um local é selecionado
   */
  onLocationFound?: (result: any) => void;
  /**
   * Callback chamado quando ocorre um erro na busca
   */
  onError?: (error: Error) => void;
}

/**
 * Hook personalizado para adicionar busca geográfica a um mapa Leaflet
 * 
 * @example
 * ```tsx
 * const { searchControl } = useLeafletGeoSearch({
 *   map,
 *   onLocationFound: (result) => {
 *     console.log('Local encontrado:', result);
 *   },
 *   onError: (error) => {
 *     console.error('Erro na busca:', error);
 *   },
 * });
 * ```
 */
export const useLeafletGeoSearch = ({
  map,
  enabled = true,
  style = 'bar',
  showMarker = true,
  retainZoomLevel = false,
  animateZoom = true,
  autoClose = true,
  keepResult = true,
  onLocationFound,
  onError,
}: UseLeafletGeoSearchOptions) => {
  const searchControlRef = useRef<GeoSearchControl | null>(null);
  const providerRef = useRef<OpenStreetMapProvider>(
    new OpenStreetMapProvider({
      params: {
        'accept-language': 'pt', // Idioma preferencial para resultados
        countrycodes: 'ao', // Priorizar resultados em Angola
        addressdetails: 1, // Incluir detalhes do endereço
      },
    })
  );

  useEffect(() => {
    if (!map || !enabled) return;

    // Configuração do controle de busca
    const searchControl = new GeoSearchControl({
      provider: providerRef.current,
      style,
      showMarker,
      retainZoomLevel,
      animateZoom,
      autoClose,
      keepResult,
      searchLabel: 'Buscar local...',
      notFoundMessage: 'Local não encontrado',
      showPopup: true,
      marker: {
        icon: new L.Icon({
          iconUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png',
          iconRetinaUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon-2x.png',
          shadowUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png',
          iconSize: [25, 41],
          iconAnchor: [12, 41],
          popupAnchor: [1, -34],
          shadowSize: [41, 41],
        }),
      },
      popupFormat: ({ result }) => {
        const { label, x: lng, y: lat } = result;
        return `<div class="p-2">
          <h3 class="font-bold text-sm">${label}</h3>
          <p class="text-xs text-gray-600">Lat: ${lat.toFixed(4)}, Lng: ${lng.toFixed(4)}</p>
        </div>`;
      },
    });

    // Adiciona o controle ao mapa
    map.addControl(searchControl);
    searchControlRef.current = searchControl;

    // Configura os event listeners
    const handleResultSelected = (result: any) => {
      if (onLocationFound) {
        onLocationFound(result);
      }
    };

    const handleError = (error: Error) => {
      if (onError) {
        onError(error);
      } else {
        console.error('Erro na busca geográfica:', error);
      }
    };

    map.on('geosearch/showlocation', handleResultSelected);
    map.on('geosearch/error', handleError);

    // Limpeza
    return () => {
      if (map && searchControlRef.current) {
        map.removeControl(searchControlRef.current);
        map.off('geosearch/showlocation', handleResultSelected);
        map.off('geosearch/error', handleError);
      }
    };
  }, [map, enabled, style, showMarker, retainZoomLevel, animateZoom, autoClose, keepResult, onLocationFound, onError]);

  return {
    searchControl: searchControlRef.current,
    provider: providerRef.current,
  };
};

export default useLeafletGeoSearch;

