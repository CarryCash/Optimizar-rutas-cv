import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import os
from find_distance import find_shortest_seaport_distance  # Asegúrate de que esta función esté correctamente implementada

# Ruta al archivo CSV
DF_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "world_seaports.csv"))

# Función para traducir nombres de puertos a coordenadas
def get_src_dst_rest_latLng(df: pd.DataFrame, source_name: str, rest_name: str, dest_name: str):
    source_row = df[df["name"] == source_name].iloc[0]
    rest_row = df[df["name"] == rest_name].iloc[0]
    dest_row = df[df["name"] == dest_name].iloc[0]

    src_lng, src_lat = source_row["Longitude"], source_row["Latitude"]
    rest_lng, rest_lat = rest_row["Longitude"], rest_row["Latitude"]
    dst_lng, dst_lat = dest_row["Longitude"], dest_row["Latitude"]

    return src_lng, src_lat, rest_lng, rest_lat, dst_lng, dst_lat

if __name__ == "__main__":
    st.sidebar.title("Planificador de Rutas")
    st.title("Mapa Interactivo y Planificación de Rutas")

    # Cargar datos de puertos
    seaports_data = pd.read_csv(DF_PATH)
    seaport_names = seaports_data['name'].unique()

    # Selección de puertos por el usuario
    source_port = st.sidebar.selectbox("Puerto de Partida", seaport_names)
    rest_port = st.sidebar.selectbox("Puerto Intermedio", seaport_names)
    destination_port = st.sidebar.selectbox("Puerto de Llegada", seaport_names)

    # Asegurarse de que los puertos sean distintos
    if source_port == destination_port or source_port == rest_port or rest_port == destination_port:
        st.write("<H3>Selecciona diferentes puertos para el punto de partida, escala y llegada.</H3>", unsafe_allow_html=True)
    else:
        # Obtener coordenadas de los puertos seleccionados
        src_lng, src_lat, rest_lng, rest_lat, dst_lng, dst_lat = get_src_dst_rest_latLng(
            seaports_data, source_port, rest_port, destination_port
        )

        # Calcular rutas para formar el triángulo
        route_1 = find_shortest_seaport_distance(srcLng=src_lng, srcLat=src_lat, dstLng=rest_lng, dstLat=rest_lat)
        route_2 = find_shortest_seaport_distance(srcLng=rest_lng, srcLat=rest_lat, dstLng=dst_lng, dstLat=dst_lat)
        route_3 = find_shortest_seaport_distance(srcLng=dst_lng, srcLat=dst_lat, dstLng=src_lng, dstLat=src_lat)

        # Distancia total
        total_distance = route_1["length"] + route_2["length"] + route_3["length"]

        # Combinar coordenadas para formar el camino triangular
        coord_path = route_1["coordinate_path"] + route_2["coordinate_path"] + route_3["coordinate_path"]

        st.write(f"<H4>La distancia total por mar entre {source_port}, {rest_port}, y {destination_port} es: {total_distance} km</H4>", unsafe_allow_html=True)

        # Crear el mapa
        m = folium.Map(location=[(src_lat + dst_lat) / 2, (src_lng + dst_lng) / 2], zoom_start=4)

        # Añadir la ruta triangular al mapa
        folium.PolyLine(coord_path, color="blue", weight=4, opacity=0.7).add_to(m)

        # Añadir marcadores para cada puerto
        folium.Marker([src_lat, src_lng], icon=folium.Icon(color="green"), popup=f"{source_port}").add_to(m)
        folium.Marker([rest_lat, rest_lng], icon=folium.Icon(color="orange"), popup=f"{rest_port}").add_to(m)
        folium.Marker([dst_lat, dst_lng], icon=folium.Icon(color="red"), popup=f"{destination_port}").add_to(m)

        # Mostrar el mapa interactivo
        st.write("Haz clic en el mapa para obtener las coordenadas de cualquier punto.")
        map_data = st_folium(m, height=500, width=700)

        # Mostrar las coordenadas de los puertos seleccionados
        st.write("### Coordenadas de los vértices del triángulo:")
        st.write(f"**{source_port}:** Latitud: {src_lat}, Longitud: {src_lng}")
        st.write(f"**{rest_port}:** Latitud: {rest_lat}, Longitud: {rest_lng}")
        st.write(f"**{destination_port}:** Latitud: {dst_lat}, Longitud: {dst_lng}")

        # Capturar clics del usuario en el mapa
        if map_data["last_clicked"] is not None:
            clicked_lat = map_data["last_clicked"]["lat"]
            clicked_lng = map_data["last_clicked"]["lng"]

            # Mostrar las coordenadas seleccionadas por el usuario
            st.write("### Coordenadas seleccionadas:")
            st.write(f"**Latitud:** {clicked_lat}")
            st.write(f"**Longitud:** {clicked_lng}")
