import streamlit as st
import math

def determinar_direccion(x1, y1, z1, x2, y2, z2):
    """
    Determina la dirección principal entre dos puntos en R3.
    """
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1

    # Determinar la dirección horizontal (x, y)
    if dx == 0 and dy == 0:
        horizontal = "Sin desplazamiento horizontal"
    elif abs(dx) > abs(dy):
        if dx > 0:
            horizontal = "Este"
        else:
            horizontal = "Oeste"
    elif abs(dy) > abs(dx):
        if dy > 0:
            horizontal = "Norte"
        else:
            horizontal = "Sur"
    else:
        if dx > 0 and dy > 0:
            horizontal = "Noreste"
        elif dx > 0 and dy < 0:
            horizontal = "Sureste"
        elif dx < 0 and dy > 0:
            horizontal = "Noroeste"
        elif dx < 0 and dy < 0:
            horizontal = "Suroeste"
    
    # Determinar la dirección vertical (z)
    if dz > 0:
        vertical = "Ascendente"
    elif dz < 0:
        vertical = "Descendente"
    else:
        vertical = "Nivel constante"

    # Combinar resultados
    if horizontal == "Sin desplazamiento horizontal":
        return vertical
    elif vertical == "Nivel constante":
        return horizontal
    else:
        return f"{horizontal} y {vertical}"

# Configuración de la app
st.title("Dirección en R3 entre dos puntos")
st.write("Ingrese las coordenadas de dos puntos para determinar la dirección principal en \( R^3 \).")

# Entrada del usuario
st.subheader("Punto de partida")
x1 = st.number_input("Coordenada X1", value=0.0, format="%.2f")
y1 = st.number_input("Coordenada Y1", value=0.0, format="%.2f")
z1 = st.number_input("Coordenada Z1", value=0.0, format="%.2f")

st.subheader("Punto de llegada")
x2 = st.number_input("Coordenada X2", value=0.0, format="%.2f")
y2 = st.number_input("Coordenada Y2", value=0.0, format="%.2f")
z2 = st.number_input("Coordenada Z2", value=0.0, format="%.2f")

if st.button("Determinar dirección"):
    direccion = determinar_direccion(x1, y1, z1, x2, y2, z2)
    st.success(f"La dirección principal entre los dos puntos es: {direccion}")
