"""
Script para probar la API actualizada con los dos modelos
"""
import requests
import cv2
import numpy as np

def test_local_api():
    """Prueba la API local con una imagen de prueba"""
    
    # URL de la API local
    api_url = "http://localhost:10000/detect"
    
    # Ruta a una imagen de prueba (ajusta según tu dataset)
    test_image_path = "data/images/test/003a5aaf6d17c917.jpg"
    
    try:
        # Leer imagen
        img = cv2.imread(test_image_path)
        if img is None:
            print(f"❌ No se pudo cargar la imagen: {test_image_path}")
            return
        
        # Codificar imagen como JPEG
        _, img_encoded = cv2.imencode('.jpg', img)
        
        # Preparar petición
        files = {'image': ('test.jpg', img_encoded.tobytes(), 'image/jpeg')}
        data = {'conf': 0.25}
        
        print("Enviando petición a la API...")
        response = requests.post(api_url, files=files, data=data)
        
        # Mostrar resultado
        if response.status_code == 200:
            result = response.json()
            print("\n✅ Respuesta de la API:")
            print(f"Success: {result['success']}")
            print(f"Placas detectadas: {result['count']}")
            
            for i, plate in enumerate(result.get('plates', []), 1):
                print(f"\nPlaca {i}:")
                print(f"  Texto: {plate['text']}")
                print(f"  Confianza placa: {plate['plate_confidence']}")
                print(f"  Confianza números: {plate['numbers_confidence']}")
                print(f"  Confianza OCR: {plate['ocr_confidence']}")
                print(f"  BBox placa: {plate['plate_bbox']}")
                print(f"  BBox números: {plate['numbers_bbox']}")
        else:
            print(f"❌ Error en la API: {response.status_code}")
            print(response.text)
    
    except requests.exceptions.ConnectionError:
        print("❌ No se pudo conectar a la API. Asegúrate de que esté corriendo en http://localhost:10000")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    print("=== Test de API con Dual Model ===\n")
    test_local_api()
