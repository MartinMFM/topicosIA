"""
Utilidades y funciones auxiliares
"""
import numpy as np


def calcular_distancia(lat1, lon1, lat2, lon2):
    """
    Calcular distancia euclidiana entre dos puntos geográficos
    
    Utiliza la fórmula de distancia euclidiana para calcular la separación
    entre dos coordenadas geográficas. Apropiado para distancias cortas.
    
    Args:
        lat1 (float): Latitud del primer punto
        lon1 (float): Longitud del primer punto  
        lat2 (float): Latitud del segundo punto
        lon2 (float): Longitud del segundo punto
        
    Returns:
        float: Distancia euclidiana entre los dos puntos en grados
        
    Note:
        Para convertir a kilómetros, multiplicar por ~111 km/grado
    """
    return np.sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2)


def obtener_peso_cultivo(cultivo):
    """
    Obtener peso de importancia económica por tipo de cultivo
    
    Asigna pesos basados en la importancia económica de cada cultivo
    en la región de Guasave, Sinaloa según datos de producción estatal.
    
    Args:
        cultivo (str): Tipo de cultivo ('Maíz', 'Chile', 'Tomate')
        
    Returns:
        float: Peso de importancia del cultivo
            - Maíz: 2.17 (21.7% de producción estatal)
            - Chile: 1.5 (producción significativa)
            - Tomate: 0.99 (9.9% de producción estatal)
            - Otros: 1.0 (peso neutro por defecto)
            
    Note:
        Mayor peso indica mayor prioridad para ubicación de sensores
    """
    pesos = {
        'Maíz': 2.17,     # 21.7% de producción estatal
        'Tomate': 0.99,   # 9.9% de producción estatal  
        'Chile': 1.5      # Producción significativa
    }
    return pesos.get(cultivo, 1.0)
