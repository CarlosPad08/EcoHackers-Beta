from datetime import datetime, timedelta
from collections import Counter
from statistics import mode
import json

# Ruta del archivo JSON
archivo_json = r"C:\Users\HP\Documents\Hackathon-EcoHackers\backend\pyhton\database\analisis_calidad_aire.json"

# Leer el archivo JSON
with open(archivo_json, 'r') as file:
    data = json.load(file)

# Funcion swich
def switch_demo(argument):
        if argument == "Buena":
            return "No se requieren medidas adicionales"
        elif argument == "Moderada":
            return "Se recomienda reducir levemente actividades al aire libre"
        elif argument == "Dañina para grupos sensibles":
            return "Se recomienda no hacer actividades al aire libre y salir con tapabocas"
        elif argument == "Dañina a la salud":
            return "Se recomienda no estar más de una hora fuera de casa y usar tapabocas"
        elif argument == "Muy dañina a la salud":
            return "Se recomienda no salir de casa y usar tapabocas"
        elif argument == "Peligrosa":
            return "Se recomienda tomar medidas de emergencia y no salir de casa y resguardar entrada de aire a la casa"
        else:
            return "No hay datos suficientes para hacer una recomendación"

# Fecha y hora simulada como "actual"
hora_actual_str = "2024-11-13 07:00:00"
hora_actual = datetime.strptime(hora_actual_str, "%Y-%m-%d %H:%M:%S")

# Hora de inicio (5 horas antes)
hora_inicio = hora_actual - timedelta(hours=5)
hora_inicio_str = hora_inicio.strftime("%Y-%m-%d %H:%M:%S")

# Generar predicción para los próximos 4 días (viernes a lunes)
dias_futuros = ["2024-11-16", "2024-11-17", "2024-11-18", "2024-11-19"]
pronostico_semanal = []

for dia_futuro in dias_futuros:
    # Convertir la fecha futura a objeto datetime
    fecha_futura = datetime.strptime(dia_futuro, "%Y-%m-%d")
    
    # Obtener la fecha correspondiente de la semana pasada
    fecha_historica = fecha_futura - timedelta(weeks=1)
    fecha_historica_str = fecha_historica.strftime("%Y-%m-%d")
    
    # Buscar datos históricos para la fecha correspondiente
    categorias = []
    for entry in data:
        if entry["fecha"] == fecha_historica_str:
            categorias.extend(entry["horas"].values())
            break

    # Calcular la moda si hay datos históricos
    if categorias:
        moda = Counter(categorias).most_common(1)[0][0]
        recomendaciones = switch_demo(moda)
        print(moda)
        print(recomendaciones)

        pronostico_semanal.append({
            "fecha": dia_futuro,
            "categoria_predicha": moda,
            "detalle": f"Pronóstico basado en los datos de {fecha_historica_str}",
            "recomendaciones": f"Recomendaciones para el día: {recomendaciones}",
        })
    else:
        pronostico_semanal.append({
            "fecha": dia_futuro,
            "categoria_predicha": None,
            "detalle": "Sin datos históricos para este día",
        })

# Generar el JSON de salida
json_output = json.dumps(pronostico_semanal, indent=4, ensure_ascii=False)

# Guardar el JSON en una ruta específica
ruta_archivo = r"C:\Users\HP\Documents\Hackathon-EcoHackers\backend\pyhton\database\pronostico_semanal.json"

with open(ruta_archivo, "w", encoding="utf-8") as archivo:
    json.dump(pronostico_semanal, archivo, ensure_ascii=False, indent=4)

print(f"Pronóstico semanal guardado en: {ruta_archivo}")

# Recopilamos las categorías dentro del rango
categorias = []

for entry in data:
    fecha = entry["fecha"]
    for hora, calidad in entry["horas"].items():
        # Crear una cadena datetime completa para comparar
        hora_completa_str = f"{fecha} {hora}:00"
        
        if hora_inicio_str <= hora_completa_str <= hora_actual_str:
            categorias.append(calidad)

# Calcular la moda
if categorias:
    moda = Counter(categorias).most_common(1)[0][0]
    print(f"La moda de las últimas 5 horas es: {moda}")
else:
    print("No hay datos en las últimas 5 horas.")