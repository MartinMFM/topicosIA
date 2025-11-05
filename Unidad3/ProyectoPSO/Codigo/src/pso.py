"""
Implementación del algoritmo PSO para optimización de sensores
"""
import numpy as np
from objetivo import funcion_objetivo_sensores
from utils import calcular_distancia
from reporte import GeneradorReportes
from visualizacion import graficar_resultados


class PSOSensores:
    """
    Algoritmo de Optimización por Enjambre de Partículas para ubicación de sensores agrícolas
    
    Implementa PSO para encontrar la distribución óptima de sensores de humedad
    en campos agrícolas, considerando factores como tipo de cultivo, variabilidad
    del suelo y topografía para maximizar la eficiencia del riego.
    
    Attributes:
        datos_campo (pd.DataFrame): Datos de las parcelas del campo
        n_sensores (int): Número de sensores a ubicar
        n_particulas (int): Tamaño del enjambre de partículas
        n_iteraciones (int): Número máximo de iteraciones
        dimensiones (int): Dimensiones del problema (n_sensores * 2)
        mejor_global_posicion (np.ndarray): Mejor solución encontrada
        mejor_global_valor (float): Mejor valor de función objetivo
        historial_convergencia (list): Historial de convergencia del algoritmo
    """
    
    def __init__(self, datos_campo, n_sensores=5, n_particulas=30, n_iteraciones=100):
        """
        Inicializar el optimizador PSO para ubicación de sensores
        
        Configura los parámetros del algoritmo PSO y establece los límites
        geográficos basados en los datos del campo.
        
        Args:
            datos_campo (pd.DataFrame): DataFrame con datos de las parcelas
            n_sensores (int, optional): Número de sensores a ubicar. Default: 5
            n_particulas (int, optional): Tamaño del enjambre. Default: 30  
            n_iteraciones (int, optional): Iteraciones máximas. Default: 100
            
        Note:
            Los límites geográficos se determinan automáticamente a partir
            de las coordenadas mínimas y máximas en los datos del campo.
        """
        self.datos_campo = datos_campo
        self.n_sensores = n_sensores
        self.n_particulas = n_particulas
        self.n_iteraciones = n_iteraciones
        
        # Límites geográficos de Guasave
        self.lat_min = datos_campo['Latitud'].min()
        self.lat_max = datos_campo['Latitud'].max()
        self.lon_min = datos_campo['Longitud'].min()
        self.lon_max = datos_campo['Longitud'].max()
        
        # Dimensiones: n_sensores * 2 (lat, lon para cada sensor)
        self.dimensiones = n_sensores * 2
        
        # Límites para PSO
        self.limites = []
        for _ in range(n_sensores):
            self.limites.append([self.lat_min, self.lat_max])  # Latitud
            self.limites.append([self.lon_min, self.lon_max])  # Longitud
        self.limites = np.array(self.limites)
        
        # Parámetros PSO
        self.w = 0.7
        self.c1 = 1.5
        self.c2 = 1.5
        
        # Inicialización
        self._inicializar_enjambre()
        
        # Mejores valores
        self.mejor_global_posicion = None
        self.mejor_global_valor = float('inf')
        self.historial_convergencia = []
    
    def _inicializar_enjambre(self):
        """
        Inicializar el enjambre de partículas con posiciones y velocidades aleatorias
        
        Genera posiciones aleatorias dentro de los límites geográficos del campo
        y velocidades iniciales pequeñas para una exploración controlada del
        espacio de soluciones.
        
        Note:
            - Posiciones: Distribuidas uniformemente en el área del campo
            - Velocidades: 1% del rango geográfico para convergencia estable
            - Mejores personales: Inicializados con posiciones actuales
        """
        # Posiciones aleatorias dentro de los límites geográficos
        self.posiciones = np.random.uniform(
            self.limites[:, 0], 
            self.limites[:, 1], 
            (self.n_particulas, self.dimensiones)
        )
        
        # Velocidades pequeñas
        rango_velocidad = (self.limites[:, 1] - self.limites[:, 0]) * 0.01
        self.velocidades = np.random.uniform(
            -rango_velocidad, 
            rango_velocidad, 
            (self.n_particulas, self.dimensiones)
        )
        
        # Mejores personales
        self.mejores_posiciones_personales = self.posiciones.copy()
        self.mejores_valores_personales = np.full(self.n_particulas, float('inf'))
    
    def _evaluar_particulas(self):
        """
        Evaluar todas las partículas del enjambre y actualizar mejores soluciones
        
        Calcula el valor de la función objetivo para cada partícula y actualiza
        tanto los mejores valores personales como el mejor global si se encuentran
        mejores soluciones.
        
        Note:
            - Evaluación: Utiliza función_objetivo_sensores para cada partícula
            - Actualización: Solo si el nuevo valor es mejor (menor costo)
            - Mejor global: Se actualiza cuando cualquier partícula mejora
        """
        for i in range(self.n_particulas):
            valor_actual = funcion_objetivo_sensores(self.posiciones[i], self.datos_campo, self.n_sensores)
            
            if valor_actual < self.mejores_valores_personales[i]:
                self.mejores_valores_personales[i] = valor_actual
                self.mejores_posiciones_personales[i] = self.posiciones[i].copy()
                
                if valor_actual < self.mejor_global_valor:
                    self.mejor_global_valor = valor_actual
                    self.mejor_global_posicion = self.posiciones[i].copy()
    
    def _actualizar_velocidades(self):
        """
        Actualizar velocidades del enjambre usando la ecuación estándar de PSO
        
        Aplica la ecuación de velocidad de PSO que combina:
        - Componente de inercia (w): Mantiene dirección previa
        - Componente cognitiva (c1): Atracción hacia mejor personal  
        - Componente social (c2): Atracción hacia mejor global
        
        Note:
            - Inercia w=0.7: Balance entre exploración y explotación
            - Coeficientes c1=c2=1.5: Igual peso a experiencia personal y social
            - Límite de velocidad: 2% del rango geográfico para estabilidad
        """
        for i in range(self.n_particulas):
            r1 = np.random.random(self.dimensiones)
            r2 = np.random.random(self.dimensiones)
            
            cognitiva = self.c1 * r1 * (self.mejores_posiciones_personales[i] - self.posiciones[i])
            social = self.c2 * r2 * (self.mejor_global_posicion - self.posiciones[i])
            
            self.velocidades[i] = self.w * self.velocidades[i] + cognitiva + social
            
            # Limitar velocidad
            v_max = (self.limites[:, 1] - self.limites[:, 0]) * 0.02
            self.velocidades[i] = np.clip(self.velocidades[i], -v_max, v_max)
    
    def _actualizar_posiciones(self):
        """
        Actualizar posiciones de las partículas aplicando velocidades
        
        Mueve cada partícula sumando su velocidad a su posición actual y
        asegura que todas las partículas permanezcan dentro de los límites
        geográficos del campo.
        
        Note:
            - Movimiento: posicion_nueva = posicion_actual + velocidad
            - Restricciones: Clipping a límites geográficos [lat_min, lat_max] y [lon_min, lon_max]
            - Manejo de límites: Las partículas que salen del área son reubicadas en el borde
        """
        self.posiciones += self.velocidades
        
        # Mantener dentro de límites geográficos
        for d in range(self.dimensiones):
            self.posiciones[:, d] = np.clip(self.posiciones[:, d], 
                                          self.limites[d, 0], self.limites[d, 1])
    
    def optimizar(self, verbose=True, guardar_progreso=False, archivo_progreso="progreso_pso.txt"):
        """
        Ejecutar el algoritmo de optimización PSO para ubicación de sensores
        
        Implementa el bucle principal del algoritmo PSO: inicialización, evaluación,
        actualización de velocidades y posiciones, y seguimiento de convergencia.
        
        Args:
            verbose (bool, optional): Si mostrar información de progreso. Default: True
            guardar_progreso (bool, optional): Si guardar progreso en archivo. Default: False
            archivo_progreso (str, optional): Nombre del archivo de progreso. Default: "progreso_pso.txt"
            
        Returns:
            dict: Diccionario con resultados de optimización:
                - sensores_optimos (np.ndarray): Coordenadas [lat, lon] de cada sensor
                - costo_minimo (float): Mejor valor de función objetivo encontrado
                - historial (list): Evolución del mejor costo por iteración
                
        Note:
            - Progreso: Se muestra cada 20 iteraciones si verbose=True
            - Archivo: Se guarda progreso cada 10 iteraciones si guardar_progreso=True
            - Convergencia: El algoritmo puede terminar antes si encuentra solución óptima
            - Resultados: Incluye análisis de cobertura y eficiencia del sistema
        """
        if verbose:
            self._mostrar_encabezado(guardar_progreso, archivo_progreso)
        
        # Inicializar archivo de progreso
        if guardar_progreso:
            GeneradorReportes.inicializar_archivo(
                archivo_progreso, self.n_sensores, self.n_particulas, 
                self.n_iteraciones, self.datos_campo
            )
        
        # Evaluación inicial
        self._evaluar_particulas()
        self.historial_convergencia.append(self.mejor_global_valor)
        
        # Bucle principal
        for iteracion in range(self.n_iteraciones):
            self._actualizar_velocidades()
            self._actualizar_posiciones()
            self._evaluar_particulas()
            
            self.historial_convergencia.append(self.mejor_global_valor)
            
            # Mostrar progreso cada 20 iteraciones
            if verbose and (iteracion + 1) % 20 == 0:
                print(f"Iteración {iteracion + 1}: Costo = {self.mejor_global_valor:.2f}")
            
            # Guardar progreso cada 10 iteraciones
            if guardar_progreso and (iteracion + 1) % 10 == 0:
                GeneradorReportes.guardar_progreso(
                    archivo_progreso, iteracion + 1, self.mejor_global_valor,
                    self.mejor_global_posicion, self.n_sensores, 
                    self.historial_convergencia
                )
        
        if verbose:
            self._mostrar_resultados()
        
        # Guardar resultado final
        if guardar_progreso:
            GeneradorReportes.guardar_resultado_final(
                archivo_progreso, self.mejor_global_valor, self.mejor_global_posicion,
                self.n_sensores, self.historial_convergencia, self.datos_campo
            )
        
        return {
            'sensores_optimos': self.mejor_global_posicion.reshape(self.n_sensores, 2),
            'costo_minimo': self.mejor_global_valor,
            'historial': self.historial_convergencia
        }
    
    def _mostrar_encabezado(self, guardar_progreso, archivo_progreso):
        """Mostrar encabezado de optimización"""
        print("=" * 70)
        print("PSO PARA OPTIMIZACIÓN DE UBICACIÓN DE SENSORES AGRÍCOLAS")
        print("=" * 70)
        print(f"Región: Guasave, Sinaloa")
        print(f"Sensores a ubicar: {self.n_sensores}")
        print(f"Parcelas del campo: {len(self.datos_campo)}")
        print(f"Partículas: {self.n_particulas}")
        print(f"Iteraciones máx: {self.n_iteraciones}")
        if guardar_progreso:
            print(f"Guardando progreso en: {archivo_progreso}")
        print()
    
    def _mostrar_resultados(self):
        """
        Mostrar análisis detallado de los resultados de optimización
        
        Presenta un resumen completo de la solución encontrada incluyendo:
        coordenadas de sensores, métricas de cobertura y eficiencia del sistema.
        
        Note:
            - Coordenadas: Latitud y longitud de cada sensor óptimo
            - Cobertura: Distancia promedio de parcelas al sensor más cercano  
            - Eficiencia: Inverso de la cobertura promedio como porcentaje
            - Unidades: Distancias convertidas a kilómetros para interpretación práctica
        """
        sensores = self.mejor_global_posicion.reshape(self.n_sensores, 2)
        
        print(f"\n RESULTADOS DE OPTIMIZACIÓN")
        print("=" * 50)
        print(f"Costo total mínimo: {self.mejor_global_valor:.2f}")
        print(f"\n Ubicaciones óptimas de sensores:")
        
        for i, (lat, lon) in enumerate(sensores, 1):
            print(f"   Sensor {i}: Lat {lat:.6f}, Lon {lon:.6f}")
        
        # Calcular cobertura promedio
        cobertura_promedio = self._calcular_cobertura_promedio(sensores)
        print(f"\n Métricas del sistema:")
        print(f"   Cobertura promedio: {cobertura_promedio:.1f} km")
        print(f"   Eficiencia de monitoreo: {(1/cobertura_promedio)*100:.1f}%")
    
    def _calcular_cobertura_promedio(self, sensores):
        """
        Calcular la distancia promedio de todas las parcelas al sensor más cercano
        
        Métrica de calidad del sistema que indica qué tan bien distribuidos
        están los sensores para cubrir todo el campo agrícola.
        
        Args:
            sensores (np.ndarray): Array de coordenadas [lat, lon] de los sensores
            
        Returns:
            float: Distancia promedio en kilómetros de parcelas a sensores
            
        Note:
            - Cálculo: Para cada parcela, encuentra el sensor más cercano
            - Conversión: De grados geográficos a kilómetros (1° ≈ 111 km)
            - Interpretación: Menor distancia promedio = mejor cobertura
        """
        distancias = []
        for _, parcela in self.datos_campo.iterrows():
            lat_parcela = parcela['Latitud']
            lon_parcela = parcela['Longitud']
            
            dist_min = float('inf')
            for sensor_lat, sensor_lon in sensores:
                dist = calcular_distancia(lat_parcela, lon_parcela, sensor_lat, sensor_lon)
                dist_min = min(dist_min, dist)
            
            # Convertir a km aproximadamente (1 grado ≈ 111 km)
            distancias.append(dist_min * 111)
        
        return np.mean(distancias)
    
    def graficar_resultados(self):
        """
        Generar visualizaciones de los resultados de optimización PSO
        
        Crea dos gráficas principales para análisis de resultados:
        1. Convergencia del algoritmo PSO a lo largo de las iteraciones
        2. Mapa geográfico con ubicación óptima de sensores y distribución de cultivos
        
        Note:
            - Gráfica 1: Evolución del costo (función objetivo) vs iteraciones
            - Gráfica 2: Mapa con parcelas coloreadas por cultivo y sensores marcados
            - Colores: Maíz (azul), Chile (cyan), Tomate (verde), Sensores (rojo)
            - Escalas: Coordenadas geográficas reales de Guasave, Sinaloa
        """
        graficar_resultados(
            self.historial_convergencia, 
            self.datos_campo, 
            self.mejor_global_posicion,
            self.n_sensores
        )
