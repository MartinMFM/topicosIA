# Algoritmo Genético para el Problema del Viajante (TSP)

---

### **Información General**

- **Universidad:** Tecnológico Nacional de México, Campus Culiacán
- **Materia:** Tópicos de Inteligencia Artificial
- **Profesor:** Mora Félix Zuriel Dathan
- **Integrantes:**
  - Dávila Bejarano Víctor Jesús
  - Flores Medina Martin

---

## Descripción del Proyecto

Este proyecto implementa un **Algoritmo Genético (AG)** para resolver el **Problema del Viajante (Traveling Salesman Problem - TSP)**, es uno de los problemas más destacados y estudiados en el campo de la optimización combinatoria.
El objetivo es encontrar la ruta óptima que permita a un agente viajero visitar un conjunto dado de n ciudades, pasando por cada una de ellas exactamente una vez, y regresando finalmente a la ciudad de origen

### ¿Qué es un Algoritmo Genético?

Los algoritmos genéticos son técnicas de optimización inspiradas en la evolución biológica natural. Utilizan conceptos como:

- **Población**: Conjunto de soluciones candidatas (rutas)
- **Selección**: Escoge los mejores individuos para reproducirse
- **Cruzamiento (Crossover)**: Combina dos soluciones para crear nuevas
- **Mutación**: Introduce variaciones aleatorias para mantener diversidad
- **Elitismo**: Preserva las mejores soluciones entre generaciones

### Implementación

El algoritmo utiliza:

- **Operador de Cruzamiento**: Order Crossover (OX) - preserva el orden relativo de las ciudades
- **Operador de Mutación**: Swap Mutation - intercambia aleatoriamente pares de ciudades
- **Selección**: Combinación de elitismo (20% mejores individuos) y selección por ruleta
- **Función de Aptitud**: Inverso de la distancia total del recorrido (menor distancia = mayor aptitud)

## Estructura del Proyecto

```
TareaValidacionAG/
│
├── main.py                      # Punto de entrada principal
├── municipio.py                 # Clase para representar ciudades
├── aptitud.py                   # Cálculo de fitness de rutas
├── operadores_geneticos.py      # Operadores de crossover y mutación
├── seleccion.py                 # Funciones de selección y población
├── algoritmo_genetico.py        # Lógica principal del AG
├── utils.py                     # Utilidades (carga de CSV)
├── generador_reportes.py        # Generación de reportes
├── ciudades.csv                 # Dataset de ciudades con coordenadas
└── README.md                    # Este archivo
```

## Dependencias

Este proyecto requiere Python 3.7 o superior y las siguientes bibliotecas:

```
numpy>=1.19.0
pandas>=1.1.0
```

### Instalación de dependencias

```
pip install numpy pandas
```

## Cómo Ejecutar el Código

### 1. Ejecutar el algoritmo

Desde terminal:

```
python main.py
```

### 2. Personalizar parámetros

Puedes modificar los parámetros del algoritmo editando `main.py`:

```python
mejorRuta = algoritmoGenetico(
    poblacion=ciudades,           # Lista de ciudades
    tamanoPoblacion=100,          # Tamaño de la población
    indivSelecionados=20,         # Individuos elite (20%)
    razonMutacion=0.01,           # Probabilidad de mutación (1%)
    generaciones=500,             # Número de generaciones
    verbose=True                  # Mostrar progreso
)
```

## Salida del Programa

El programa muestra:

1. **Parámetros de configuración** iniciales
2. **Progreso cada 50 generaciones** con distancia actual
3. **Resultados finales**:
   - Distancia inicial
   - Distancia final
   - Porcentaje de mejora
   - Reducción de distancia
4. **Mejor ruta encontrada** con lista de ciudades
5. **Ruta optimizada** en formato visual (A → B → C → ... → A)
6. **Archivo txt con los resultados**
