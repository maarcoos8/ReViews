import httpx
from typing import Optional, Tuple
import logging


async def geocode_location(location_name: str) -> Optional[Tuple[float, float]]:
    """
    Obtiene las coordenadas (latitud, longitud) de una ubicación usando Nominatim (OpenStreetMap)
    
    Args:
        location_name: Nombre del país o ciudad a geocodificar
        
    Returns:
        Tupla (latitud, longitud) o None si no se encuentra
    """
    # Usar Nominatim (OpenStreetMap) - servicio gratuito
    # Documentación: https://nominatim.org/release-docs/develop/api/Search/
    url = "https://nominatim.openstreetmap.org/search"
    
    params = {
        "q": location_name,
        "format": "json",
        "limit": 1,
        "addressdetails": 1
    }
    
    headers = {
        "User-Agent": "Eventual/1.0"  # Nominatim requiere un User-Agent
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, headers=headers, timeout=10.0)
            response.raise_for_status()
            
            results = response.json()
            
            if not results or len(results) == 0:
                logging.warning(f"No se encontraron coordenadas para: {location_name}")
                return None
            
            result = results[0]
            latitude = float(result['lat'])
            longitude = float(result['lon'])
            
            logging.info(f"Geocodificado '{location_name}': ({latitude}, {longitude})")
            return (latitude, longitude)
            
    except httpx.HTTPError as e:
        logging.error(f"Error HTTP en geocoding para '{location_name}': {str(e)}")
        return None
    except (KeyError, ValueError) as e:
        logging.error(f"Error al parsear respuesta de geocoding: {str(e)}")
        return None
    except Exception as e:
        logging.error(f"Error inesperado en geocoding: {str(e)}")
        return None


async def reverse_geocode(latitude: float, longitude: float) -> Optional[str]:
    """
    Obtiene el nombre de la ubicación a partir de coordenadas (reverse geocoding)
    
    Args:
        latitude: Latitud
        longitude: Longitud
        
    Returns:
        Nombre de la ubicación o None si no se encuentra
    """
    url = "https://nominatim.openstreetmap.org/reverse"
    
    params = {
        "lat": latitude,
        "lon": longitude,
        "format": "json",
        "zoom": 10
    }
    
    headers = {
        "User-Agent": "Eventual/1.0"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, headers=headers, timeout=10.0)
            response.raise_for_status()
            
            result = response.json()
            
            if 'display_name' in result:
                return result['display_name']
            
            return None
            
    except Exception as e:
        logging.error(f"Error en reverse geocoding: {str(e)}")
        return None
