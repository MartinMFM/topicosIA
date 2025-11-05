"""
Programa principal para optimización de sensores agrícolas
"""
from data_loader import cargar_datos_cultivos
from pso import PSOSensores


def main():
    """
    Función principal del programa de optimización de sensores agrícolas
    
    Orquesta la ejecución completa del sistema: carga de datos, configuración
    del algoritmo PSO, ejecución de la optimización y visualización de resultados.
    
    Returns:
        dict: Resultados de la optimización con coordenadas óptimas de sensores
        
    Workflow:
        1. Cargar datos de cultivos de Guasave desde CSV o generar simulados
        2. Inicializar optimizador PSO con parámetros por defecto
        3. Ejecutar optimización con 5 sensores, 30 partículas, 100 iteraciones
        4. Mostrar gráficas de convergencia y mapa de ubicación óptima
        
    Note:
        Esta función implementa el caso de uso principal del sistema para
        optimización de ubicación de sensores en agricultura de precisión.
    """
    print(" OPTIMIZACIÓN DE SENSORES AGRÍCOLAS EN GUASAVE, SINALOA")
    print("Objetivo: Maximizar eficiencia del riego mediante ubicación óptima de sensores\n")
    
    # Cargar datos
    datos = cargar_datos_cultivos()
    
    # Ejecutar optimización PSO
    pso = PSOSensores(datos, n_sensores=5, n_particulas=30, n_iteraciones=100)
    resultado = pso.optimizar(guardar_progreso=True, archivo_progreso="resultados_optimizacion.txt")
    
    # Mostrar gráficas
    pso.graficar_resultados()
    
    return resultado


if __name__ == "__main__":
    resultado = main()
