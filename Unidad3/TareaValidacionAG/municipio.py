import numpy as np

class municipio:
	"""
	Representa una ciudad con coordenadas geográficas
	
	ARGUMENTOS:
		x: Coordenada X (latitud)
		y: Coordenada Y (longitud)
		nombre: Nombre de la ciudad (opcional)
	"""
	def __init__(self, x, y, nombre=None):
		self.x = x
		self.y = y
		self.nombre = nombre
	
	def distancia(self, municipio):
		"""
		Calcula la distancia euclidiana entre dos municipios usando el teorema de Pitágoras
		
		ARGUMENTOS:
			municipio: Objeto municipio con el que se calcula la distancia
		
		RETORNA:
			Distancia euclidiana entre los dos municipios
		"""
		xDis = abs(self.x - municipio.x)
		yDis = abs(self.y - municipio.y)
		distancia = np.sqrt((xDis ** 2) + (yDis ** 2))
		return distancia

	def __repr__(self):
		"""
		Devuelve una representación en string del municipio
		
		RETORNA:
			String con nombre y coordenadas o solo coordenadas
		"""
		if self.nombre:
			return f"{self.nombre} ({self.x}, {self.y})"
		return "(" + str(self.x) + "," + str(self.y) + ")"
