import requests
import numpy as np

# OpenWeather API key
API_KEY = "048f5fec87756ded93d9be89b501a7e9"


# Temas relacionados vector gradiente y punto critico


def get_weather_data(lat, lon):
    """
    Obtiene los datos meteorológicos en tiempo real desde OpenWeather API.

    Args:
        lat (float): Latitud de la ubicación.
        lon (float): Longitud de la ubicación.

    Returns:
        dict: Diccionario con descripción del clima, temperatura, velocidad del viento y dirección del viento.
    """
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data['cod'] == 200:
        return {
            "weather": data['weather'][0]['description'],
            "temperature": data['main']['temp'],
            "wind_speed": data['wind']['speed'],
            "wind_direction": data['wind']['deg']
        }
    else:
        return None

def calculate_gradient(data_points):
    """
    Calcula el gradiente en base a los datos meteorológicos proporcionados.

    Args:
        data_points (list): Lista de diccionarios con datos meteorológicos (incluyendo latitud y longitud).

    Returns:
        tuple: Gradiente aproximado en la dirección de la latitud y la longitud.
    """
    latitudes = np.array([point['lat'] for point in data_points])
    longitudes = np.array([point['lon'] for point in data_points])
    temperatures = np.array([point['temperature'] for point in data_points])

    # Inicializar gradientes
    grad_lat = np.zeros(len(data_points))
    grad_lon = np.zeros(len(data_points))

    for i, point in enumerate(data_points):
        # Calcular diferencia con puntos vecinos en latitud
        lat_diffs = latitudes - point['lat']
        lon_diffs = longitudes - point['lon']

        temp_diffs = temperatures - point['temperature']

        # Evitar dividir por cero
        lat_diffs[lat_diffs == 0] = np.inf
        lon_diffs[lon_diffs == 0] = np.inf

        # Gradiente aproximado
        grad_lat[i] = np.sum(temp_diffs / lat_diffs) / len(data_points)
        grad_lon[i] = np.sum(temp_diffs / lon_diffs) / len(data_points)

    return grad_lat, grad_lon

def find_critical_points(gradient_lat, gradient_lon):
    """
    Identifica puntos críticos donde el gradiente es cercano a cero.

    Args:
        gradient_lat (numpy array): Gradiente en la dirección de la latitud.
        gradient_lon (numpy array): Gradiente en la dirección de la longitud.

    Returns:
        list: Lista de índices donde el gradiente es cercano a cero.
    """
    critical_points = np.where((np.abs(gradient_lat) < 1e-3) & (np.abs(gradient_lon) < 1e-3))
    return list(critical_points[0])

# Uso real con datos de OpenWeather
def example_usage():
    """
    Ejemplo de uso del análisis meteorológico con datos reales obtenidos de OpenWeather.
    """
    # Coordenadas del puerto marítimo de Guayaquil y el Canal de Panamá
    cities = ["Puerto Marítimo de Guayaquil", "Canal de Panamá"]
    coordinates = []

    # Coordenadas aproximadas
    guayaquil_coords = {"lat": -2.1700, "lon": -79.9220}  # Puerto Marítimo de Guayaquil
    panama_coords = {"lat": 9.0817, "lon": -79.7167}  # Canal de Panamá

    coordinates.append(guayaquil_coords)
    coordinates.append(panama_coords)

    # Obtener datos reales de clima
    for point in coordinates:
        weather_data = get_weather_data(point['lat'], point['lon'])
        if weather_data:
            point.update(weather_data)

    # Calcular gradiente
    grad_lat, grad_lon = calculate_gradient(coordinates)

    # Identificar puntos críticos
    critical_points = find_critical_points(grad_lat, grad_lon)

    print("Gradientes calculados:", grad_lat, grad_lon)
    print("Puntos críticos identificados:", critical_points)

if __name__ == "__main__":
    example_usage()
