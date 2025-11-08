class Aptitud:
	"""
	Calcula y almacena la aptitud (fitness) de una ruta
	
	ARGUMENTOS:
		ruta: Lista de objetos municipio que representa una ruta completa
	"""
	def __init__(self, ruta):
		self.ruta = ruta
		self.distancia = 0
		self.f_aptitud= 0.0
	
	def distanciaRuta(self):
		"""
		Calcula la distancia total de la ruta incluyendo el regreso al inicio
		
		RETORNA:
			Distancia total de la ruta
		"""
		if self.distancia ==0:
			distanciaRelativa = 0
			for i in range(0, len(self.ruta)):
				puntoInicial = self.ruta[i]
				puntoFinal = None
				if i + 1 < len(self.ruta):
					puntoFinal = self.ruta[i + 1]
				else:
					puntoFinal = self.ruta[0]
				distanciaRelativa += puntoInicial.distancia(puntoFinal)
			self.distancia = distanciaRelativa
		return self.distancia
	
	def rutaApta(self):
		"""
		Calcula la aptitud de la ruta (inverso de la distancia)
		
		RETORNA:
			Valor de aptitud (fitness) - mayor es mejor
		"""
		if self.f_aptitud == 0:
			self.f_aptitud = 1 / float(self.distanciaRuta())
		return self.f_aptitud
