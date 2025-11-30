from flask import Flask, request, jsonify
from flask_cors import CORS
from ultralytics import YOLO
import easyocr
import cv2
import numpy as np
import re
from PIL import Image
import io
import os

app = Flask(__name__)
CORS(app)

print("Cargando modelos...")

# Asigna las rutas de los modelos ya entrenados
DIRECTORIO_ACTUAL = os.path.dirname(os.path.abspath(__file__))
RUTA_MODELO_PLACA = os.path.join(DIRECTORIO_ACTUAL, 'best.pt')
RUTA_MODELO_NUMEROS = os.path.join(DIRECTORIO_ACTUAL, 'bestNumbers.pt')

print(f"Ruta modelo placas: {RUTA_MODELO_PLACA}")
print(f"Ruta modelo números: {RUTA_MODELO_NUMEROS}")

detector_placas = YOLO(RUTA_MODELO_PLACA)
detector_numeros = YOLO(RUTA_MODELO_NUMEROS)
lector = easyocr.Reader(['en'], gpu=False)
print("✓ Modelos listos")

def preprocesar_para_ocr(imagen):
    """
    Preprocesa la imagen de los números para mejorar OCR.
    Args:
        imagen: Imagen de entrada (numpy array)
    Returns:
        Imagen preprocesada (numpy array)
    """
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    
    # CLAHE para mejorar contraste adaptativo
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    mejorada = clahe.apply(gris)
    
    # Binarización con Otsu
    _, umbral = cv2.threshold(mejorada, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Reducción de ruido con median blur
    sin_ruido = cv2.medianBlur(umbral, 3)
    
    return sin_ruido

"""Limpia el texto OCR conservando solo alfanuméricos
    Args:
    texto: Texto OCR no procesado
    Returns:
        Texto limpio con solo caracteres A-Z y 0-9 y en mayúsculas
"""
def limpiar_texto(texto):
    return re.sub(r'[^A-Z0-9]', '', texto.upper())


# Rutas de la API
@app.route('/', methods=['GET'])
def inicio():
    return jsonify({
        'status': 'ok',
        'message': 'API de Detección de Placas Vehiculares',
        'endpoints': {
            'health': '/health',
            'detect': '/detect (POST)'
        }
    })


@app.route('/health', methods=['GET'])
def estado_salud():
    return jsonify({
        'status': 'ok',
        'message': 'Detector de placas funcionando'
    })

# Endpoint para detección de placas
"""
    Funcion para detectar los números de placas vehiculares en una imagen

    Returns:
        JSON con resultados de detección y OCR
"""
@app.route('/detect', methods=['POST'])
def detectar_placa():
    try:
        if 'image' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No se recibió imagen'
            }), 400
        
        archivo = request.files['image']
        umbral_confianza = float(request.form.get('conf', 0.25)) 
        
        # Leer imagen desde el archivo recibido
        bytes_imagen = archivo.read()
        imagen_pil = Image.open(io.BytesIO(bytes_imagen)).convert('RGB')
        imagen_np = np.array(imagen_pil)
        imagen_cv = cv2.cvtColor(imagen_np, cv2.COLOR_RGB2BGR)
        
        # Paso 1: Detectar placas completas
        detecciones_placas = detector_placas(imagen_cv, conf=umbral_confianza, verbose=False)
        
        lista_placas = []
        
        for deteccion in detecciones_placas:
            cajas = deteccion.boxes
            
            for caja in cajas:
                x1, y1, x2, y2 = map(int, caja.xyxy[0].tolist())
                confianza_placa = float(caja.conf[0].item())
                
                # Recortar placa completa
                recorte_placa = imagen_cv[y1:y2, x1:x2]
                
                if recorte_placa.size == 0:
                    continue
                
                # Redimensionar si es muy pequeña
                alto, ancho = recorte_placa.shape[:2]
                if alto < 50:
                    escala = 50 / alto
                    recorte_placa = cv2.resize(recorte_placa, None, fx=escala, fy=escala)
                
                # Paso 2: Detectar región de números dentro de la placa
                detecciones_numeros = detector_numeros(recorte_placa, conf=0.5, verbose=False)
                
                texto_placa_limpio = ""
                confianza_ocr = 0.0
                caja_numeros = None
                mejor_confianza_numeros = 0.0
                
                # Buscar la detección de números con mayor confianza
                for det_num in detecciones_numeros:
                    cajas_num = det_num.boxes
                    if len(cajas_num) > 0:
                        # Tomar el box con mayor confianza
                        mejor_caja = max(cajas_num, key=lambda b: b.conf[0].item())
                        mejor_confianza_numeros = float(mejor_caja.conf[0].item())
                
                        # Si encontramos región de números, hacer OCR solo en esa región
                        nx1, ny1, nx2, ny2 = map(int, mejor_caja.xyxy[0].tolist())
                        recorte_numeros = recorte_placa[ny1:ny2, nx1:nx2]
                        
                        if recorte_numeros.size > 0:
                            # Redimensionar región de números si es necesaria
                            n_alto, n_ancho = recorte_numeros.shape[:2]
                            if n_alto < 50:
                                escala_num = 50 / n_alto
                                recorte_numeros = cv2.resize(recorte_numeros, None, fx=escala_num, fy=escala_num)
                            
                            try:
                                # Preprocesar y aplicar OCR solo a la región de números
                                numeros_procesados = preprocesar_para_ocr(recorte_numeros)
                                resultados_ocr = lector.readtext(numeros_procesados)
                                
                                if resultados_ocr:
                                    # Tomar el resultado OCR con MAYOR confianza (no promediar)
                                    mejor_ocr = max(resultados_ocr, key=lambda x: x[2])
                                    texto_bruto = mejor_ocr[1]
                                    confianza_ocr = mejor_ocr[2]
                                    texto_placa_limpio = limpiar_texto(texto_bruto)
                                    
                                    # Coordenadas de la región de números en la imagen original
                                    caja_numeros = [x1 + nx1, y1 + ny1, x1 + nx2, y1 + ny2]
                            except Exception as e:
                                print(f"Error en OCR: {e}")
                                texto_placa_limpio = ""
                                confianza_ocr = 0.0
                
                # Solo agregar si se detectó texto
                if texto_placa_limpio:
                    lista_placas.append({
                        'text': texto_placa_limpio,
                        'plate_confidence': round(confianza_placa, 3),
                        'numbers_confidence': round(mejor_confianza_numeros, 3),
                        'ocr_confidence': round(confianza_ocr, 3),
                        'plate_bbox': [x1, y1, x2, y2],
                        'numbers_bbox': caja_numeros
                    })
        
        return jsonify({
            'success': True if lista_placas else False,
            'plates': lista_placas,
            'count': len(lista_placas)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    puerto = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=puerto)