import os
import pandas as pd
from municipio import municipio

def cargarCiudadesDesdeCSV(archivo_csv):
	"""
	Carga ciudades desde un archivo CSV
	
	ARGUMENTOS:
		archivo_csv: Nombre o ruta del archivo CSV con columnas: nombre, x, y
	
	RETORNA:
		Lista de objetos municipio
	"""
	# Obtener la ruta absoluta del directorio donde está este script
	script_dir = os.path.dirname(os.path.abspath(__file__))
	# Construir la ruta completa al archivo CSV
	ruta_completa = os.path.join(script_dir, archivo_csv)
	
	df = pd.read_csv(ruta_completa)
	listaCiudades = []
	
	# Iterar sobre las filas del DataFrame y crear objetos municipio
	for index, row in df.iterrows():
		nombre = row['nombre'] if 'nombre' in row else None
		ciudad = municipio(row['x'], row['y'], nombre)
		listaCiudades.append(ciudad)
	
	return listaCiudades
