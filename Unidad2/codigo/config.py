# Archivos de datos
ARCHIVO_DATOS_TIENDAS = 'datos_distribucion_tiendas.xlsx'
ARCHIVO_MATRIZ_DISTANCIAS = 'matriz_distancias.xlsx'
ARCHIVO_MATRIZ_COMBUSTIBLE = 'matriz_costos_combustible.xlsx'
ARCHIVO_RESULTADOS = 'resultados_optimizacion_zonas.txt'

# Parámetros del algoritmo de recocido simulado
TEMPERATURA_INICIAL = 5000
TASA_ENFRIAMIENTO = 0.995
TEMP_FINAL = 0.001
L_ITERACIONES = 50

# Configuración de salida
MOSTRAR_PROGRESO = True
PROGRESO_CADA_PORCENTAJE = 25
ENCODING_ARCHIVO = 'utf-8'

# Nombres de columnas esperadas en los datos
COLUMNAS_ESPERADAS = {
    'tipo': 'Tipo',
    'nombre': 'Nombre',
    'latitud': 'Latitud_WGS84',
    'longitud': 'Longitud_WGS84',
    'capacidad': 'Capacidad_Venta'
}

# Tipos de ubicaciones
TIPO_CENTRO_DISTRIBUCION = 'Centro de Distribución'
TIPO_TIENDA = 'Tienda'