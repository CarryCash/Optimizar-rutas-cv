import streamlit as st
import folium
import datetime
import pandas as pd
import requests
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster, HeatMap
import os
from find_distance import find_shortest_seaport_distance

# Path to the CSV file
DF_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "world_seaports.csv"))


# OpenWeather API key
API_KEY = "048f5fec87756ded93d9be89b501a7e9"  

def get_weather_data(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data['cod'] == 200:
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        wind_speed = data['wind']['speed']
        wind_direction = data['wind']['deg']
        return weather_description, temperature, wind_speed, wind_direction
    else:
        return None, None, None, None


# Function that translates source and destination names to coordinates
def get_src_dst_latLng(df: pd.DataFrame, source_name: str, dest_name: str):
    source_row = df[df["name"] == source_name].iloc[0]
    dest_row = df[df["name"] == dest_name].iloc[0]

    src_lng = source_row["Longitude"]
    src_lat = source_row["Latitude"]

    dst_lng = dest_row["Longitude"]
    dst_lat = dest_row["Latitude"]

    return src_lng, src_lat, dst_lng, dst_lat

# Function to extract intermediate ports along the route (this is a simplified placeholder)
def get_intermediate_ports(route, seaport_data):
    intermediate_ports = []
    countries_crossed = set()
    
    for coord in route:
        # Find nearest port to the coordinate (this is a simplified placeholder logic)
        nearest_port = seaport_data.iloc[((seaport_data['Latitude'] - coord[0])**2 + (seaport_data['Longitude'] - coord[1])**2).idxmin()]
        port_name = nearest_port['name']
        country = nearest_port['Country']
        
        if port_name not in intermediate_ports:
            intermediate_ports.append(port_name)
            countries_crossed.add(country)
    
    return intermediate_ports, list(countries_crossed)

def add_weather_effects(m, seaports_data):
    # Lists for heatmap data and wind vectors
    heatmap_data = []
    wind_data = []

    for _, row in seaports_data.iterrows():
        lat = row['Latitude']
        lon = row['Longitude']

        # Get weather data for the seaport
        weather_desc, temp, wind_speed, wind_direction = get_weather_data(lat, lon)
        
        # Heatmap data (temperature)
        if temp is not None:
            heatmap_data.append([lat, lon, temp])
        
        # Wind vectors (add lines to represent wind direction)
        if wind_speed is not None:
            wind_data.append({
                "lat": lat,
                "lon": lon,
                "speed": wind_speed,
                "direction": wind_direction
            })
            
    # Add heatmap layer
    if heatmap_data:
        HeatMap(heatmap_data).add_to(m)

    # Add wind vectors
    for wind in wind_data:
        folium.Marker(
            location=[wind['lat'], wind['lon']],
            icon=folium.Icon(icon="cloud", color="blue"),
            popup=f"Wind Speed: {wind['speed']} m/s\nWind Direction: {wind['direction']}°"
        ).add_to(m)
        
    return m


# Adding custom CSS styling
st.markdown("""
    <style>
    /* General App Styling */
    body {
        background-color: #f4f4f9;
        font-family: 'Arial', sans-serif;
    }
    
    h1, h2, h3, h4 {
        color: white;
        font-weight: 600;
    }

    /* Sidebar Styling */
    .sidebar .sidebar-content {
        background-color: #34495e;
        color: white;
        padding: 1rem;
    }

    .sidebar .sidebar-content h1 {
        color: white;
    }

    .css-1gkgrw6 {
        margin-top: 20px;
    }

    /* Styling for the Map */
    .leaflet-container {
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        padding: 10px;
    }

    /* Table Styling */
    .stTable {
        margin-top: 20px;
        background-color: #ffffff;
        border-radius: 8px;
        border: 1px solid #ddd;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        padding: 15px;
    }

    .stTable th {
        background-color: #2980b9;
        color: white;
    }

    .stTable td {
        color: #34495e;
    }

    /* Button Styling */
    .css-12oz5g7 {
        background-color: #3498db;
        color: white;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        border-radius: 5px;
        cursor: pointer;
    }

    .css-12oz5g7:hover {
        background-color: #2980b9;
    }

    </style>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    # Sidebar and main title
    st.sidebar.title("Planificador de Rutas ")
    st.title("Distancia Marítima entre Puertos")

    # Load data
    seaports_data = pd.read_csv(DF_PATH)

    # Sidebar dropdowns for selecting source and destination
    seaport_names = seaports_data['name'].unique()
    source_port = st.sidebar.selectbox("Punto de Partida", seaport_names)
    destination_port = st.sidebar.selectbox("Punto de Llegada", seaport_names)

    # Sidebar toggle for map layers
    heatmap_toggle = st.sidebar.checkbox("Mapa de calor de la actividad del puerto marítimo", value=False)

    # Map settings
    map_center = [20.0, 0.0]  # Neutral center
    m = folium.Map(location=map_center, zoom_start=2)

    # Adding cluster markers for all seaports (this can be optional)
    marker_cluster = MarkerCluster().add_to(m)
    for _, row in seaports_data.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"<b>{row['name']}</b><br>Region: {row['D_Region']}<br>Country: {row['Country']}",
            tooltip=f"{row['name']} ({row['Country']})"
        ).add_to(marker_cluster)

    # Add heatmap layer if toggled
    if heatmap_toggle:
        heatmap_data = [[row['Latitude'], row['Longitude']] for _, row in seaports_data.iterrows()]
        HeatMap(heatmap_data).add_to(m)

    # Display the map with seaports and optional heatmap
    folium_static(m)

    # Calculate shortest sea distance and display on map
    if source_port == destination_port:
        st.write("<H3>Los puertos de origen y destino son los mismos. Selecciona otros puertos.</H3>", unsafe_allow_html=True)
    else:
        # Obtener las coordenadas del puerto de origen y destino
        src_lng, src_lat, dst_lng, dst_lat = get_src_dst_latLng(seaports_data, source_port, destination_port)
        
        # Llamada a la función para obtener la distancia más corta y la ruta
        result_obj = find_shortest_seaport_distance(srcLng=src_lng, srcLat=src_lat, dstLng=dst_lng, dstLat=dst_lat)
        
        # Obtener la distancia mínima y el camino de coordenadas
        min_sea_dist = result_obj["length"]
        coord_path = result_obj["coordinate_path"]
        
        # Mostrar resultados en la interfaz
        st.write(f"<H4>La distancia más corta por mar entre {source_port} y {destination_port} es: {min_sea_dist} km</H4>", unsafe_allow_html=True)

        # Obtener la duración estimada (esto es solo un ejemplo, ajusta según sea necesario)
        estimated_duration = datetime.timedelta(hours=48)  # Ejemplo de duración de 2 días
        estimated_arrival = datetime.datetime.now() + estimated_duration
        estimated_arrival_str = estimated_arrival.strftime("%d de %B de %Y %H:%M")
        
        st.write(f"<b>Hora de salida:</b> {datetime.datetime.now().strftime('%d de %B de %Y %H:%M')}", unsafe_allow_html=True)
        st.write(f"<b>Resultado:</b>", unsafe_allow_html=True)
        st.write(f"<b>Distancia:</b> {min_sea_dist} km", unsafe_allow_html=True)
        st.write(f"<b>Distancia en ECA:</b> 0 km", unsafe_allow_html=True)  # Este dato puede ser calculado si se tiene la información
        st.write(f"<b>Duración estimada:</b> {estimated_duration.days} días {estimated_duration.seconds // 3600} horas", unsafe_allow_html=True)
        st.write(f"<b>Llegada estimada:</b> {estimated_arrival_str}", unsafe_allow_html=True)
        
        # Listar puertos intermedios y el cruce por el Canal de Panamá (o cualquier otro cruce relevante)
        intermediate_ports, countries_crossed = get_intermediate_ports(coord_path, seaports_data)
        
        weather_src = get_weather_data(src_lat, src_lng)
        weather_dst = get_weather_data(dst_lat, dst_lng)
        
        if weather_src[0]:
            st.write(f"<b>Clima en {source_port}:</b> {weather_src[0]}, {weather_src[1]}°C, Viento: {weather_src[2]} m/s, Dirección: {weather_src[3]}°", unsafe_allow_html=True)
        if weather_dst[0]:
            st.write(f"<b>Clima en {destination_port}:</b> {weather_dst[0]}, {weather_dst[1]}°C, Viento: {weather_dst[2]} m/s, Dirección: {weather_dst[3]}°", unsafe_allow_html=True)
        


        
        st.write(f"<b>Cruce:</b> Canal de Panamá", unsafe_allow_html=True)  # Aquí puedes ajustar el cruce relevante
        
        # Crear el mapa para visualizar la ruta
        m2 = folium.Map(location=map_center, zoom_start=2)

        # Dibujar la línea que representa la ruta entre el origen y el destino
        folium.PolyLine(
            coord_path,  # Lista de coordenadas que definen la ruta
            color="darkblue",  # Color de la línea
            weight=4,  # Grosor de la línea
            opacity=0.7  # Opacidad de la línea
        ).add_to(m2)

        # Agregar marcadores para los puertos de origen y destino
        folium.Marker(
            location=[src_lat, src_lng],
            icon=folium.Icon(color="green"),
            popup=f"{source_port}",
            tooltip="Source Port"
        ).add_to(m2)

        folium.Marker(
            location=[dst_lat, dst_lng],
            icon=folium.Icon(color="red"),
            popup=f"{destination_port}",
            tooltip="Destination Port"
        ).add_to(m2)

        # Mostrar el mapa con la ruta trazada
        folium_static(m2)
