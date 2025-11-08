import random
import numpy as np
import pandas as pd
import operator
from aptitud import Aptitud

def crearRuta(listaMunicipios):
	"""
	Crea una ruta aleatoria visitando todos los municipios
	
	ARGUMENTOS:
		listaMunicipios: Lista de objetos municipio a visitar
	
	RETORNA:
		Lista de municipios en orden aleatorio (una ruta)
	"""
	route = random.sample(listaMunicipios, len(listaMunicipios))
	return route

def poblacionInicial(tamanoPob, listaMunicipios):
	"""
	Genera la población inicial de rutas aleatorias
	
	ARGUMENTOS:
		tamanoPob: Número de individuos en la población
		listaMunicipios: Lista de municipios a visitar
	
	RETORNA:
		Lista de rutas (población inicial)
	"""
	poblacion = []

	for i in range(0, tamanoPob):
		poblacion.append(crearRuta(listaMunicipios))
	return poblacion

def clasificacionRutas(poblacion):
	"""
	Evalúa y clasifica todas las rutas de la población por aptitud
	
	ARGUMENTOS:
		poblacion: Lista de rutas a evaluar
	
	RETORNA:
		Lista de tuplas (índice, aptitud) ordenadas de mayor a menor aptitud
	"""
	fitnessResults = {}
	
	for i in range(0, len(poblacion)):
		fitnessResults[i] = Aptitud(poblacion[i]).rutaApta()
	# Ordenar rutas por aptitud (de mayor a menor)
	return sorted(fitnessResults.items(), key=operator.itemgetter(1), reverse=True)

def seleccionRutas(popRanked, indivSelecionados):
	"""
	Selecciona individuos para reproducción usando elitismo y selección por ruleta
	
	ARGUMENTOS:
		popRanked: Población clasificada (lista de tuplas índice-aptitud)
		indivSelecionados: Número de mejores individuos a seleccionar directamente
	
	RETORNA:
		Lista de índices de individuos seleccionados
	"""
	resultadosSeleccion = []
	# Crea el DataFrame con los datos de aptitud
	df = pd.DataFrame(np.array(popRanked), columns=["Indice", "Aptitud"])
	df['cum_sum'] = df.Aptitud.cumsum()
	df['cum_perc'] = 100*df.cum_sum/df.Aptitud.sum()
	
	# Elitismo: seleccionar los mejores individuos directamente
	for i in range(0, indivSelecionados):
		resultadosSeleccion.append(popRanked[i][0])
	
	# Selección por ruleta para el resto
	for _ in range(0, len(popRanked) - indivSelecionados):
		seleccion = 100*random.random()  # Valor aleatorio entre 0 y 100
		for j in range(0, len(popRanked)):
			# Comprueba si el valor aleatorio cae dentro del porcentaje acumulado
			if seleccion <= df.iat[j, 3]:
				resultadosSeleccion.append(popRanked[j][0])
				break
	return resultadosSeleccion

def grupoApareamiento(poblacion, resultadosSeleccion):
	"""
	Extrae los individuos seleccionados de la población para apareamiento
	
	ARGUMENTOS:
		poblacion: Población completa de rutas
		resultadosSeleccion: Lista de índices de individuos seleccionados
	
	RETORNA:
		Lista de rutas seleccionadas para reproducción
	"""
	grupoApareamiento = []
	
	for i in range(0, len(resultadosSeleccion)):
		index = resultadosSeleccion[i]
		grupoApareamiento.append(poblacion[index])
	return grupoApareamiento
