import 'leaflet';
import { GeoSearchControl as BaseGeoSearchControl, GeoSearchResult } from 'leaflet-geosearch';

declare module 'leaflet' {
  namespace Control {
    class GeoSearchControl extends BaseGeoSearchControl {
      constructor(options: any);
    }
  }

  namespace control {
    function geosearch(options?: any): Control.GeoSearchControl;
  }
}

export interface GeoSearchResultWithAddress extends GeoSearchResult {
  raw: {
    address?: {
      city?: string;
      country?: string;
      country_code?: string;
      county?: string;
      postcode?: string;
      road?: string;
      state?: string;
      suburb?: string;
      town?: string;
      village?: string;
    };
    display_name?: string;
    type?: string;
  };
}

export interface GeoSearchEvent extends L.LeafletEvent {
  location: GeoSearchResultWithAddress;
  locationIdx: number;
}

