import streamlit as st
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Radio de la Tierra en km
R = 6378

# Función para convertir latitud y longitud en coordenadas cilíndricas
def convertir_a_cilindricas(lat, lon):
    # Convertir grados a radianes
    lat_rad = np.radians(lat)
    lon_rad = np.radians(lon)

    # Coordenadas cilíndricas
    r = R * np.cos(lat_rad)  # Distancia radial
    z = R * np.sin(lat_rad)  # Altura (latitud proyectada)
    theta = lon_rad          # Longitud como ángulo

    # Coordenadas cartesianas X, Y, Z
    x = r * np.cos(theta)
    y = r * np.sin(theta)

    return x, y, z

# Interfaz de usuario con Streamlit
st.title("Conversión de coordenadas geográficas a esfericas 3D")
st.write("Ingrese las coordenadas de latitud y longitud para convertirlas en coordenadas cilíndricas y graficarlas en 3D.")

# Entrada de las coordenadas geográficas
st.subheader("Coordenadas del Punto A")
lat1 = st.number_input("Latitud A (en grados)", value=-2.27)
lon1 = st.number_input("Longitud A (en grados)", value=-79.90)

st.subheader("Coordenadas del Punto B")
lat2 = st.number_input("Latitud B (en grados)", value=9.1205)
lon2 = st.number_input("Longitud B (en grados)", value=-79.7517)

st.subheader("Coordenadas del Punto C")
lat3 = st.number_input("Latitud C (en grados)", value=10.0)
lon3 = st.number_input("Longitud C (en grados)", value=-75.0)

# Convertir las coordenadas a cilíndricas (X, Y, Z)
x1, y1, z1 = convertir_a_cilindricas(lat1, lon1)
x2, y2, z2 = convertir_a_cilindricas(lat2, lon2)
x3, y3, z3 = convertir_a_cilindricas(lat3, lon3)

# Mostrar resultados dentro de Streamlit
st.subheader("Resultados de las coordenadas esfericas")
st.write(f"**Punto A (Latitud: {lat1}°, Longitud: {lon1}°):**")
st.write(f"Coordenadas esfericas: (X: {x1:.2f} km, Y: {y1:.2f} km, Z: {z1:.2f} km)")

st.write(f"**Punto B (Latitud: {lat2}°, Longitud: {lon2}°):**")
st.write(f"Coordenadas esfericas: (X: {x2:.2f} km, Y: {y2:.2f} km, Z: {z2:.2f} km)")

st.write(f"**Punto C (Latitud: {lat3}°, Longitud: {lon3}°):**")
st.write(f"Coordenadas esfericas: (X: {x3:.2f} km, Y: {y3:.2f} km, Z: {z3:.2f} km)")

# Graficar los puntos en 3D
def graficar_puntos(x1, y1, z1, x2, y2, z2, x3, y3, z3):
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    # Graficar los puntos A, B y C
    ax.scatter(x1, y1, z1, color='r', label="Punto A", s=100)
    ax.scatter(x2, y2, z2, color='b', label="Punto B", s=100)
    ax.scatter(x3, y3, z3, color='g', label="Punto C", s=100)

    # Graficar líneas entre los puntos
    ax.plot([x1, x2], [y1, y2], [z1, z2], color='purple', linestyle='--', label="Línea A-B")
    ax.plot([x2, x3], [y2, y3], [z2, z3], color='orange', linestyle='--', label="Línea B-C")
    ax.plot([x3, x1], [y3, y1], [z3, z1], color='gray', linestyle='--', label="Línea C-A")

    # Etiquetas y título
    ax.set_xlabel('X (Coordenada cilíndrica)')
    ax.set_ylabel('Y (Coordenada cilíndrica)')
    ax.set_zlabel('Z (Altura)')
    ax.set_title('Gráfico 3D de los puntos A, B y C en coordenadas cilíndricas')

    # Mostrar la leyenda
    ax.legend()

    # Mostrar el gráfico
    st.pyplot(fig)

# Graficar los puntos al presionar el botón
if st.button("Graficar puntos"):
    graficar_puntos(x1, y1, z1, x2, y2, z2, x3, y3, z3)
