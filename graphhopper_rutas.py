
"""
Script para calcular distancia, duración y narrativa de viaje entre
ciudades de Chile y Argentina usando API GraphHopper.
Examen Transversal - DRY7122 - Ítem 2
"""

import requests
import urllib.parse
import sys


API_KEY = "1bcad2cd-9b91-4d8b-b54f-59768e4b0e73"


GEOCODE_URL = "https://graphhopper.com/api/1/geocode?"
ROUTE_URL = "https://graphhopper.com/api/1/route?"



def geocodificar(ciudad):
    """
    Función que toma el nombre de una ciudad y devuelve sus coordenadas
    (latitud, longitud) usando la API de Geocodificación de GraphHopper.
    """
    
    params = {"q": ciudad, "limit": "1", "key": API_KEY}
    url = GEOCODE_URL + urllib.parse.urlencode(params)

    try:
        print(f"  Buscando coordenadas para: {ciudad}")
        
        respuesta = requests.get(url)
        datos = respuesta.json()

        
        if respuesta.status_code == 200 and datos.get('hits'):
            
            lat = datos['hits'][0]['point']['lat']
            lng = datos['hits'][0]['point']['lng']
            nombre_completo = datos['hits'][0].get('name', ciudad)
            pais = datos['hits'][0].get('country', '')
            print(f"  ✅ Coordenadas encontradas: {nombre_completo}, {pais} ({lat}, {lng})")
            return True, lat, lng
        else:
            print(f"  ❌ Ciudad no encontrada o error en la API.")
            return False, None, None
    except Exception as e:
        print(f"  ❌ Error al conectar con la API de Geocodificación: {e}")
        return False, None, None

def obtener_ruta(origen_lat, origen_lng, destino_lat, destino_lng, medio_transporte):
    """
    Función que calcula la ruta entre dos puntos usando la API de Routing de GraphHopper.
    """
    # Construir los parámetros para la ruta
    # point=lat,lng para origen y destino
    params = {
        "key": API_KEY,
        "point": [f"{origen_lat},{origen_lng}", f"{destino_lat},{destino_lng}"],
        "vehicle": medio_transporte,
        "locale": "es",  # Para que las instrucciones vengan en español
        "debug": "true"  # Para obtener instrucciones detalladas (narrativa)
    }
    # La URL se construye de forma diferente para múltiples 'point'
    # por lo que usamos requests.get con un diccionario de parámetros
    try:
        print(f"  Calculando ruta en {medio_transporte}...")
        respuesta = requests.get(ROUTE_URL, params=params)
        datos = respuesta.json()

        if respuesta.status_code == 200 and datos.get('paths'):
            # Extraer la primera ruta (la mejor)
            ruta = datos['paths'][0]
            
            # Datos de la ruta
            distancia_metros = ruta['distance']
            tiempo_segundos = ruta['time'] / 1000  # El tiempo viene en milisegundos
            
            # Calcular distancias en kilómetros y millas
            distancia_km = distancia_metros / 1000
            distancia_millas = distancia_km * 0.621371
            
            # Formatear la duración en HH:MM:SS
            horas = int(tiempo_segundos // 3600)
            minutos = int((tiempo_segundos % 3600) // 60)
            segundos = int(tiempo_segundos % 60)
            duracion_str = f"{horas:02d}:{minutos:02d}:{segundos:02d}"
            
            # Obtener la narrativa del viaje (instrucciones paso a paso)
            narrativa = []
            if 'instructions' in ruta:
                for instruccion in ruta['instructions']:
                    # Cada instrucción tiene un texto y la distancia
                    texto = instruccion.get('text', '')
                    distancia_inst = instruccion.get('distance', 0) / 1000  # a km
                    if texto:  # Solo agregar si hay texto
                        narrativa.append(f"  - {texto} ({distancia_inst:.1f} km)")
            else:
                narrativa = ["  Narrativa detallada no disponible."]
            
            return True, distancia_km, distancia_millas, duracion_str, narrativa
        else:
            print("  ❌ Error al calcular la ruta o no se encontró camino.")
            # Mostrar el error si existe
            if 'message' in datos:
                print(f"  Mensaje de error: {datos['message']}")
            return False, None, None, None, None
    except Exception as e:
        print(f"  ❌ Error al conectar con la API de Routing: {e}")
        return False, None, None, None, None

# --- Función Principal del Programa ---

def main():
    print("\n" + "="*60)
    print("    CALCULADOR DE RUTAS CHILE - ARGENTINA")
    print("="*60)
    print("   Usa la API de GraphHopper")
    print("-"*60)

    while True:
        print("\nOpciones de transporte:")
        print("  - car (auto)")
        print("  - bike (bicicleta)")
        print("  - foot (a pie)")
        print("  - s (salir)")

        # 1. Solicitar medio de transporte
        medio = input("\nElige medio de transporte (car/bike/foot): ").strip().lower()
        
        if medio == 's':
            print("¡Hasta luego!")
            break

        if medio not in ['car', 'bike', 'foot']:
            print("❌ Opción no válida. Intenta de nuevo.")
            continue

        # 2. Solicitar ciudad de origen y destino
        ciudad_origen = input("Ciudad de Origen (en español): ").strip()
        if ciudad_origen.lower() == 's':
            print("¡Hasta luego!")
            break

        ciudad_destino = input("Ciudad de Destino (en español): ").strip()
        if ciudad_destino.lower() == 's':
            print("¡Hasta luego!")
            break

        # 3. Geocodificar origen
        print("\n--- Geocodificando Origen ---")
        exito, lat_origen, lng_origen = geocodificar(ciudad_origen)
        if not exito:
            print("No se pudo encontrar la ciudad de origen. Intenta de nuevo.\n")
            continue

        # 4. Geocodificar destino
        print("\n--- Geocodificando Destino ---")
        exito, lat_destino, lng_destino = geocodificar(ciudad_destino)
        if not exito:
            print("No se pudo encontrar la ciudad de destino. Intenta de nuevo.\n")
            continue

        # 5. Calcular la ruta
        print("\n--- Calculando Ruta ---")
        exito, dist_km, dist_millas, duracion, narrativa = obtener_ruta(
            lat_origen, lng_origen, lat_destino, lng_destino, medio
        )

        # 6. Mostrar los resultados
        if exito:
            print("\n" + "="*60)
            print("                 RESULTADOS DEL VIAJE")
            print("="*60)
            print(f"  Origen:         {ciudad_origen}")
            print(f"  Destino:        {ciudad_destino}")
            print(f"  Transporte:     {medio}")
            print("-"*60)
            print(f"  Distancia:      {dist_km:.2f} km ({dist_millas:.2f} millas)")
            print(f"  Duración:       {duracion} (HH:MM:SS)")
            print("-"*60)
            print("  Narrativa del Viaje:")
            if narrativa:
                for paso in narrativa:
                    print(paso)
            else:
                print("  (Narrativa no disponible)")
            print("="*60 + "\n")
        else:
            print("\n❌ No se pudo completar el cálculo de la ruta.\n")

        # Preguntar si quiere salir después de mostrar un resultado
        salir = input("\n¿Deseas salir? (s/n): ").strip().lower()
        if salir == 's':
            print("¡Hasta luego!")
            break
        # Si no, el ciclo continúa

# Ejecutar el programa
if __name__ == "__main__":
    main()
