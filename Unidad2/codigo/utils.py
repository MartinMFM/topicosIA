import os
from config import ARCHIVO_RESULTADOS, ENCODING_ARCHIVO

class ResultadosManager:
    
    @staticmethod
    def mostrar_resultados_consola(resultados_zonas, costo_total, datos_df):
        print("\n" + "="*70)
        print("RESULTADOS FINALES DE OPTIMIZACIÓN")
        print("="*70)
        
        for zona_id, resultado in resultados_zonas.items():
            print(f"\n{resultado['centro']}")
            print(f"   Tiendas: {resultado['tiendas_count']}")
            print(f"   Costo optimizado: {resultado['costo']:.2f}")
            print(f"   Capacidad total de zona: {resultado['capacidad_total']:,}")
            
            # Mostrar ruta con nombres
            ruta_nombres = [datos_df.iloc[nodo]['Nombre'] for nodo in resultado['ruta']]
            ruta_str = ' - '.join(ruta_nombres)
            print(f"   Ruta: {ruta_str}")
        
        print(f"\n COSTO TOTAL OPTIMIZADO: {costo_total:.2f}")
        print(f" Rutas optimizadas para {len(resultados_zonas)} zonas")
    
    @staticmethod
    def guardar_resultados_archivo(resultados_zonas, costo_total, datos_df, archivo=None):
        archivo = archivo or ARCHIVO_RESULTADOS
        
        try:
            with open(archivo, 'w', encoding=ENCODING_ARCHIVO) as f:
                f.write("RESULTADOS DE OPTIMIZACIÓN DE RUTAS POR ZONAS\n")
                f.write("="*50 + "\n\n")
                
                for zona_id, resultado in resultados_zonas.items():
                    f.write(f"ZONA: {resultado['centro']}\n")
                    f.write(f"Tiendas: {resultado['tiendas_count']}\n")
                    f.write(f"Costo: {resultado['costo']:.2f}\n")
                    f.write(f"Capacidad: {resultado['capacidad_total']:,}\n")
                    
                    # Escribir ruta con nombres
                    ruta_nombres = [datos_df.iloc[nodo]['Nombre'] for nodo in resultado['ruta']]
                    ruta_str = ' → '.join(ruta_nombres)
                    f.write(f"Ruta: {ruta_str}\n")
                    f.write("-" * 50 + "\n")
                
                f.write(f"\nCOSTO TOTAL: {costo_total:.2f}\n")
            
            print(f"\n Resultados guardados en: '{archivo}'")
            return archivo
            
        except Exception as e:
            print(f" Error al guardar resultados: {e}")
            return None
    
    @staticmethod
    def mostrar_resumen_estadisticas(resumen):
        if not resumen:
            print(" No hay resultados para mostrar")
            return
        
        print("\n RESUMEN ESTADÍSTICO")
        print("-" * 30)
        print(f"Zonas totales: {resumen['zonas_totales']}")
        print(f"Zonas activas: {resumen['zonas_activas']}")
        print(f"Total de tiendas: {resumen['total_tiendas']}")
        print(f"Capacidad total: {resumen['total_capacidad']:,}")
        print(f"Costo total: {resumen['costo_total']:.2f}")
        print(f"Costo promedio por zona: {resumen['costo_promedio_por_zona']:.2f}")


class ValidadorDatos:
    @staticmethod
    def validar_archivos_existen(archivos):
        archivos_faltantes = []
        for archivo in archivos:
            if not os.path.exists(archivo):
                archivos_faltantes.append(archivo)
        
        if archivos_faltantes:
            print("❌ Archivos faltantes:")
            for archivo in archivos_faltantes:
                print(f"   - {archivo}")
            return False
        
        return True
    
    @staticmethod
    def validar_datos_completitud(datos_df, columnas_requeridas):
        columnas_faltantes = []
        for columna in columnas_requeridas:
            if columna not in datos_df.columns:
                columnas_faltantes.append(columna)
        
        if columnas_faltantes:
            print(" Columnas faltantes en los datos:")
            for columna in columnas_faltantes:
                print(f"   - {columna}")
            return False
        
        return True