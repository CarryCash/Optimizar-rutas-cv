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

# Function that translates source, destination, and rest stop names to coordinates
def get_src_dst_rest_latLng(df: pd.DataFrame, source_name: str, rest_name: str, dest_name: str):
    source_row = df[df["name"] == source_name].iloc[0]
    rest_row = df[df["name"] == rest_name].iloc[0]
    dest_row = df[df["name"] == dest_name].iloc[0]

    src_lng, src_lat = source_row["Longitude"], source_row["Latitude"]
    rest_lng, rest_lat = rest_row["Longitude"], rest_row["Latitude"]
    dst_lng, dst_lat = dest_row["Longitude"], dest_row["Latitude"]

    return src_lng, src_lat, rest_lng, rest_lat, dst_lng, dst_lat

def add_weather_effects(m, seaports_data):
    heatmap_data = []
    wind_data = []

    for _, row in seaports_data.iterrows():
        lat = row['Latitude']
        lon = row['Longitude']
        
        weather_desc, temp, wind_speed, wind_direction = get_weather_data(lat, lon)
        
        if temp is not None:
            heatmap_data.append([lat, lon, temp])
        
        if wind_speed is not None:
            folium.Marker(
                location=[lat, lon],
                icon=folium.Icon(icon="cloud", color="blue"),
                popup=f"Wind Speed: {wind_speed} m/s\nWind Direction: {wind_direction}°"
            ).add_to(m)

    if heatmap_data:
        HeatMap(heatmap_data).add_to(m)

    return m

# Adding custom CSS styling
st.markdown("""
    <style>
    body {
        background-color: #f4f4f9;
        font-family: 'Arial', sans-serif;
    }
    
    h1, h2, h3, h4 {
        color: white;
        font-weight: 600;
    }
    .sidebar .sidebar-content {
        background-color: #34495e;
        color: white;
        padding: 1rem;
    }
    .leaflet-container {
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        padding: 10px;
    }
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
    st.sidebar.title("Planificador de Rutas")
    st.title("Distancia Marítima entre Puertos con Escala")

    seaports_data = pd.read_csv(DF_PATH)
    seaport_names = seaports_data['name'].unique()

    source_port = st.sidebar.selectbox("Punto de Partida", seaport_names)
    rest_port = st.sidebar.selectbox("Punto de Escala", seaport_names)
    destination_port = st.sidebar.selectbox("Punto de Llegada", seaport_names)

    if source_port == destination_port or source_port == rest_port or rest_port == destination_port:
        st.write("<H3>Selecciona diferentes puertos para el punto de partida, escala y llegada.</H3>", unsafe_allow_html=True)
    else:
        src_lng, src_lat, rest_lng, rest_lat, dst_lng, dst_lat = get_src_dst_rest_latLng(
            seaports_data, source_port, rest_port, destination_port
        )

        route_1 = find_shortest_seaport_distance(srcLng=src_lng, srcLat=src_lat, dstLng=rest_lng, dstLat=rest_lat)
        route_2 = find_shortest_seaport_distance(srcLng=rest_lng, srcLat=rest_lat, dstLng=dst_lng, dstLat=dst_lat)

        total_distance = route_1["length"] + route_2["length"]
        coord_path = route_1["coordinate_path"] + route_2["coordinate_path"]

        st.write(f"<H4>La distancia total por mar entre {source_port}, {rest_port}, y {destination_port} es: {total_distance} km</H4>", unsafe_allow_html=True)

        m = folium.Map(location=[(src_lat + dst_lat) / 2, (src_lng + dst_lng) / 2], zoom_start=3)

        folium.PolyLine(coord_path, color="darkblue", weight=4, opacity=0.7).add_to(m)

        folium.Marker([src_lat, src_lng], icon=folium.Icon(color="green"), popup=f"{source_port}").add_to(m)
        folium.Marker([rest_lat, rest_lng], icon=folium.Icon(color="orange"), popup=f"{rest_port}").add_to(m)
        folium.Marker([dst_lat, dst_lng], icon=folium.Icon(color="red"), popup=f"{destination_port}").add_to(m)

        folium_static(m)
