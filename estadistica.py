import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

# Datos proporcionados
distancia = 1557.6902  # km
hora_salida = datetime(2025, 1, 11, 23, 2)
duracion_estimada = timedelta(days=2, hours=0)  # Duración estimada de 2 días

# Clima en Guayaquil
clima_guayaquil = {
    "descripcion": "broken clouds",
    "temperatura": 27.03,  # en °C
    "viento": 6.17,  # m/s
    "direccion_viento": 230  # grados
}

# Clima en Panama Canal
clima_panama = {
    "descripcion": "overcast clouds",
    "temperatura": 25.92,  # en °C
    "viento": 0.81,  # m/s
    "direccion_viento": 313  # grados
}

# Coordenadas aproximadas para las ciudades
coords_guayaquil = (-2.1896, -79.8891)  # Latitud, Longitud
coords_panama = (8.9824, -79.5199)      # Latitud, Longitud

# Cálculo de la llegada estimada
hora_llegada = hora_salida + duracion_estimada

# Creación del gráfico catastrófico
fig, ax = plt.subplots(figsize=(10, 6))

# Datos del gráfico
categorias = ['Temperatura (°C)', 'Viento (m/s)', 'Dirección del Viento (°)']
valores_guayaquil = [clima_guayaquil['temperatura'], clima_guayaquil['viento'], clima_guayaquil['direccion_viento']]
valores_panama = [clima_panama['temperatura'], clima_panama['viento'], clima_panama['direccion_viento']]

x = np.arange(len(categorias))
width = 0.35

# Barras
barras_guayaquil = ax.bar(x - width/2, valores_guayaquil, width, label='Guayaquil', color='royalblue')
barras_panama = ax.bar(x + width/2, valores_panama, width, label='Panama Canal', color='darkorange')

# Etiquetas y diseño
ax.set_xlabel('Categorías')
ax.set_title('Gráfico Catastrófico: Comparación de Variables Climáticas')
ax.set_xticks(x)
ax.set_xticklabels(categorias)
ax.legend()

# Añadir etiquetas a las barras
def agregar_etiquetas(barras):
    for barra in barras:
        altura = barra.get_height()
        ax.annotate(f'{altura:.2f}',
                    xy=(barra.get_x() + barra.get_width() / 2, altura),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom')

agregar_etiquetas(barras_guayaquil)
agregar_etiquetas(barras_panama)

# Mostrar el gráfico
plt.tight_layout()
plt.show()

# Imprimir los resultados clave
print(f"Distancia: {distancia:.4f} km")
print("\nResultado:")
print(f"Hora de salida: {hora_salida.strftime('%d de %B de %Y %H:%M')}")
print(f"Duración estimada: {duracion_estimada.days} días {duracion_estimada.seconds//3600} horas")
print(f"Llegada estimada: {hora_llegada.strftime('%d de %B de %Y %H:%M')}")
print(f"Clima en Guayaquil: {clima_guayaquil['descripcion']}, {clima_guayaquil['temperatura']}°C, Viento: {clima_guayaquil['viento']} m/s, Dirección: {clima_guayaquil['direccion_viento']}°")
print(f"Clima en Panama Canal: {clima_panama['descripcion']}, {clima_panama['temperatura']}°C, Viento: {clima_panama['viento']} m/s, Dirección: {clima_panama['direccion_viento']}°")
