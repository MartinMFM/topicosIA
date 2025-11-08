from seleccion import poblacionInicial, clasificacionRutas, seleccionRutas, grupoApareamiento
from operadores_geneticos import reproduccionPoblacion, mutacionPoblacion

def nuevaGeneracion(generacionActual, indivSelecionados, razonMutacion):
	"""
	Crea una nueva generación mediante selección, crossover y mutación
	
	ARGUMENTOS:
		generacionActual: Población actual de rutas
		indivSelecionados: Número de mejores individuos (elite)
		razonMutacion: Probabilidad de mutación
	
	RETORNA:
		Nueva población (siguiente generación)
	"""
	# Clasificar rutas
	popRanked = clasificacionRutas(generacionActual)

	# Selección de los candidatos
	selectionResults = seleccionRutas(popRanked, indivSelecionados)

	# Generar grupo de apareamiento
	grupoApa = grupoApareamiento(generacionActual, selectionResults)

	# Generación de la población cruzada, reproducida
	hijos = reproduccionPoblacion(grupoApa, indivSelecionados)

	# Incluir las mutaciones en la nueva generación
	nuevaGeneracion = mutacionPoblacion(hijos, razonMutacion)

	return nuevaGeneracion

def algoritmoGenetico(poblacion, tamanoPoblacion, indivSelecionados, razonMutacion, generaciones, verbose=True):
	"""
	Ejecuta el algoritmo genético para optimizar rutas (Problema del Viajante)
	
	ARGUMENTOS:
		poblacion: Lista de ciudades a visitar
		tamanoPoblacion: Número de individuos en cada generación
		indivSelecionados: Número de mejores individuos (elite)
		razonMutacion: Probabilidad de mutación
		generaciones: Número de iteraciones del algoritmo
		verbose: Si True, muestra información del progreso
	
	RETORNA:
		Tupla con (mejor_ruta, distancia_inicial, distancia_final)
	"""
	pop = poblacionInicial(tamanoPoblacion, poblacion)
	distanciaInicial = 1 / clasificacionRutas(pop)[0][1]
	
	if verbose:
		print("="*60)
		print("ALGORITMO GENETICO - OPTIMIZACION DE RUTAS")
		print("="*60)
		print(f"Parametros:")
		print(f"  - Tamaño de poblacion: {tamanoPoblacion}")
		print(f"  - Individuos seleccionados: {indivSelecionados}")
		print(f"  - Razon de mutacion: {razonMutacion}")
		print(f"  - Generaciones: {generaciones}")
		print(f"  - Numero de ciudades: {len(poblacion)}")
		print("="*60)
		print(f"\nDistancia Inicial: {distanciaInicial:.4f}")
		print("\nProgreso:")
	
	mejorDistanciaPorGeneracion = [distanciaInicial]
	
	# Evolución a través de generaciones
	for i in range(0, generaciones):
		pop = nuevaGeneracion(pop, indivSelecionados, razonMutacion)
		distanciaActual = 1 / clasificacionRutas(pop)[0][1]
		mejorDistanciaPorGeneracion.append(distanciaActual)
		
		if verbose and (i + 1) % 50 == 0:
			print(f"  Gen {i+1:4d}/{generaciones} - Distancia: {distanciaActual:.4f}")
	
	# Clasificar una sola vez al final para obtener la mejor ruta
	popRankedFinal = clasificacionRutas(pop)
	distanciaFinal = 1 / popRankedFinal[0][1]
	bestRouteIndex = popRankedFinal[0][0]
	mejorRuta = pop[bestRouteIndex]
	
	if verbose:
		mejoraTotal = ((distanciaInicial - distanciaFinal) / distanciaInicial) * 100
		print("\n" + "="*60)
		print("RESULTADOS FINALES")
		print("="*60)
		print(f"Distancia Inicial: {distanciaInicial:.4f}")
		print(f"Distancia Final:   {distanciaFinal:.4f}")
		print(f"Mejora Total:      {mejoraTotal:.2f}%")
		print(f"Reduccion:         {distanciaInicial - distanciaFinal:.4f}")
		print("="*60)
	
	return mejorRuta, distanciaInicial, distanciaFinal
