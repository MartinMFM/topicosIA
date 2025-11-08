import os
from datetime import datetime
from aptitud import Aptitud

class GeneradorReportes:
    """Clase para generar reportes de resultados en archivos .txt"""
    
    def __init__(self, carpeta="reportes"):
        self.carpeta = carpeta
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
    
    def crear_reporte(self, mejor_ruta, distancia_inicial, distancia_final):
        """Genera un reporte completo del algoritmo genético"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archivo = os.path.join(self.carpeta, f"reporte_ag_{timestamp}.txt")
        
        mejora = ((distancia_inicial - distancia_final) / distancia_inicial) * 100
        nombres = [c.nombre if c.nombre else str(c) for c in mejor_ruta]
        
        with open(archivo, 'w', encoding='utf-8') as f:
            f.write("REPORTE ALGORITMO GENÉTICO - TSP\n")
            f.write("=" * 40 + "\n")
            f.write(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
            f.write(f"Distancia inicial: {distancia_inicial:.4f}\n")
            f.write(f"Distancia final:   {distancia_final:.4f}\n")
            f.write(f"Mejora obtenida:   {mejora:.2f}%\n\n")
            f.write("MEJOR RUTA ENCONTRADA:\n")
            f.write(" -> ".join(nombres) + f" -> {nombres[0]}\n")
        
        return archivo