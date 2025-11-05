"""
Módulo para generación de reportes
"""
import numpy as np
from datetime import datetime
from utils import calcular_distancia


class GeneradorReportes:
    """Generador de reportes de optimización"""
    
    @staticmethod
    def inicializar_archivo(archivo, n_sensores, n_particulas, n_iteraciones, datos_campo):
        """
        Inicializar archivo de progreso con encabezados
        
        Args:
            archivo (str): Nombre del archivo donde guardar el progreso
            n_sensores (int): Número de sensores
            n_particulas (int): Número de partículas
            n_iteraciones (int): Número de iteraciones
            datos_campo (pd.DataFrame): Datos del campo
        """
        with open(archivo, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("PROGRESO DE OPTIMIZACION PSO - SENSORES AGRICOLAS\n")
            f.write("=" * 80 + "\n")
            f.write(f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Region: Guasave, Sinaloa\n")
            f.write(f"Sensores a ubicar: {n_sensores}\n")
            f.write(f"Particulas: {n_particulas}\n")
            f.write(f"Iteraciones max: {n_iteraciones}\n")
            f.write(f"Parcelas del campo: {len(datos_campo)}\n")
            f.write("=" * 80 + "\n\n")
            f.write("PROGRESO DE OPTIMIZACION:\n")
            f.write("-" * 50 + "\n")
    
    @staticmethod
    def guardar_progreso(archivo, iteracion, mejor_valor, mejor_posicion, n_sensores, historial):
        """
        Guardar progreso actual
        
        Args:
            archivo (str): Nombre del archivo
            iteracion (int): Número de iteración actual
            mejor_valor (float): Mejor valor actual
            mejor_posicion (np.ndarray): Mejor posición actual
            n_sensores (int): Número de sensores
            historial (list): Historial de convergencia
        """
        with open(archivo, 'a', encoding='utf-8') as f:
            f.write(f"Iteracion {iteracion:3d}: Mejor costo = {mejor_valor:.4f}\n")
            
            # Cada 50 iteraciones, mostrar más detalles
            if iteracion % 50 == 0:
                sensores = mejor_posicion.reshape(n_sensores, 2)
                f.write(f"  Posiciones actuales de sensores:\n")
                for i, (lat, lon) in enumerate(sensores):
                    f.write(f"    Sensor {i+1}: Lat={lat:.6f}, Lon={lon:.6f}\n")
                f.write(f"  Mejora desde inicio: {historial[0] - mejor_valor:.4f}\n")
                f.write("-" * 30 + "\n")
    
    @staticmethod
    def guardar_resultado_final(archivo, mejor_valor, mejor_posicion, n_sensores, 
                                historial, datos_campo):
        """
        Guardar resultado final de la optimización
        
        Args:
            archivo (str): Nombre del archivo
            mejor_valor (float): Mejor valor final
            mejor_posicion (np.ndarray): Mejor posición final
            n_sensores (int): Número de sensores
            historial (list): Historial de convergencia
            datos_campo (pd.DataFrame): Datos del campo
        """
        sensores = mejor_posicion.reshape(n_sensores, 2)
        
        with open(archivo, 'a', encoding='utf-8') as f:
            f.write("\n" + "=" * 80 + "\n")
            f.write("RESULTADO FINAL DE OPTIMIZACION\n")
            f.write("=" * 80 + "\n")
            f.write(f"Costo final: {mejor_valor:.4f}\n")
            f.write(f"Mejora total: {historial[0] - mejor_valor:.4f}\n")
            f.write(f"Porcentaje de mejora: {((historial[0] - mejor_valor) / historial[0] * 100):.2f}%\n")
            f.write("\nUBICACIONES OPTIMAS DE SENSORES:\n")
            f.write("-" * 40 + "\n")
            
            for i, (lat, lon) in enumerate(sensores):
                f.write(f"Sensor {i+1}: Latitud={lat:.6f}, Longitud={lon:.6f}\n")
            
            # Calcular estadísticas de cobertura
            distancias = []
            for _, parcela in datos_campo.iterrows():
                dist_min = float('inf')
                for lat_s, lon_s in sensores:
                    dist = calcular_distancia(parcela['Latitud'], parcela['Longitud'], lat_s, lon_s)
                    dist_min = min(dist_min, dist)
                distancias.append(dist_min)
            
            f.write(f"\nESTADISTICAS DE COBERTURA:\n")
            f.write("-" * 30 + "\n")
            f.write(f"Distancia promedio a sensores: {np.mean(distancias):.4f} km\n")
            f.write(f"Distancia maxima: {np.max(distancias):.4f} km\n")
            f.write(f"Distancia minima: {np.min(distancias):.4f} km\n")
            f.write(f"Desviacion estandar: {np.std(distancias):.4f} km\n")
            
            f.write(f"\nHISTORIAL DE CONVERGENCIA:\n")
            f.write("-" * 30 + "\n")
            for i, valor in enumerate(historial[::10]):  # Cada 10 valores
                f.write(f"Iter {i*10:3d}: {valor:.4f}\n")
            
            f.write("\n" + "=" * 80 + "\n")
            f.write("FIN DEL REPORTE DE OPTIMIZACION\n")
            f.write("=" * 80 + "\n")
