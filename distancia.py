import streamlit as st
import math
import pydeck as pdk

def calcular_distancia(lat1, lon1, lat2, lon2):
    """
    Calcula la distancia entre dos puntos geográficos usando la fórmula del haversine.
    """
    R = 6378.0  # Radio de la Tierra en km

    # Convertir grados a radianes
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Diferencias
    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad

    # Fórmula del haversine
    a = math.sin(delta_lat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

def determinar_direccion(lat1, lon1, lat2, lon2):
    """
    Determina la dirección entre dos puntos geográficos según latitud y longitud.
    """
    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    # Direcciones cardinales
    if delta_lat > 0 and delta_lon == 0:
        return "Norte"
    elif delta_lat < 0 and delta_lon == 0:
        return "Sur"
    elif delta_lon > 0 and delta_lat == 0:
        return "Este"
    elif delta_lon < 0 and delta_lat == 0:
        return "Oeste"
    elif delta_lat > 0 and delta_lon > 0:
        return "Noreste"
    elif delta_lat > 0 and delta_lon < 0:
        return "Noroeste"
    elif delta_lat < 0 and delta_lon > 0:
        return "Sureste"
    elif delta_lat < 0 and delta_lon < 0:
        return "Suroeste"
    else:
        return "Sin dirección definida"

# Streamlit App
st.title("Calculadora de Distancia Geográfica")
st.write("Ingrese las coordenadas de dos puntos para calcular la distancia y visualizar la línea en el mapa.")

# Entradas del usuario
lat1 = st.number_input("Latitud del primer punto", value=0.0, format="%.6f")
lon1 = st.number_input("Longitud del primer punto", value=0.0, format="%.6f")
lat2 = st.number_input("Latitud del segundo punto", value=0.0, format="%.6f")
lon2 = st.number_input("Longitud del segundo punto", value=0.0, format="%.6f")

if st.button("Calcular distancia y dirección"):
    # Calcular distancia
    distancia = calcular_distancia(lat1, lon1, lat2, lon2)
    st.success(f"La distancia entre los dos puntos es de {distancia:.2f} km.")

    # Determinar dirección
    direccion = determinar_direccion(lat1, lon1, lat2, lon2)
    st.info(f"La dirección entre los dos puntos es: {direccion}.")

    # Crear la visualización en el mapa
    layer = pdk.Layer(
        "LineLayer",
        data=[
            {"start_lat": lat1, "start_lon": lon1, "end_lat": lat2, "end_lon": lon2}
        ],
        get_source_position="[start_lon, start_lat]",
        get_target_position="[end_lon, end_lat]",
        get_width=5,
        get_color=[255, 0, 0],
        pickable=True,
    )

    # Configuración del mapa
    view_state = pdk.ViewState(
        latitude=(lat1 + lat2) / 2,
        longitude=(lon1 + lon2) / 2,
        zoom=4,
        pitch=0,
    )

    # Mostrar el mapa en Streamlit
    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "Conexión entre los puntos"},
    ))
