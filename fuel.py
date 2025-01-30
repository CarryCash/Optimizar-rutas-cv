import numpy as np
from geopy.distance import geodesic
import requests


# Temas relacionados - Teorema de Green, Aceleracion tangencial y normal, Integral de Linea

# OpenWeather API key
API_KEY = "048f5fec87756ded93d9be89b501a7e9"

def get_weather_data(lat, lon):
   
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data['cod'] == 200:
        return {
            "wind_speed": data['wind']['speed'],
            "wind_direction": data['wind']['deg']
        }
    else:
        return None

def compute_distance(lat1, lon1, lat2, lon2):
 
    start = (lat1, lon1)
    end = (lat2, lon2)
    distance = geodesic(start, end).meters
    return distance

def compute_travel_time(distance, vessel_speed):
    """
    Calcula el tiempo de viaje basado en la distancia y la velocidad del buque.

    Args:
        distance (float): Distancia recorrida por el buque (en metros).
        vessel_speed (float): Velocidad del buque (en m/s).

    Returns:
        float: Tiempo de viaje en horas.
    """
    travel_time_seconds = distance / vessel_speed
    travel_time_hours = travel_time_seconds / 3600
    return travel_time_hours

def compute_fuel_consumption(travel_time_hours, fuel_consumption_rate):
  
    fuel_consumption = travel_time_hours * fuel_consumption_rate
    return fuel_consumption

def optimize_fuel_consumption(lat1, lon1, lat2, lon2, initial_speed, fuel_consumption_rate, speed_increment=1, max_iterations=100):
    """
    Optimiza el consumo de combustible ajustando la velocidad del buque.

    Args:
        lat1, lon1: Coordenadas del punto de partida.
        lat2, lon2: Coordenadas del punto de llegada.
        initial_speed (float): Velocidad inicial del buque (en m/s).
        fuel_consumption_rate (float): Tasa de consumo de combustible (en litros por hora).
        speed_increment (float): Incremento de velocidad para la optimización (en m/s).
        max_iterations (int): Número máximo de iteraciones para la optimización.

    Returns:
        tuple: Velocidad óptima, consumo de combustible mínimo y consumo de combustible actual.
    """
    distance = compute_distance(lat1, lon1, lat2, lon2)
    
    # Calcular el consumo de combustible con la velocidad inicial
    initial_travel_time_hours = compute_travel_time(distance, initial_speed)
    initial_fuel_consumption = compute_fuel_consumption(initial_travel_time_hours, fuel_consumption_rate)
    
    best_speed = initial_speed
    best_fuel_consumption = initial_fuel_consumption

    for _ in range(max_iterations):
        current_speed = initial_speed + _ * speed_increment
        travel_time_hours = compute_travel_time(distance, current_speed)
        fuel_consumption = compute_fuel_consumption(travel_time_hours, fuel_consumption_rate)

        if fuel_consumption < best_fuel_consumption:
            best_fuel_consumption = fuel_consumption
            best_speed = current_speed

    return best_speed, best_fuel_consumption, initial_fuel_consumption

def optimize_navigation(lat1, lon1, lat2, lon2, vessel_speed, fuel_consumption_rate):
    """
    Optimiza la navegación del buque utilizando cálculo vectorial y datos meteorológicos.

    Args:
        lat1, lon1: Coordenadas del punto de partida.
        lat2, lon2: Coordenadas del punto de llegada.
        vessel_speed (float): Velocidad del buque (en m/s).
        fuel_consumption_rate (float): Tasa de consumo de combustible (en litros por hora).

    Returns:
        dict: Información optimizada de navegación, incluyendo tiempo de viaje, consumo de combustible y efectos del viento.
    """
    # Calcular la distancia entre los puntos
    distance = compute_distance(lat1, lon1, lat2, lon2)

    # Obtener datos meteorológicos para los puntos de interés
    weather_start = get_weather_data(lat1, lon1)
    weather_end = get_weather_data(lat2, lon2)

    if not weather_start or not weather_end:
        return {"error": "No se pudieron obtener datos meteorológicos."}

    # Promediar los datos del viento
    avg_wind_speed = (weather_start['wind_speed'] + weather_end['wind_speed']) / 2
    avg_wind_direction = (weather_start['wind_direction'] + weather_end['wind_direction']) / 2

    # Optimizar la velocidad del buque para el consumo de combustible
    optimal_speed, min_fuel_consumption, current_fuel_consumption = optimize_fuel_consumption(lat1, lon1, lat2, lon2, vessel_speed, fuel_consumption_rate)

    # Calcular tiempo de viaje
    travel_time_hours = compute_travel_time(distance, optimal_speed)

    # Resultado
    return {
        "distance_meters": distance,
        "optimal_speed_mps": optimal_speed,
        "min_fuel_consumption_liters": min_fuel_consumption,
        "current_fuel_consumption_liters": current_fuel_consumption,
        "travel_time_hours": travel_time_hours,
        "avg_wind_speed": avg_wind_speed,
        "avg_wind_direction": avg_wind_direction
    }

# Ejemplo de uso
lat1, lon1 = -2.2700, -79.90  # Puerto Marítimo de Guayaquil
lat2, lon2 = 9.35, -79.915 # Canal de Panamá
vessel_speed = 15  # m/s
fuel_consumption_rate = 225  # litros por hora

results = optimize_navigation(lat1, lon1, lat2, lon2, vessel_speed, fuel_consumption_rate)

if "error" in results:
    print(results["error"])
else:
    print(f"Velocidad óptima: {results['optimal_speed_mps']:.2f} m/s")
    print(f"Consumo mínimo de combustible: {results['min_fuel_consumption_liters']:.2f} litros")
    print(f"Consumo actual de combustible: {results['current_fuel_consumption_liters']:.2f} litros")
    print(f"Velocidad promedio del viento: {results['avg_wind_speed']:.2f} m/s")
    print(f"Dirección promedio del viento: {results['avg_wind_direction']:.2f}°")
