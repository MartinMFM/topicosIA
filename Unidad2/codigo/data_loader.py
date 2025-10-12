import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist
from config import (
    ARCHIVO_DATOS_TIENDAS,
    ARCHIVO_MATRIZ_DISTANCIAS, 
    ARCHIVO_MATRIZ_COMBUSTIBLE,
    TIPO_CENTRO_DISTRIBUCION,
    TIPO_TIENDA,
    COLUMNAS_ESPERADAS
)

class DataLoader:
    
    def __init__(self):
        self.datos_df = None
        self.centros_distribucion = None
        self.tiendas = None
        self.costo_total_matrix = None
    
    def cargar_datos_ubicaciones(self):
        try:
            self.datos_df = pd.read_excel(ARCHIVO_DATOS_TIENDAS)
            print(f"Datos de ubicaciones cargados: {len(self.datos_df)} ubicaciones")
            return True
        except FileNotFoundError:
            print(f"Error: No se encontró '{ARCHIVO_DATOS_TIENDAS}'")
            return False
    
    def cargar_matrices_costos(self):
        try:
            distancias_df = pd.read_excel(ARCHIVO_MATRIZ_DISTANCIAS)
            costos_combustible_df = pd.read_excel(ARCHIVO_MATRIZ_COMBUSTIBLE)
            
            # Combinar matrices de costo
            costo_total_df = distancias_df + costos_combustible_df
            self.costo_total_matrix = costo_total_df.to_numpy()
            
            print("Matrices de costos cargadas y combinadas")
            return True
        except FileNotFoundError:
            print("Error: No se encontraron las matrices de costos")
            return False
    
    def separar_ubicaciones(self):
        if self.datos_df is None:
            print("Error: Datos no cargados")
            return False
        
        self.centros_distribucion = self.datos_df[
            self.datos_df[COLUMNAS_ESPERADAS['tipo']] == TIPO_CENTRO_DISTRIBUCION
        ].copy()
        
        self.tiendas = self.datos_df[
            self.datos_df[COLUMNAS_ESPERADAS['tipo']] == TIPO_TIENDA
        ].copy()
        
        print(f"{len(self.centros_distribucion)} centros de distribución")
        print(f"{len(self.tiendas)} tiendas identificadas")
        return True
    
    def asignar_tiendas_a_zonas(self):
        if self.centros_distribucion is None or self.tiendas is None:
            print("Error: Ubicaciones no separadas")
            return False
        
        # Obtener coordenadas
        coordenadas_centros = self.centros_distribucion[
            [COLUMNAS_ESPERADAS['latitud'], COLUMNAS_ESPERADAS['longitud']]
        ].values
        
        coordenadas_tiendas = self.tiendas[
            [COLUMNAS_ESPERADAS['latitud'], COLUMNAS_ESPERADAS['longitud']]
        ].values
        
        # Calcular distancias y asignar a zona más cercana
        distancias = cdist(coordenadas_tiendas, coordenadas_centros, metric='euclidean')
        asignaciones_zona = np.argmin(distancias, axis=1)
        self.tiendas['zona'] = asignaciones_zona
        
        print("Tiendas asignadas a zonas por proximidad")
        return True
    
    def cargar_todos_los_datos(self):
        print("=== CARGANDO Y PREPARANDO DATOS ===")
        
        # Cargar datos básicos
        if not self.cargar_datos_ubicaciones():
            return False
        
        if not self.cargar_matrices_costos():
            return False
        
        # Preparar datos
        if not self.separar_ubicaciones():
            return False
        
        if not self.asignar_tiendas_a_zonas():
            return False
        
        print("Todos los datos cargados y preparados correctamente")
        return True
    
    def obtener_tiendas_por_zona(self, zona_id):
        if self.tiendas is None:
            return pd.DataFrame()
        return self.tiendas[self.tiendas['zona'] == zona_id]
    
    def obtener_centro_por_zona(self, zona_id):
        if self.centros_distribucion is None:
            return None
        return self.centros_distribucion.iloc[zona_id]