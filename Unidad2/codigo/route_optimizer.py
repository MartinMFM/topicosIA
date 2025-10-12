from data_loader import DataLoader
from simulated_annealing import SimulatedAnnealing
from config import (
    TEMPERATURA_INICIAL,
    TASA_ENFRIAMIENTO,
    TEMP_FINAL,
    L_ITERACIONES,
    MOSTRAR_PROGRESO
)

class RouteOptimizer:
    def __init__(self):
        self.data_loader = DataLoader()
        self.resultados_zonas = {}
        self.costo_total_optimizado = 0
    
    def cargar_datos(self):
        return self.data_loader.cargar_todos_los_datos()
    
    def optimizar_rutas_por_zonas(self, temp_inicial=None, tasa_enfriamiento=None):

        # Usar valores por defecto si no se especifican
        temp_inicial = temp_inicial or TEMPERATURA_INICIAL
        tasa_enfriamiento = tasa_enfriamiento or TASA_ENFRIAMIENTO
        
        self.resultados_zonas = {}
        self.costo_total_optimizado = 0
        
        if MOSTRAR_PROGRESO:
            print(f"\nINICIANDO OPTIMIZACIÓN DE RUTAS POR ZONAS")
            print(f"Parámetros: T={temp_inicial}, decay={tasa_enfriamiento}")
            print("="*70)
        
        # Optimizar cada zona
        num_zonas = len(self.data_loader.centros_distribucion)
        
        for zona_id in range(num_zonas):
            tiendas_zona = self.data_loader.obtener_tiendas_por_zona(zona_id)
            centro_zona = self.data_loader.obtener_centro_por_zona(zona_id)
            
            if MOSTRAR_PROGRESO:
                print(f"\nOptimizando {centro_zona['Nombre']}")
            
            if len(tiendas_zona) > 0:
                # Ejecutar optimización para esta zona con todos los parámetros
                ruta_optima, costo_optimo = SimulatedAnnealing.optimizar_zona(
                    self.data_loader.costo_total_matrix,
                    zona_id,
                    tiendas_zona,
                    temp_inicial,
                    tasa_enfriamiento,
                    TEMP_FINAL,
                    L_ITERACIONES
                )
                
                # Guardar resultados
                self.resultados_zonas[zona_id] = {
                    'centro': centro_zona['Nombre'],
                    'ruta': ruta_optima,
                    'costo': costo_optimo,
                    'tiendas_count': len(tiendas_zona),
                    'capacidad_total': tiendas_zona['Capacidad_Venta'].sum()
                }
                
                self.costo_total_optimizado += costo_optimo
                
                if MOSTRAR_PROGRESO:
                    print(f"    Optimización completada - Costo final: {costo_optimo:.2f}")
            else:
                if MOSTRAR_PROGRESO:
                    print(f"    Sin tiendas asignadas")
        
        return self.resultados_zonas, self.costo_total_optimizado
    
    def obtener_resumen_resultados(self):
        if not self.resultados_zonas:
            return None
        
        total_tiendas = sum(resultado['tiendas_count'] for resultado in self.resultados_zonas.values())
        total_capacidad = sum(resultado['capacidad_total'] for resultado in self.resultados_zonas.values())
        zonas_activas = len([r for r in self.resultados_zonas.values() if r['tiendas_count'] > 0])
        
        return {
            'zonas_totales': len(self.resultados_zonas),
            'zonas_activas': zonas_activas,
            'total_tiendas': total_tiendas,
            'total_capacidad': total_capacidad,
            'costo_total': self.costo_total_optimizado,
            'costo_promedio_por_zona': self.costo_total_optimizado / zonas_activas if zonas_activas > 0 else 0
        }
    
    def obtener_ruta_formateada(self, zona_id):

        if zona_id not in self.resultados_zonas:
            return []
        
        ruta_indices = self.resultados_zonas[zona_id]['ruta']
        ruta_nombres = []
        
        for nodo in ruta_indices:
            nombre = self.data_loader.datos_df.iloc[nodo]['Nombre']
            ruta_nombres.append(nombre)
        
        return ruta_nombres