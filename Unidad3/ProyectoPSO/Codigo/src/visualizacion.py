"""
Módulo para visualización de resultados
"""
import matplotlib.pyplot as plt


def graficar_resultados(historial_convergencia, datos_campo, sensores_optimos, n_sensores):
    """
    Generar visualizaciones de los resultados de optimización PSO
    
    Crea dos gráficas principales para análisis de resultados:
    1. Convergencia del algoritmo PSO a lo largo de las iteraciones
    2. Mapa geográfico con ubicación óptima de sensores y distribución de cultivos
    
    Args:
        historial_convergencia (list): Historia del mejor costo en cada iteración
        datos_campo (pd.DataFrame): Datos de las parcelas
        sensores_optimos (np.ndarray): Coordenadas [lat, lon] de cada sensor
        n_sensores (int): Número de sensores
        
    Note:
        - Gráfica 1: Evolución del costo (función objetivo) vs iteraciones
        - Gráfica 2: Mapa con parcelas coloreadas por cultivo y sensores marcados
        - Colores: Maíz (azul), Chile (cyan), Tomate (verde), Sensores (rojo)
        - Escalas: Coordenadas geográficas reales de Guasave, Sinaloa
    """
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('Optimización PSO: Ubicación de Sensores en Guasave, Sinaloa', fontsize=16)
    
    # 1. Convergencia del PSO
    ax1 = axes[0]
    ax1.plot(historial_convergencia, 'b-', linewidth=2)
    ax1.set_title('Convergencia del Algoritmo PSO')
    ax1.set_xlabel('Iteración')
    ax1.set_ylabel('Costo (Suma de distancias al cuadrado)')
    ax1.grid(True, alpha=0.3)
    
    # 2. Mapa de ubicación óptima de sensores
    ax2 = axes[1]

    # Graficar parcelas por cultivo
    for cultivo in datos_campo['Cultivo'].unique():
        datos_cultivo = datos_campo[datos_campo['Cultivo'] == cultivo]
        
        if cultivo == 'Maíz':
            ax2.scatter(datos_cultivo['Longitud'], datos_cultivo['Latitud'], 
                       c='blue', alpha=0.6, s=30, label='Maíz', marker='o')
        elif cultivo == 'Chile':
            ax2.scatter(datos_cultivo['Longitud'], datos_cultivo['Latitud'], 
                       c='cyan', alpha=0.6, s=30, label='Chile', marker='x')
        else:  # Tomate
            ax2.scatter(datos_cultivo['Longitud'], datos_cultivo['Latitud'], 
                       c='green', alpha=0.6, s=30, label='Tomate', marker='^')
    
    # Graficar sensores óptimos
    sensores = sensores_optimos.reshape(n_sensores, 2)
    ax2.scatter(sensores[:, 1], sensores[:, 0], 
               c='red', s=200, marker='X', edgecolors='black', linewidth=2,
               label='Sensores Óptimos (PSO)', zorder=5)
    
    ax2.set_title('Mapa de Colocación Óptima de Sensores en Guasave')
    ax2.set_xlabel('Longitud')
    ax2.set_ylabel('Latitud')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
