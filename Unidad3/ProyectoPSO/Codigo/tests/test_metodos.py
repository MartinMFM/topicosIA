import sys
import os
import numpy as np
import pandas as pd

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from pso_sensores import (
    calcular_distancia,
    obtener_peso_cultivo,
    cargar_datos_cultivos,
    funcion_objetivo_sensores,
    PSOSensores
)

def test_calcular_distancia():
    """Pruebas basicas de calculo de distancia"""
    print("Probando calcular_distancia...")
    
    # Test 1: Distancia cero
    dist = calcular_distancia(0, 0, 0, 0)
    assert dist == 0, f"Distancia entre puntos iguales deberia ser 0, obtenido: {dist}"
    print("Test distancia cero: PASO")
    
    # Test 2: Distancia conocida
    dist = calcular_distancia(0, 0, 3, 4)
    expected = 5.0  # Triangulo 3-4-5
    assert abs(dist - expected) < 1e-10, f"Distancia esperada {expected}, obtenido: {dist}"
    print("Test distancia conocida: PASO")
    
    # Test 3: Simetria
    d1 = calcular_distancia(1, 2, 3, 4)
    d2 = calcular_distancia(3, 4, 1, 2)
    assert abs(d1 - d2) < 1e-10, f"Distancia no es simetrica: {d1} != {d2}"
    print("Test simetria: PASO")

def test_obtener_peso_cultivo():
    """Pruebas de pesos por cultivo"""
    print("\nProbando obtener_peso_cultivo...")
    
    # Test 1: Cultivos conocidos
    assert obtener_peso_cultivo('Maíz') == 2.17, "Error: Peso de Maiz incorrecto"
    assert obtener_peso_cultivo('Chile') == 1.5, "Error: Peso de Chile incorrecto"
    assert obtener_peso_cultivo('Tomate') == 0.99, "Error: Peso de Tomate incorrecto"
    print("Test cultivos conocidos: PASO")
    
    # Test 2: Cultivo desconocido
    peso = obtener_peso_cultivo('Inexistente')
    assert peso == 1.0, f"Error: Peso por defecto deberia ser 1.0, obtenido: {peso}"
    print("Test cultivo desconocido: PASO")
    
    # Test 3: Orden de importancia
    peso_maiz = obtener_peso_cultivo('Maíz')
    peso_chile = obtener_peso_cultivo('Chile')
    peso_tomate = obtener_peso_cultivo('Tomate')
    assert peso_maiz > peso_chile > peso_tomate, "Error: Orden de pesos incorrecto"
    print("Test orden de importancia: PASO")

def test_cargar_datos():
    """Pruebas de carga de datos"""
    print("\nProbando cargar_datos_cultivos...")
    
    datos = cargar_datos_cultivos()
    
    # Test 1: Estructura basica
    assert isinstance(datos, pd.DataFrame), "Error: Debe retornar DataFrame"
    assert len(datos) > 0, "Error: DataFrame no puede estar vacio"
    print("Test estructura basica: PASO")
    
    # Test 2: Columnas requeridas
    columnas_requeridas = ['Cultivo', 'Latitud', 'Longitud', 'Humedad (%)', 'Elevación (m)']
    for col in columnas_requeridas:
        assert col in datos.columns, f"Error: Falta columna {col}"
    print("Test columnas requeridas: PASO")
    
    # Test 3: Rangos geograficos de Guasave
    lat_min, lat_max = datos['Latitud'].min(), datos['Latitud'].max()
    lon_min, lon_max = datos['Longitud'].min(), datos['Longitud'].max()
    
    assert 25.0 <= lat_min <= 26.0, f"Error: Latitud minima fuera de rango: {lat_min}"
    assert 25.0 <= lat_max <= 26.0, f"Error: Latitud maxima fuera de rango: {lat_max}"
    assert -109.0 <= lon_min <= -108.0, f"Error: Longitud minima fuera de rango: {lon_min}"
    assert -109.0 <= lon_max <= -108.0, f"Error: Longitud maxima fuera de rango: {lon_max}"
    print("Test rangos geograficos: PASO")

def test_funcion_objetivo():
    """Pruebas de funcion objetivo"""
    print("\nProbando funcion_objetivo_sensores...")
    
    # Datos pequenos para prueba
    datos_test = pd.DataFrame({
        'Cultivo': ['Maíz', 'Chile'],
        'Latitud': [25.56, 25.57],
        'Longitud': [-108.47, -108.46],
        'Temperatura (°C)': [25.0, 30.0],
        'Humedad (%)': [20.0, 25.0],
        'Salinidad (dS/m)': [1.0, 2.0],
        'Elevación (m)': [20.0, 30.0]
    })
    
    # Test 1: Retorno valido
    posiciones = np.array([25.56, -108.47, 25.57, -108.46])
    costo = funcion_objetivo_sensores(posiciones, datos_test, n_sensores=2)
    assert isinstance(costo, (int, float, np.number)), "Error: Debe retornar numero"
    assert costo >= 0, f"Error: Costo no puede ser negativo: {costo}"
    print("Test retorno valido: PASO")
    
    # Test 2: Penalizacion por cercania
    posiciones_cercanas = np.array([25.56, -108.47, 25.56, -108.47])  # Mismo lugar
    posiciones_separadas = np.array([25.56, -108.47, 25.58, -108.45])  # Separados
    
    costo_cercanos = funcion_objetivo_sensores(posiciones_cercanas, datos_test, n_sensores=2)
    costo_separados = funcion_objetivo_sensores(posiciones_separadas, datos_test, n_sensores=2)
    
    assert costo_cercanos > costo_separados, "Error: Sensores cercanos deben tener mayor costo"
    print("Test penalizacion cercania: PASO")

def test_pso_inicializacion():
    """Pruebas de inicializacion de PSO"""
    print("\nProbando inicializacion PSOSensores...")
    
    # Datos minimos
    datos_test = pd.DataFrame({
        'Cultivo': ['Maíz', 'Chile', 'Tomate'],
        'Latitud': [25.56, 25.57, 25.58],
        'Longitud': [-108.47, -108.46, -108.45],
        'Temperatura (°C)': [25.0, 30.0, 35.0],
        'Humedad (%)': [20.0, 25.0, 30.0],
        'Salinidad (dS/m)': [1.0, 2.0, 3.0],
        'Elevación (m)': [20.0, 30.0, 40.0]
    })
    
    # Test 1: Creacion basica
    pso = PSOSensores(datos_test, n_sensores=2, n_particulas=5, n_iteraciones=3)
    assert pso.n_sensores == 2, "Error: Numero de sensores incorrecto"
    assert pso.n_particulas == 5, "Error: Numero de particulas incorrecto"
    assert pso.dimensiones == 4, "Error: Dimensiones incorrectas"
    print("Test creacion basica: PASO")
    
    # Test 2: Inicializacion de arrays
    assert pso.posiciones.shape == (5, 4), "Error: Shape posiciones incorrecto"
    assert pso.velocidades.shape == (5, 4), "Error: Shape velocidades incorrecto"
    print("Test inicializacion arrays: PASO")
    
    # Test 3: Limites geograficos
    lat_esperado_min = datos_test['Latitud'].min()
    lat_esperado_max = datos_test['Latitud'].max()
    assert pso.lat_min == lat_esperado_min, "Error: Limite lat min incorrecto"
    assert pso.lat_max == lat_esperado_max, "Error: Limite lat max incorrecto"
    print("Test limites geograficos: PASO")

def test_pso_optimizacion():
    """Prueba basica de optimizacion PSO"""
    print("\nProbando optimizacion PSO...")
    
    # Datos para optimizacion rapida
    np.random.seed(42)  # Para reproducibilidad
    datos_test = pd.DataFrame({
        'Cultivo': ['Maíz'] * 5 + ['Chile'] * 3,
        'Latitud': np.random.uniform(25.55, 25.65, 8),
        'Longitud': np.random.uniform(-108.5, -108.4, 8),
        'Temperatura (°C)': np.random.uniform(20, 35, 8),
        'Humedad (%)': np.random.uniform(15, 35, 8),
        'Salinidad (dS/m)': np.random.uniform(1, 3, 8),
        'Elevación (m)': np.random.uniform(20, 40, 8)
    })
    
    # PSO muy pequeno para prueba rapida
    pso = PSOSensores(datos_test, n_sensores=2, n_particulas=3, n_iteraciones=3)
    resultado = pso.optimizar(verbose=False)
    
    # Test 1: Estructura del resultado
    assert 'sensores_optimos' in resultado, "Error: Falta sensores_optimos"
    assert 'costo_minimo' in resultado, "Error: Falta costo_minimo"
    assert 'historial' in resultado, "Error: Falta historial"
    print("Test estructura resultado: PASO")
    
    # Test 2: Dimensiones correctas
    sensores = resultado['sensores_optimos']
    assert sensores.shape == (2, 2), f"Error: Shape sensores incorrecto: {sensores.shape}"
    print("Test dimensiones resultado: PASO")
    
    # Test 3: Sensores dentro de limites
    lat_min, lat_max = datos_test['Latitud'].min(), datos_test['Latitud'].max()
    lon_min, lon_max = datos_test['Longitud'].min(), datos_test['Longitud'].max()
    
    assert np.all(sensores[:, 0] >= lat_min), "Error: Sensor fuera de limite lat min"
    assert np.all(sensores[:, 0] <= lat_max), "Error: Sensor fuera de limite lat max"
    assert np.all(sensores[:, 1] >= lon_min), "Error: Sensor fuera de limite lon min"
    assert np.all(sensores[:, 1] <= lon_max), "Error: Sensor fuera de limite lon max"
    print("Test sensores dentro de limites: PASO")
    
    # Test 4: Historial de convergencia
    historial = resultado['historial']
    assert len(historial) == 4, f"Error: Historial debe tener 4 elementos, tiene: {len(historial)}"
    assert all(isinstance(x, (int, float, np.number)) for x in historial), "Error: Historial debe ser numerico"
    print("Test historial convergencia: PASO")

def ejecutar_todas_las_pruebas():
    """Ejecutar todas las pruebas simples"""
    print("INICIANDO PRUEBAS UNITARIAS BASICAS")
    print("="*60)
    
    total_tests = 0
    tests_pasados = 0
    
    try:
        test_calcular_distancia()
        tests_pasados += 1
    except Exception as e:
        print(f"test_calcular_distancia FALLO: {e}")
    total_tests += 1
    
    try:
        test_obtener_peso_cultivo()
        tests_pasados += 1
    except Exception as e:
        print(f"test_obtener_peso_cultivo FALLO: {e}")
    total_tests += 1
    
    try:
        test_cargar_datos()
        tests_pasados += 1
    except Exception as e:
        print(f"test_cargar_datos FALLO: {e}")
    total_tests += 1
    
    try:
        test_funcion_objetivo()
        tests_pasados += 1
    except Exception as e:
        print(f"test_funcion_objetivo FALLO: {e}")
    total_tests += 1
    
    try:
        test_pso_inicializacion()
        tests_pasados += 1
    except Exception as e:
        print(f"test_pso_inicializacion FALLO: {e}")
    total_tests += 1
    
    try:
        test_pso_optimizacion()
        tests_pasados += 1
    except Exception as e:
        print(f"test_pso_optimizacion FALLO: {e}")
    total_tests += 1
    
    print("\n" + "="*60)
    print("RESUMEN DE PRUEBAS")
    print("="*60)
    print(f"Pruebas pasadas: {tests_pasados}/{total_tests}")
    print(f"Pruebas fallidas: {total_tests - tests_pasados}/{total_tests}")
    
    if tests_pasados == total_tests:
        print("TODAS LAS PRUEBAS PASARON!")
        return True
    else:
        print("Algunas pruebas fallaron. Revisa el codigo.")
        return False

if __name__ == "__main__":
    ejecutar_todas_las_pruebas()