import random
import math
from config import MOSTRAR_PROGRESO

class SimulatedAnnealing:
    
    @staticmethod
    def calcular_costo_ruta(ruta, matriz_costos):
        costo = 0
        for i in range(len(ruta) - 1):
            costo += matriz_costos[ruta[i]][ruta[i+1]]
        return costo
    
    @staticmethod
    def generar_solucion_inicial_zona(centro_id, tiendas_zona):

        tiendas_ids = list(tiendas_zona.index)  # Usar directamente los índices del DataFrame
        random.shuffle(tiendas_ids)
        ruta_inicial = [centro_id] + tiendas_ids + [centro_id]
        return ruta_inicial
    
    @staticmethod
    def generar_solucion_vecina(ruta):
        vecina = ruta[:]
        
        # Solo hacer swap si hay al menos 2 tiendas para intercambiar
        # Las posiciones 0 y -1 son el centro de distribución, no se tocan
        if len(vecina) > 3:  
            # Seleccionar dos posiciones diferentes entre las tiendas (posiciones 1 a len-2)
            pos1, pos2 = random.sample(range(1, len(vecina) - 1), 2)
            
            # Hacer el swap entre las dos posiciones seleccionadas
            vecina[pos1], vecina[pos2] = vecina[pos2], vecina[pos1]
            
        return vecina
    
    @classmethod
    def optimizar_zona(cls, matriz_costos, centro_id, tiendas_zona, 
                      temp_inicial, tasa_enfriamiento, 
                      temp_final=0.001, L=50):
        if len(tiendas_zona) == 0:
            if MOSTRAR_PROGRESO:
                print(f"     Zona {centro_id + 1} no tiene tiendas asignadas")
            return [centro_id + 1], 0
        
        # Inicializacion del algoritmo
        s_actual = cls.generar_solucion_inicial_zona(centro_id, tiendas_zona)
        costo_actual = cls.calcular_costo_ruta(s_actual, matriz_costos)
        
        s_mejor = s_actual[:]
        costo_mejor = costo_actual
        t = temp_inicial
        
        mejoras = 0
        
        if MOSTRAR_PROGRESO:
            print(f"    Zona {centro_id + 1}: {len(tiendas_zona)} tiendas, costo inicial: {costo_mejor:.2f}")
        
        # Bucle principal del recocido simulado
        # Termina cuando: temperatura < minima OR costo = 0
        while t > temp_final and costo_mejor > 0:
            
            # L iteraciones por cada temperatura
            for i in range(L):
                if costo_mejor == 0:
                    break
                
                # Generar solucion candidata usando swap entre dos puntos
                s_candidata = cls.generar_solucion_vecina(s_actual)
                costo_candidata = cls.calcular_costo_ruta(s_candidata, matriz_costos)
                
                delta_costo = costo_candidata - costo_actual
                
                # Criterio de aceptacion del recocido simulado
                if delta_costo < 0:
                    # Aceptar solucion mejor (siempre aceptamos mejoras)
                    s_actual = s_candidata
                    costo_actual = costo_candidata
                    
                    # Actualizar mejor solucion encontrada
                    if costo_actual < costo_mejor:
                        s_mejor = s_actual[:]
                        costo_mejor = costo_actual
                        mejoras += 1
                        
                        # Si encontramos la solucion optima (costo 0), terminar
                        if costo_mejor == 0:
                            if MOSTRAR_PROGRESO:
                                print(f"        Solucion optima encontrada! Costo = 0")
                            break
                        
                else:
                    # Aceptar solucion peor con probabilidad exp(-delta/T)
                    probabilidad = math.exp(-delta_costo / t) if t > 0 else 0
                    if random.random() < probabilidad:
                        s_actual = s_candidata
                        costo_actual = costo_candidata
            
            # Enfriar la temperatura despues de L iteraciones
            t *= tasa_enfriamiento
        
        # Determinar la razon de terminacion
        if MOSTRAR_PROGRESO:
            if costo_mejor == 0:
                razon = "solucion optima (costo = 0)"
            elif t <= temp_final:
                razon = "temperatura minima alcanzada"
            else:
                razon = "terminacion desconocida"
            
            print(f"        Optimizacion completada ({razon}) - Costo final: {costo_mejor:.2f} ({mejoras} mejoras)")
        
        return s_mejor, costo_mejor