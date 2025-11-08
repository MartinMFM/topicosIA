import random
import numpy as np
from municipio import municipio
from aptitud import Aptitud
from seleccion import crearRuta, poblacionInicial, clasificacionRutas, seleccionRutas
from operadores_geneticos import reproduccion, mutacion


# CONFIGURACIÓN DE PRUEBAS
def crear_ciudades_prueba(n=5):
	"""Crea un conjunto de ciudades de prueba con coordenadas conocidas"""
	coordenadas = [
		(0, 0, "A"),
		(0, 1, "B"),
		(1, 1, "C"),
		(1, 0, "D"),
		(0.5, 0.5, "E")
	]
	return [municipio(x, y, nombre) for x, y, nombre in coordenadas[:n]]


# PRUEBA 1: FUNCIÓN DE APTITUD CON ENTRADAS CONOCIDAS
def test_aptitud_distancias_conocidas():
	"""
	Prueba que la función de aptitud calcula correctamente las distancias
	usando casos conocidos y verificables
	"""
	print("\n" + "="*70)
	print("PRUEBA 1: FUNCION DE APTITUD - DISTANCIAS CONOCIDAS")
	print("="*70)
	
	# Caso 1: Cuadrado unitario (distancia conocida = 4.0)
	c1 = municipio(0, 0, "Origen")
	c2 = municipio(1, 0, "Este")
	c3 = municipio(1, 1, "NorEste")
	c4 = municipio(0, 1, "Norte")
	
	ruta_cuadrado = [c1, c2, c3, c4]
	aptitud_cuadrado = Aptitud(ruta_cuadrado)
	distancia_cuadrado = aptitud_cuadrado.distanciaRuta()
	
	distancia_esperada = 4.0
	
	print(f"\n  Cuadrado unitario:")
	print(f"    Distancia calculada: {distancia_cuadrado:.4f} | Esperada: {distancia_esperada:.4f}")
	print(f"    CORRECTO" if abs(distancia_cuadrado - distancia_esperada) < 0.001 else f"    ERROR")
	
	# Caso 2: Triángulo rectángulo
	t1 = municipio(0, 0, "A")
	t2 = municipio(2, 0, "B")
	t3 = municipio(2, 2, "C")
	
	ruta_triangulo = [t1, t2, t3]
	distancia_triangulo = Aptitud(ruta_triangulo).distanciaRuta()
	distancia_esperada_triangulo = 2 + 2 + np.sqrt(8)

	print(f"\n  Triangulo rectangulo:")
	print(f"    Distancia calculada: {distancia_triangulo:.4f} | Esperada: {distancia_esperada_triangulo:.4f}")
	print(f"    CORRECTO" if abs(distancia_triangulo - distancia_esperada_triangulo) < 0.001 else f"    ERROR")
	
	# Caso 3: Verificar que rutas más cortas tienen mayor aptitud
	# Ruta corta: solo 3 puntos en línea recta horizontal
	ruta_corta = [c1, c2]
	# Ruta larga: 4 puntos formando un cuadrado completo
	ruta_larga = [c1, c2, c3, c4]  
	
	distancia_corta = Aptitud(ruta_corta).distanciaRuta()
	distancia_larga = Aptitud(ruta_larga).distanciaRuta()
	aptitud_corta = Aptitud(ruta_corta).rutaApta()
	aptitud_larga = Aptitud(ruta_larga).rutaApta()
	
	print(f"\n  Comparacion aptitudes (corta vs larga):")
	print(f"    Ruta corta  - Distancia: {distancia_corta:.4f}, Aptitud: {aptitud_corta:.4f}")
	print(f"    Ruta larga  - Distancia: {distancia_larga:.4f}, Aptitud: {aptitud_larga:.4f}")
	print(f"    CORRECTO: Ruta corta > Ruta larga" if aptitud_corta > aptitud_larga else f"    ERROR")


# PRUEBA 2: PROCESO DE SELECCIÓN Y DISTRIBUCIÓN
def test_seleccion_distribucion():
	"""
	Verifica que el proceso de selección funciona correctamente
	y que los mejores individuos tienen mayor probabilidad de ser seleccionados
	"""
	print("\n" + "="*70)
	print("PRUEBA 2: PROCESO DE SELECCION Y DISTRIBUCION")
	print("="*70)
	
	ciudades = crear_ciudades_prueba(5)
	poblacion = poblacionInicial(20, ciudades)
	popRanked = clasificacionRutas(poblacion)
	
	print(f"\n  Poblacion: {len(poblacion)} individuos")
	print(f"  Mejor aptitud:  {popRanked[0][1]:.6f}")
	print(f"  Peor aptitud:   {popRanked[-1][1]:.6f}")
	
	# Verificar ordenamiento
	aptitudes = [apt for idx, apt in popRanked]
	esta_ordenada = all(aptitudes[i] >= aptitudes[i+1] for i in range(len(aptitudes)-1))
	print(f"  Ordenamiento correcto" if esta_ordenada else f"  ERROR: No ordenada")
	
	# Verificar elitismo
	seleccionados = seleccionRutas(popRanked, 5)
	elite_indices = [popRanked[i][0] for i in range(5)]
	elite_incluida = all(idx in seleccionados for idx in elite_indices)
	print(f"  Elite preservada (top 5)" if elite_incluida else f"  ERROR: Elite no preservada")
	
	# Análisis estadístico
	print(f"\n  Analisis estadistico (1000 iteraciones):")
	conteo_selecciones = {i: 0 for i in range(len(poblacion))}
	
	for _ in range(1000):
		seleccionados = seleccionRutas(popRanked, 5)
		for idx in seleccionados:
			conteo_selecciones[idx] += 1
	
	items_ordenados = sorted(conteo_selecciones.items(), key=lambda x: x[1], reverse=True)
	top5_promedio = sum(count for idx, count in items_ordenados[:5]) / 5
	bottom5_promedio = sum(count for idx, count in items_ordenados[-5:]) / 5
	
	print(f"    Promedio top 5:    {top5_promedio:.1f} selecciones")
	print(f"    Promedio bottom 5: {bottom5_promedio:.1f} selecciones")
	print(f"  Seleccion favorece mejores" if top5_promedio > bottom5_promedio * 2 else f"  ERROR: Distribucion incorrecta")


# PRUEBA 3: OPERADORES GENÉTICOS - VALIDEZ DE DESCENDENCIA
def test_operadores_geneticos_validez():
	"""
	Verifica que crossover y mutación producen descendencia válida
	(todas las ciudades presentes, sin duplicados)
	"""
	print("\n" + "="*70)
	print("PRUEBA 3: OPERADORES GENETICOS - VALIDEZ DE DESCENDENCIA")
	print("="*70)
	
	ciudades = crear_ciudades_prueba(5)
	
	# CROSSOVER 
	print("\n  A. Operador de Crossover (Order Crossover)")
	
	padre1 = list(ciudades)
	padre2 = list(reversed(ciudades))
	
	hijos_validos = 0
	for i in range(100):
		hijo = reproduccion(padre1, padre2)
		longitud_correcta = len(hijo) == len(padre1)
		sin_duplicados = len(hijo) == len(set(hijo))
		todas_presentes = set(hijo) == set(padre1)
		
		if longitud_correcta and sin_duplicados and todas_presentes:
			hijos_validos += 1
	
	print(f"    Hijos validos: {hijos_validos}/100")
	print(f"    Crossover correcto" if hijos_validos == 100 else f"    ERROR: {100-hijos_validos} invalidos")
	
	# MUTACIÓN 
	print("\n  B. Operador de MutaciOn (Swap Mutation)")
	
	ruta_original = list(ciudades)
	mutaciones_validas = 0
	mutaciones_efectivas = 0
	
	for i in range(100):
		ruta_copia = ruta_original.copy()
		ruta_mutada = mutacion(ruta_copia, razonMutacion=0.5)
		
		longitud_correcta = len(ruta_mutada) == len(ruta_original)
		sin_duplicados = len(ruta_mutada) == len(set(ruta_mutada))
		todas_presentes = set(ruta_mutada) == set(ruta_original)
		
		if longitud_correcta and sin_duplicados and todas_presentes:
			mutaciones_validas += 1
		
		if ruta_mutada != ruta_original:
			mutaciones_efectivas += 1
	
	print(f"    Mutaciones validas: {mutaciones_validas}/100")
	print(f"    Mutaciones efectivas: {mutaciones_efectivas}/100")
	print(f"    Mutacion correcta" if mutaciones_validas == 100 else f"    ERROR: {100-mutaciones_validas} invalidas")
	
	# PRESERVACIÓN DEL ORIGINAL 
	print("\n  C. Verificar preservacion del original")
	ruta_test = list(ciudades)
	ruta_test_copia = ruta_test.copy()
	ruta_mutada = mutacion(ruta_test, razonMutacion=1.0)
	
	original_preservado = ruta_test == ruta_test_copia
	print(f"    Original preservado" if original_preservado else f"    ERROR: Original modificado")


# EJECUTAR TODAS LAS PRUEBAS
def ejecutar_todas_las_pruebas():
	"""Ejecuta las pruebas principales y genera un reporte"""
	print("\n" + "="*70)
	print("SUITE DE PRUEBAS - ALGORITMO GENETICO TSP")
	print("="*70)
	
	try:
		test_aptitud_distancias_conocidas()
		test_seleccion_distribucion()
		test_operadores_geneticos_validez()
		
		print("\n" + "="*70)
		print("PRUEBAS COMPLETADAS EXITOSAMENTE")
		
	except Exception as e:
		print(f"\nERROR: {str(e)}")
		import traceback
		traceback.print_exc()


# PUNTO DE ENTRADA
if __name__ == "__main__":
	ejecutar_todas_las_pruebas()
