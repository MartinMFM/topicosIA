"""
Función objetivo para la optimización
"""
from utils import calcular_distancia, obtener_peso_cultivo


def funcion_objetivo_sensores(posiciones_sensores, datos_campo, n_sensores=5):
    """
    Función objetivo para optimizar ubicación de sensores
    
    Args:
        posiciones_sensores: Array [lat1, lon1, lat2, lon2, ...] posiciones de sensores
        datos_campo: DataFrame con datos del campo
        n_sensores: Número de sensores a ubicar
    
    Returns:
        float: Costo total a minimizar (menor cobertura = mayor costo)
    """
    # Reshape posiciones de sensores
    sensores = posiciones_sensores.reshape(n_sensores, 2)
    
    costo_total = 0
    
    # Para cada parcela, calcular la cobertura de sensores
    for _, parcela in datos_campo.iterrows():
        lat_parcela = parcela['Latitud']
        lon_parcela = parcela['Longitud']
        cultivo = parcela['Cultivo']
        humedad = parcela['Humedad (%)']
        elevacion = parcela['Elevación (m)']
        
        # Calcular distancia a cada sensor
        distancias = []
        for sensor_lat, sensor_lon in sensores:
            distancia = calcular_distancia(lat_parcela, lon_parcela, sensor_lat, sensor_lon)
            distancias.append(distancia)
        
        # Distancia al sensor más cercano
        dist_min = min(distancias)
        
        # Factor de cobertura (mejor cobertura = menor costo)
        # Sensores deben estar cerca para monitoreo efectivo
        max_distancia_efectiva = 0.01  # ~1km en grados
        factor_cobertura = min(1.0, dist_min / max_distancia_efectiva)
        
        # Peso por importancia del cultivo
        peso_cultivo = obtener_peso_cultivo(cultivo)
        
        # Peso por variabilidad de humedad (más variable = más sensores necesarios)
        peso_humedad = 1 + abs(humedad - 25) / 25  # Normalizado a humedad media
        
        # Peso por elevación (variaciones topográficas requieren más monitoreo)
        peso_elevacion = 1 + abs(elevacion - 30) / 20  # Normalizado a elevación media
        
        # Costo de esta parcela (penaliza poca cobertura)
        costo_parcela = factor_cobertura * peso_cultivo * peso_humedad * peso_elevacion
        costo_total += costo_parcela
    
    # Penalización por sensores muy cercanos entre sí (redundancia)
    penalizacion_redundancia = 0
    for i in range(n_sensores):
        for j in range(i + 1, n_sensores):
            dist_sensores = calcular_distancia(sensores[i, 0], sensores[i, 1], 
                                             sensores[j, 0], sensores[j, 1])
            if dist_sensores < 0.005:  # Muy cercanos
                penalizacion_redundancia += 50
    
    return costo_total + penalizacion_redundancia
