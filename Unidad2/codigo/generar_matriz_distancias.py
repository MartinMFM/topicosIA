import pandas as pd
import numpy as np
from math import radians, cos, sin, asin, sqrt


def haversine(lat1, lon1, lat2, lon2):
    # Convertir grados a radianes
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    
    # Formula de Haversine
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    
    # Radio de la Tierra en kilometros
    r = 6371
    
    return c * r


def generar_matriz_distancias(archivo_entrada='datos_distribucion_tiendas.xlsx',
                              archivo_salida='matriz_distancias.xlsx'):
    
    print("GENERADOR DE MATRIZ DE DISTANCIAS - FORMULA DE HAVERSINE")
    
    # Cargar datos de ubicaciones
    try:
        df_ubicaciones = pd.read_excel(archivo_entrada)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{archivo_entrada}'")
        return False
    except Exception as e:
        print(f"Error al cargar datos: {e}")
        return False
    
    # Verificar columnas necesarias
    columnas_necesarias = ['Latitud_WGS84', 'Longitud_WGS84']
    if not all(col in df_ubicaciones.columns for col in columnas_necesarias):
        print(f"Error: El archivo debe contener las columnas {columnas_necesarias}")
        return False
    
    # Extraer coordenadas
    latitudes = df_ubicaciones['Latitud_WGS84'].values
    longitudes = df_ubicaciones['Longitud_WGS84'].values
    n_ubicaciones = len(latitudes)
    
    # Calcular matriz de distancias
    matriz_distancias = np.zeros((n_ubicaciones, n_ubicaciones))
    
    for i in range(n_ubicaciones):
        for j in range(n_ubicaciones):
            if i == j:
                matriz_distancias[i, j] = 0.0
            else:
                distancia = haversine(
                    latitudes[i], longitudes[i],
                    latitudes[j], longitudes[j]
                )
                matriz_distancias[i, j] = distancia
    
    # Crear DataFrame con el formato correcto (Nodo_1, Nodo_2, ...)
    columnas = [f'Nodo_{i+1}' for i in range(n_ubicaciones)]
    df_matriz = pd.DataFrame(matriz_distancias, columns=columnas)
    
    # Guardar en Excel
    try:
        df_matriz.to_excel(archivo_salida, index=False)
    except Exception as e:
        print(f"Error al guardar archivo: {e}")
        return False
    
    print(f"Terminado: {archivo_salida} ({n_ubicaciones}x{n_ubicaciones})")
    
    return True


def main():
    """Funcion principal del script"""
    generar_matriz_distancias(
        archivo_entrada='datos_distribucion_tiendas.xlsx',
        archivo_salida='matriz_distancias.xlsx'
    )


if __name__ == "__main__":
    main()
