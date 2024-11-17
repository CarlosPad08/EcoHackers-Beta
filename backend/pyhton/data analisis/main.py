from collections import Counter
from statistics import mode
import pandas as pd
import json
import os

# Función para clasificar según el ICA
def clasificar_ica(pm2_5, pm10):
    if pm2_5 <= 12 and pm10 <= 54:
        return "Buena"
    elif pm2_5 <= 37 and pm10 <= 154:
        return "Moderada"
    elif pm2_5 <= 55 and pm10 <= 254:
        return "Dañina para grupos sensibles"
    elif pm2_5 <= 150 and pm10 <= 354:
        return "Dañina a la salud"
    elif pm2_5 <= 250 and pm10 <= 424:
        return "Muy dañina a la salud"
    else:
        return "Peligrosa"

# Leer el archivo Excel
archivo = r"C:\Users\HP\Documents\Hackathon-EcoHackers\backend\pyhton\database\NOV_ECOHACKERS.xlsx"
df = pd.read_excel(archivo)

print(df[['fecha', 'hora_entera']].head())

# Convertir las fechas a formato string para JSON
df['fecha'] = pd.to_datetime(df['fecha']).dt.strftime('%Y-%m-%d')  # Convertir fecha a string (YYYY-MM-DD)

# Crear una lista única de fechas
fechas = df['fecha'].unique()

# Generar un JSON con el análisis
resultado = []

for fecha in fechas:
    pronostico = "Pronóstico de calidad del aire para el día"
    recomendaciones = "Recomendaciones para el día"
    datos_dia = {'fecha': fecha, 'horas': {}, 'pronostico': pronostico, 'recomendaciones': recomendaciones}
    for hora_entera in range(24):
        # Filtrar datos por fecha y hora
        datos_hora = df[(df['fecha'] == fecha) & (df['hora_entera'] == hora_entera)]
        if not datos_hora.empty:
            pm2_5_avg = datos_hora['massPM2_5Avg'].mean()
            pm10_avg = datos_hora['massPM10_0Avg'].mean()
            categoria = clasificar_ica(pm2_5_avg, pm10_avg)
            datos_dia['horas'][f'{hora_entera:02d}:00'] = categoria
            datos_dia['pronostico'] = "Pronóstico de calidad del aire para el día: " + categoria
        else:
            datos_dia['horas'][f'{hora_entera:02d}:00'] = "Sin datos"

    resultado.append(datos_dia)

ruta_destino = r"C:\Users\HP\Documents\Hackathon-EcoHackers\backend\pyhton\database\analisis_calidad_aire.json"

carpeta_destino = os.path.dirname(ruta_destino)
if not os.path.exists(carpeta_destino):
    os.makedirs(carpeta_destino)

# Guardar en un archivo JSON
with open(ruta_destino, "w", encoding="utf-8") as json_file:
    json.dump(resultado, json_file, indent=4, ensure_ascii=False)

print("Archivo JSON generado: analisis_calidad_aire.json")