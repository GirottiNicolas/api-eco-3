from geopy.geocoders import Nominatim
import random

# Configura un user_agent único y descriptivo
geolocator = Nominatim(user_agent="mi_app_geolocalizacion")


def obtenerCoordenadasDe(direccion_a_buscar):
    try:
        # Obtener la ubicación
        direccion = f'{direccion_a_buscar}, Argentina'
        ubicacion = geolocator.geocode(direccion)

        # Verificar si la ubicación es válida y no es None
        if ubicacion:
            # Retornar un diccionario con latitud y longitud
            return {
                'latitud': ubicacion.latitude,
                'longitud': ubicacion.longitude
            }
        else:
            print("Ubicación no encontrada.")
            return {'latitud': None, 'longitud': None}  # o podrías retornar valores predeterminados como 0 o -1
    except Exception as e:
        print(f"Error al obtener la ubicación: {e}")
        return {'latitud': None, 'longitud': None}



def coordenadas_dispersas(lat, lon):
    # Ajusta la variación para evitar puntos demasiado cercanos
    lat_dispercion = random.uniform(-rango_lat, rango_lat)
    lon_dispercion = random.uniform(-rango_lon, rango_lon)
    return lat + lat_dispercion, lon + lon_dispercion


def generar_coordenadas_dispersas(centro_lat, centro_lon, rango_lat, rango_lon, num_puntos):
    """
    Genera coordenadas dispersas en un área geográfica específica.

    :param centro_lat: Latitud del centro del área geográfica.
    :param centro_lon: Longitud del centro del área geográfica.
    :param rango_lat: Rango de variación de latitud en grados.
    :param rango_lon: Rango de variación de longitud en grados.
    :param num_puntos: Número de coordenadas aleatorias a generar.
    :return: Lista de diccionarios con coordenadas 'latitud' y 'longitud'.
    """
    coordenadas = []
    utilizados = []

    for _ in range(num_puntos):
        while True:
            lat, lon = coordenadas_dispersas(centro_lat, centro_lon)
            if (lat, lon) not in utilizados:
                coordenadas.append({'latitud': lat, 'longitud': lon})
                utilizados.append((lat, lon))
                break

    return coordenadas


# Coordenadas base para Berazategui, Buenos Aires (aproximadas)
centro_lat = -34.7726
centro_lon = -58.2375

# Rango de variación en grados
rango_lat = 0.05  # Aproximadamente 5 km
rango_lon = 0.05  # Aproximadamente 5 km

# Número de puntos a generar
num_puntos = 10

coordenadas_dispersas = generar_coordenadas_dispersas(centro_lat, centro_lon, rango_lat, rango_lon, num_puntos)

for coordenada in coordenadas_dispersas:
    print(coordenada)
