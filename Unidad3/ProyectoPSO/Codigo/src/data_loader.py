"""
Módulo para carga y gestión de datos de cultivos
"""
import numpy as np
import pandas as pd


def cargar_datos_cultivos():
    """
    Cargar datos de cultivos de la región de Guasave, Sinaloa
    
    Intenta cargar el archivo CSV con datos reales de campo. Si no se encuentra,
    genera datos simulados basados en las características de la región.
    
    Returns:
        pd.DataFrame: DataFrame con columnas:
            - Cultivo: Tipo de cultivo (Maíz, Chile, Tomate)
            - Latitud: Coordenada latitudinal 
            - Longitud: Coordenada longitudinal
            - Temperatura (°C): Temperatura ambiente
            - Humedad (%): Porcentaje de humedad del suelo
            - Salinidad (dS/m): Nivel de salinidad del suelo
            - Elevación (m): Altura sobre el nivel del mar
    """
    try:
        datos = pd.read_csv('../data/datos_cultivos_guasave.csv')
        print(f"Datos cargados: {len(datos)} parcelas en Guasave")
        print(f"Cultivos: {datos['Cultivo'].unique()}")
        return datos
    except:
        print("Error cargando datos. Usando datos simulados...")
        return _generar_datos_simulados()


def _generar_datos_simulados():
    """
    Genera datos simulados de Guasave
    
    Returns:
        pd.DataFrame: DataFrame con datos simulados
    """
    np.random.seed(42)
    n_parcelas = 100
    cultivos = np.random.choice(['Maíz', 'Chile', 'Tomate'], n_parcelas)
    
    # Coordenadas reales de Guasave, Sinaloa
    lat_base, lon_base = 25.56, -108.47
    datos = pd.DataFrame({
        'Cultivo': cultivos,
        'Latitud': np.random.uniform(lat_base - 0.05, lat_base + 0.05, n_parcelas),
        'Longitud': np.random.uniform(lon_base - 0.05, lon_base + 0.05, n_parcelas),
        'Temperatura (°C)': np.random.uniform(20, 40, n_parcelas),
        'Humedad (%)': np.random.uniform(5, 45, n_parcelas),
        'Salinidad (dS/m)': np.random.uniform(0.5, 4.0, n_parcelas),
        'Elevación (m)': np.random.uniform(10, 50, n_parcelas)
    })
    return datos
