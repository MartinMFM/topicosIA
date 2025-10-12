from route_optimizer import RouteOptimizer
from utils import ResultadosManager, ValidadorDatos
from config import (
    ARCHIVO_DATOS_TIENDAS,
    ARCHIVO_MATRIZ_DISTANCIAS,
    ARCHIVO_MATRIZ_COMBUSTIBLE,
    COLUMNAS_ESPERADAS
)

def main():
    print("=== SISTEMA DE OPTIMIZACIÓN DE RUTAS POR ZONAS ===")
    
    # Validar que todos los archivos necesarios existan
    archivos_necesarios = [
        ARCHIVO_DATOS_TIENDAS,
        ARCHIVO_MATRIZ_DISTANCIAS,
        ARCHIVO_MATRIZ_COMBUSTIBLE
    ]
    
    if not ValidadorDatos.validar_archivos_existen(archivos_necesarios):
        print("No se pueden continuar sin los archivos necesarios")
        return
    
    # Crear optimizador y cargar datos
    optimizador = RouteOptimizer()
    
    print("Cargando datos...")
    if not optimizador.cargar_datos():
        print("Error al cargar los datos")
        return
    
    # Validar completitud de datos
    columnas_requeridas = list(COLUMNAS_ESPERADAS.values())
    if not ValidadorDatos.validar_datos_completitud(
        optimizador.data_loader.datos_df, 
        columnas_requeridas
    ):
        print("Los datos no tienen la estructura esperada")
        return
    
    # Ejecutar optimización
    try:
        print("\nIniciando proceso de optimización...")
        resultados, costo_total = optimizador.optimizar_rutas_por_zonas()
        
        if not resultados:
            print("No se obtuvieron resultados de la optimización")
            return
        
        # Mostrar resultados en consola
        ResultadosManager.mostrar_resultados_consola(
            resultados, 
            costo_total, 
            optimizador.data_loader.datos_df
        )
        
        # Mostrar resumen estadístico
        resumen = optimizador.obtener_resumen_resultados()
        ResultadosManager.mostrar_resumen_estadisticas(resumen)
        
        # Guardar resultados en archivo
        ResultadosManager.guardar_resultados_archivo(
            resultados, 
            costo_total, 
            optimizador.data_loader.datos_df
        )
        print("\nProceso de optimización completado exitosamente")
        
    except Exception as e:
        print(f"Error durante la optimización: {e}")
        raise

if __name__ == "__main__":
    main()