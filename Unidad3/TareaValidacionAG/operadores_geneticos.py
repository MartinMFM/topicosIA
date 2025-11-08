import random

def reproduccion(progenitor1, progenitor2):
	"""
	Combina dos rutas progenitoras usando Order Crossover (OX)
	
	ARGUMENTOS:
		progenitor1: Primera ruta padre
		progenitor2: Segunda ruta padre
	
	RETORNA:
		Nueva ruta hijo resultado del crossover
	"""
	hijo = []
	hijoP1 = []
	hijoP2 = []
	
	# Se generan dos puntos de corte aleatorios
	generacionX = int(random.random() * len(progenitor1))
	generacionY = int(random.random() * len(progenitor2))
	
	# Determinar los puntos de corte
	generacionInicial = min(generacionX, generacionY)
	generacionFinal = max(generacionX, generacionY)

	# Se copian los genes entre los puntos de corte del primer progenitor
	for i in range(generacionInicial, generacionFinal):
		hijoP1.append(progenitor1[i])
		
	# Se rellenan los genes restantes del segundo progenitor
	hijoP2 = [item for item in progenitor2 if item not in hijoP1]

	hijo = hijoP1 + hijoP2
	return hijo

def reproduccionPoblacion(grupoApareamiento, indivSelecionados):
	"""
	Genera una nueva población mediante reproducción
	
	ARGUMENTOS:
		grupoApareamiento: Lista de individuos seleccionados para reproducción
		indivSelecionados: Número de elite que pasa sin cambios
	
	RETORNA:
		Lista de nuevas rutas (hijos)
	"""
	hijos = []
	tamano = len(grupoApareamiento) - indivSelecionados
	espacio = random.sample(grupoApareamiento, len(grupoApareamiento))

	for i in range(0, indivSelecionados):
		hijos.append(grupoApareamiento[i])
	
	for i in range(0, tamano):
		hijo = reproduccion(espacio[i], espacio[len(grupoApareamiento)-i-1])
		hijos.append(hijo)
	return hijos

def mutacion(individuo, razonMutacion):
	"""
	Aplica mutación por intercambio (swap) a una ruta
	
	ARGUMENTOS:
		individuo: Ruta a mutar
		razonMutacion: Probabilidad de mutación para cada posición
	
	RETORNA:
		Ruta mutada
	"""
	# Crear una copia para no modificar el original
	individuoMutado = individuo.copy()
	
	# Swap mutation: intercambia pares de ciudades
	for swapped in range(len(individuoMutado)):
		if(random.random() < razonMutacion):
			swapWith = int(random.random() * len(individuoMutado))
			
			# Intercambiar las ciudades en las posiciones swapped y swapWith
			lugar1 = individuoMutado[swapped]
			lugar2 = individuoMutado[swapWith]
			
			# Realizar el intercambio
			individuoMutado[swapped] = lugar2
			individuoMutado[swapWith] = lugar1
	return individuoMutado

def mutacionPoblacion(poblacion, razonMutacion):
	"""
	Aplica mutación a toda la población
	
	ARGUMENTOS:
		poblacion: Lista de rutas a mutar
		razonMutacion: Probabilidad de mutación
	
	RETORNA:
		Población mutada
	"""
	pobMutada = []
	
	for ind in range(0, len(poblacion)):
		individuoMutar = mutacion(poblacion[ind], razonMutacion)
		pobMutada.append(individuoMutar)
	return pobMutada
