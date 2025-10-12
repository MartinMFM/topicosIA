import pandas as pd
import folium
import numpy as np
import re
import config
from scipy.spatial.distance import cdist

class GeneradorMapaRutasOptimizadas:
    def __init__(self):
        self.datos_df = None
        self.centros_distribucion = None
        self.tiendas = None
        self.mapa = None
        self.rutas_optimizadas = {}
        self.costo_total = 0
        
        self.colores_zonas = [
            'red', 'blue', 'green', 'purple', 'orange', 
            'darkred', 'magenta', 'darkviolet', 'navy', 'forestgreen'
        ]

    # Cargar datos desde archivo Excel
    def cargar_datos(self): 
        print("Cargando datos de ubicaciones...")
        try:
            self.datos_df = pd.read_excel('datos_distribucion_tiendas.xlsx')
            
            self.centros_distribucion = self.datos_df[
                self.datos_df['Tipo'] == 'Centro de Distribución'
            ].copy().reset_index(drop=True)
            
            self.tiendas = self.datos_df[
                self.datos_df['Tipo'] == 'Tienda'
            ].copy().reset_index(drop=True)
            
            print(f"Datos cargados: {len(self.datos_df)} ubicaciones")
            print(f"Centros de distribución: {len(self.centros_distribucion)}")
            print(f"Tiendas: {len(self.tiendas)}")
            return True
        except FileNotFoundError:
            return False
    
    # Parsear resultados del archivo de texto
    def parsear_resultados_optimizacion(self):
        archivo_resultados = 'resultados_optimizacion_zonas.txt'
        try:
            with open(archivo_resultados, 'r', encoding='utf-8') as file:
                contenido = file.read()
            
            match_costo = re.search(r'COSTO TOTAL:\s*([\d.]+)', contenido)
            if match_costo:
                self.costo_total = float(match_costo.group(1))
            
            zonas = re.findall(r'ZONA: (.*?)\nTiendas: (\d+)\nCosto: ([\d.]+)\nCapacidad: ([\d,]+)\nRuta: (.*?)(?=\n--)', contenido, re.DOTALL)
            
            for i, (centro, num_tiendas, costo, capacidad, ruta) in enumerate(zonas):
                ruta_limpia = ruta.replace('\n', ' ').strip()
                tiendas_en_ruta = re.findall(r'Tienda (\d+)', ruta_limpia)
                
                self.rutas_optimizadas[i] = {
                    'centro': centro,
                    'num_tiendas': int(num_tiendas),
                    'costo': float(costo),
                    'capacidad': int(capacidad.replace(',', '')),
                    'ruta_completa': ruta_limpia,
                    'tiendas': [int(t) for t in tiendas_en_ruta]
                }
            
            print(f"Costo total: {self.costo_total:.2f}")
            return True
            
        except FileNotFoundError:
            return False
        except Exception as e:
            return False
    
    def crear_mapa_base(self):
        lat_centro = self.datos_df['Latitud_WGS84'].mean() 
        lon_centro = self.datos_df['Longitud_WGS84'].mean()
        
        # Crear mapa base centrado en la media de las ubicaciones
        self.mapa = folium.Map(
            location=[lat_centro, lon_centro], 
            zoom_start=10,
            tiles='OpenStreetMap'
        )
        title_html = '''
        <h3 align="center" style="font-size:20px"><b>Mapa de Rutas Optimizadas</b></h3>
        <h4 align="center" style="font-size:16px">Costo Total: {:.2f}</h4>
        '''.format(self.costo_total)
        self.mapa.get_root().html.add_child(folium.Element(title_html))
    
    def agregar_centros_distribucion(self):
        """Agregar marcadores para centros de distribución"""
        for idx, centro in self.centros_distribucion.iterrows():
            zona_info = self.rutas_optimizadas.get(idx, {})
            
            popup_text = f"""
            <b>{centro['Nombre']}</b><br>
            Centro de Distribución<br>
            Capacidad Almacén: {centro['Capacidad_Almacenamiento']}<br>
            <hr>
            <b>Optimización:</b><br>
            Tiendas asignadas: {zona_info.get('num_tiendas', 0)}<br>
            Costo de ruta: {zona_info.get('costo', 0):.2f}<br>
            Capacidad utilizada: {zona_info.get('capacidad', 0):,}
            """
            
            folium.Marker(
                location=[centro['Latitud_WGS84'], centro['Longitud_WGS84']],
                popup=popup_text,
                tooltip=f"Centro {centro['Nombre']} - Costo: {zona_info.get('costo', 0):.2f}",
                icon=folium.Icon(color='black', icon='warehouse', prefix='fa')
            ).add_to(self.mapa)
    
    def agregar_tiendas_y_rutas(self):
        for zona_id, zona_info in self.rutas_optimizadas.items(): 
            if zona_id >= len(self.centros_distribucion):
                continue
                
            color_zona = self.colores_zonas[zona_id % len(self.colores_zonas)]
            centro = self.centros_distribucion.iloc[zona_id]
            
            coord_centro = [centro['Latitud_WGS84'], centro['Longitud_WGS84']]
            
            coordenadas_ruta = [coord_centro]
            tiendas_encontradas = 0
            
            for orden, tienda_id in enumerate(zona_info['tiendas']):
                tienda = self.tiendas[
                    self.tiendas['Nombre'].str.contains(f'Tienda {tienda_id}', na=False)
                ]
                
                if not tienda.empty:
                    tienda = tienda.iloc[0]
                    coord_tienda = [tienda['Latitud_WGS84'], tienda['Longitud_WGS84']]
                    coordenadas_ruta.append(coord_tienda)
                    tiendas_encontradas += 1
                    
                    popup_text = f"""
                    <b>{tienda['Nombre']}</b><br>
                    Zona {zona_id + 1} - Orden: {orden + 1}<br>
                    Nivel: {tienda['Nivel_Tienda']}<br>
                    Capacidad Venta: {tienda['Capacidad_Venta']}<br>
                    Costo de zona: {zona_info['costo']:.2f}
                    """
                    
                    folium.CircleMarker(
                        location=coord_tienda,
                        radius=10,
                        popup=popup_text,
                        tooltip=f"Tienda {tienda_id} (Orden: {orden + 1})",
                        color='black',
                        fillColor=color_zona,
                        fillOpacity=0.9,
                        weight=2
                    ).add_to(self.mapa)
                    
                    folium.Marker(
                        location=coord_tienda,
                        icon=folium.DivIcon(
                            html=f'<div style="font-size: 14px; color: white; font-weight: bold; background-color: {color_zona}; border-radius: 50%; width: 20px; height: 20px; text-align: center; line-height: 20px;">{orden + 1}</div>',
                            icon_size=(20, 20),
                            icon_anchor=(10, 10)
                        )
                    ).add_to(self.mapa)
            
            coordenadas_ruta.append(coord_centro)
            
            if len(coordenadas_ruta) >= 3:
                ruta_principal = folium.PolyLine(
                    locations=coordenadas_ruta,
                    color='black',
                    weight=8,
                    opacity=1.0
                )
                ruta_principal.add_to(self.mapa)
                ruta_color = folium.PolyLine(
                    locations=coordenadas_ruta,
                    color=color_zona,
                    weight=6,
                    opacity=0.9,
                    popup=f"Ruta Zona {zona_id + 1}<br>Centro: {centro['Nombre']}<br>Tiendas: {tiendas_encontradas}<br>Costo: {zona_info['costo']:.2f}",
                    tooltip=f"Ruta Zona {zona_id + 1} - Costo: {zona_info['costo']:.2f}"
                )
                ruta_color.add_to(self.mapa)
                
                for i in range(len(coordenadas_ruta) - 1):
                    folium.PolyLine(
                        locations=[coordenadas_ruta[i], coordenadas_ruta[i + 1]],
                        color='black',
                        weight=6,
                        opacity=0.8
                    ).add_to(self.mapa)
                    
                    folium.PolyLine(
                        locations=[coordenadas_ruta[i], coordenadas_ruta[i + 1]],
                        color=color_zona,
                        weight=4,
                        opacity=0.9,
                        dash_array='10, 5'
                    ).add_to(self.mapa)
                
                self.agregar_flechas_direccionales(coordenadas_ruta, color_zona)
    
    def agregar_flechas_direccionales(self, coordenadas, color):
        for i in range(1, len(coordenadas) - 1, 3):
            if i + 1 < len(coordenadas):
                lat_medio = (coordenadas[i][0] + coordenadas[i + 1][0]) / 2
                lon_medio = (coordenadas[i][1] + coordenadas[i + 1][1]) / 2
                
                lat_diff = coordenadas[i + 1][0] - coordenadas[i][0]
                lon_diff = coordenadas[i + 1][1] - coordenadas[i][1]
                angle = np.arctan2(lat_diff, lon_diff) * 180 / np.pi + 90
                
                folium.Marker(
                    location=[lat_medio, lon_medio],
                    icon=folium.DivIcon(
                        html=f'''
                        <div style="
                            transform: rotate({angle}deg); 
                            color: {color}; 
                            font-size: 24px; 
                            font-weight: bold;
                            text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
                            filter: drop-shadow(1px 1px 2px black);
                        ">▶</div>
                        ''',
                        icon_size=(24, 24),
                        icon_anchor=(12, 12)
                    )
                ).add_to(self.mapa)
    
    def agregar_leyenda_y_controles(self):
        legend_html = f'''
        <div style="position: fixed; 
                    bottom: 50px; left: 50px; width: 280px; height: 220px; 
                    background-color: white; border:2px solid grey; z-index:9999; 
                    font-size:12px; padding: 15px; box-shadow: 0 0 15px rgba(0,0,0,0.5);
                    ">
        <p><b> Mapa de Rutas Optimizadas</b></p>
        <p><i class="fa fa-warehouse" style="color:black; font-size:16px;"></i> Centros de Distribución</p>
        <p><i class="fa fa-circle" style="color:red; font-size:12px;"></i> Tiendas (numeradas por orden)</p>
        <p><b> Costo Total: {self.costo_total:.2f}</b></p>
        <hr>
        <p> <b>Características:</b></p>
        <p>• Líneas gruesas: rutas principales</p>
        <p>• Líneas punteadas: segmentos individuales</p>
        <p>• Números: orden de visita</p>
        <p>• Colores: diferentes zonas</p>
        <p>• Flechas: dirección de la ruta</p>
        </div>
        '''
        self.mapa.get_root().html.add_child(folium.Element(legend_html))
    
    def agregar_estadisticas(self):
        estadisticas_html = f'''
        <div style="position: fixed; 
                    top: 50px; right: 50px; width: 300px; height: 400px; 
                    background-color: white; border:2px solid grey; z-index:9999; 
                    font-size:11px; padding: 10px; overflow-y: auto;
                    ">
        <p><b>Estadísticas de Optimización</b></p>
        <p><b>Costo Total: {self.costo_total:.2f}</b></p>
        <hr>
        '''
        
        for zona_id, zona_info in self.rutas_optimizadas.items():
            estadisticas_html += f'''
            <p><b>Zona {zona_id + 1}: {zona_info['centro']}</b></p>
            <p>• Tiendas: {zona_info['num_tiendas']}</p>
            <p>• Costo: {zona_info['costo']:.2f}</p>
            <p>• Capacidad: {zona_info['capacidad']:,}</p>
            <hr>
            '''
        
        estadisticas_html += '</div>'
        self.mapa.get_root().html.add_child(folium.Element(estadisticas_html))
    
    def generar_mapa_completo(self):
        print("=== GENERANDO MAPA DE RUTAS OPTIMIZADAS ===")
        
        if not self.cargar_datos():
            return False
        
        if not self.parsear_resultados_optimizacion():
            return False
        
        self.crear_mapa_base()
        self.agregar_centros_distribucion()
        self.agregar_tiendas_y_rutas()
        self.agregar_leyenda_y_controles()
        self.agregar_estadisticas()
        
        nombre_archivo = 'mapa_rutas_optimizadas.html'
        self.mapa.save(nombre_archivo)
        print(f"Mapa de rutas optimizadas guardado como: {nombre_archivo}")
        
        return True

def main():
    generador = GeneradorMapaRutasOptimizadas()
    generador.generar_mapa_completo()

if __name__ == "__main__":
    main()