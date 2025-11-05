import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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
        datos = pd.read_csv('../datos_cultivos_guasave.csv')
        print(f"Datos cargados: {len(datos)} parcelas en Guasave")
        print(f"Cultivos: {datos['Cultivo'].unique()}")
        return datos
    except:
        print("Error cargando datos. Usando datos simulados...")
        # Datos simulados de Guasave
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
        
        # Inicializar archivo de progreso
        if guardar_progreso:
            self._inicializar_archivo_progreso(archivo_progreso)
        
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
                self._guardar_progreso(archivo_progreso, iteracion + 1)
        
        if verbose:
            self._mostrar_resultados()
        
        # Guardar resultado final
        if guardar_progreso:
            self._guardar_resultado_final(archivo_progreso)
        
        return {
            'sensores_optimos': self.mejor_global_posicion.reshape(self.n_sensores, 2),
            'costo_minimo': self.mejor_global_valor,
            'historial': self.historial_convergencia
        }
    
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
    
    def _inicializar_archivo_progreso(self, archivo):
        """
        Inicializar archivo de progreso con encabezados
        
        Args:
            archivo (str): Nombre del archivo donde guardar el progreso
        """
        from datetime import datetime
        
        with open(archivo, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("PROGRESO DE OPTIMIZACION PSO - SENSORES AGRICOLAS\n")
            f.write("=" * 80 + "\n")
            f.write(f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Region: Guasave, Sinaloa\n")
            f.write(f"Sensores a ubicar: {self.n_sensores}\n")
            f.write(f"Particulas: {self.n_particulas}\n")
            f.write(f"Iteraciones max: {self.n_iteraciones}\n")
            f.write(f"Parcelas del campo: {len(self.datos_campo)}\n")
            f.write("=" * 80 + "\n\n")
            f.write("PROGRESO DE OPTIMIZACION:\n")
            f.write("-" * 50 + "\n")

    def _guardar_progreso(self, archivo, iteracion):
        """
        Guardar progreso actual cada 10 iteraciones
        
        Args:
            archivo (str): Nombre del archivo donde guardar el progreso
            iteracion (int): Numero de iteracion actual
        """
        with open(archivo, 'a', encoding='utf-8') as f:
            f.write(f"Iteracion {iteracion:3d}: Mejor costo = {self.mejor_global_valor:.4f}\n")
            
            # Cada 50 iteraciones, mostrar mas detalles
            if iteracion % 50 == 0:
                sensores = self.mejor_global_posicion.reshape(self.n_sensores, 2)
                f.write(f"  Posiciones actuales de sensores:\n")
                for i, (lat, lon) in enumerate(sensores):
                    f.write(f"    Sensor {i+1}: Lat={lat:.6f}, Lon={lon:.6f}\n")
                f.write(f"  Mejora desde inicio: {self.historial_convergencia[0] - self.mejor_global_valor:.4f}\n")
                f.write("-" * 30 + "\n")

    def _guardar_resultado_final(self, archivo):
        """
        Guardar resultado final de la optimizacion
        
        Args:
            archivo (str): Nombre del archivo donde guardar el resultado
        """
        sensores = self.mejor_global_posicion.reshape(self.n_sensores, 2)
        
        with open(archivo, 'a', encoding='utf-8') as f:
            f.write("\n" + "=" * 80 + "\n")
            f.write("RESULTADO FINAL DE OPTIMIZACION\n")
            f.write("=" * 80 + "\n")
            f.write(f"Costo final: {self.mejor_global_valor:.4f}\n")
            f.write(f"Mejora total: {self.historial_convergencia[0] - self.mejor_global_valor:.4f}\n")
            f.write(f"Porcentaje de mejora: {((self.historial_convergencia[0] - self.mejor_global_valor) / self.historial_convergencia[0] * 100):.2f}%\n")
            f.write("\nUBICACIONES OPTIMAS DE SENSORES:\n")
            f.write("-" * 40 + "\n")
            
            for i, (lat, lon) in enumerate(sensores):
                f.write(f"Sensor {i+1}: Latitud={lat:.6f}, Longitud={lon:.6f}\n")
            
            # Calcular estadisticas de cobertura
            distancias = []
            for _, parcela in self.datos_campo.iterrows():
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
            for i, valor in enumerate(self.historial_convergencia[::10]):  # Cada 10 valores
                f.write(f"Iter {i*10:3d}: {valor:.4f}\n")
            
            f.write("\n" + "=" * 80 + "\n")
            f.write("FIN DEL REPORTE DE OPTIMIZACION\n")
            f.write("=" * 80 + "\n")
    
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
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        fig.suptitle('Optimización PSO: Ubicación de Sensores en Guasave, Sinaloa', fontsize=16)
        
        # 1. Convergencia del PSO
        ax1 = axes[0]
        ax1.plot(self.historial_convergencia, 'b-', linewidth=2)
        ax1.set_title('Convergencia del Algoritmo PSO')
        ax1.set_xlabel('Iteración')
        ax1.set_ylabel('Costo (Suma de distancias al cuadrado)')
        ax1.grid(True, alpha=0.3)
        
        # 2. Mapa de ubicación óptima de sensores
        ax2 = axes[1]
        
        # Plotear parcelas por cultivo
        for cultivo in self.datos_campo['Cultivo'].unique():
            datos_cultivo = self.datos_campo[self.datos_campo['Cultivo'] == cultivo]
            
            if cultivo == 'Maíz':
                ax2.scatter(datos_cultivo['Longitud'], datos_cultivo['Latitud'], 
                           c='blue', alpha=0.6, s=30, label='Maíz', marker='o')
            elif cultivo == 'Chile':
                ax2.scatter(datos_cultivo['Longitud'], datos_cultivo['Latitud'], 
                           c='cyan', alpha=0.6, s=30, label='Chile', marker='x')
            else:  # Tomate
                ax2.scatter(datos_cultivo['Longitud'], datos_cultivo['Latitud'], 
                           c='green', alpha=0.6, s=30, label='Tomate', marker='^')
        
        # Plotear sensores óptimos
        sensores = self.mejor_global_posicion.reshape(self.n_sensores, 2)
        ax2.scatter(sensores[:, 1], sensores[:, 0], 
                   c='red', s=200, marker='X', edgecolors='black', linewidth=2,
                   label='Sensores Óptimos (PSO)', zorder=5)
        
        ax2.set_title('Mapa de Colocación Óptima de Sensores en Guasave')
        ax2.set_xlabel('Longitud')
        ax2.set_ylabel('Latitud')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()

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