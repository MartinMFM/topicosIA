"""
Script para entrenar modelo YOLO de detección de NÚMEROS en placas
Este modelo detecta solo la región de números, no toda la placa
"""
from ultralytics import YOLO
import torch

"""
    Función principal para entrenar el modelo YOLOv8 para detección de números en placas,
    detecta solo el area de los números, para aislar los distractores comunes en las placas,
    como logos, nombres de estados, etc.
"""
def train_plate_numbers_detector():
    print(f"CUDA disponible: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")
    
    print("\nCargando modelo YOLOv8s...")
    model = YOLO('yolov8s.pt')
    
    print("\nIniciando entrenamiento...")
    results = model.train(
        data='data/detect_numbers/data.yaml',
        epochs=100, # Número de épocas
        imgsz=640, # Tamaño de imagen
        batch=16, # Imágenes por lote
        device='cuda:0', # Usa la gpu 0
        workers=4, # Número de hilos para carga de datos
        project='runs/train', # Carpeta de resultados
        name='plate_numbers_detector', # Nombre del experimento
        amp=True, # Entrenamiento de precisión mixta
        patience=15, # Detiene el entreno temprano si no hay mejora
        save=True, # Guardar modelos
        save_period=10, # Guardar cada 10 épocas
        hsv_h=0.015, # Ajuste de color en el canal H
        hsv_s=0.7, # Ajuste de color en el canal S
        hsv_v=0.4, # Ajuste de color en el canal V
        degrees=5, # Rotación en grados
        translate=0.1, # Traslación
        scale=0.2, # Escalado
        flipud=0.0, # Volteo vertical
        fliplr=0.5, # Volteo horizontal
        mosaic=1.0, # Uso de mosaico
        dropout=0.0, # Dropout por si hay mucho overfitting
        val=True, # Validación durante el entrenamiento
        plots=True, # Generar gráficas de entrenamiento
        verbose=True # Mostrar información durante el entrenamiento
    )
    
    print("\n" + "="*60)
    print("Entrenamiento completado!")
    print("="*60)
    print(f"Mejor modelo guardado en: runs/train/plate_numbers_detector/weights/best.pt")
    print(f"Último modelo guardado en: runs/train/plate_numbers_detector/weights/last.pt")
    
    print("\nValidando modelo...")
    metrics = model.val()
    
    print("\n" + "="*60)
    print("MÉTRICAS DEL MODELO:")
    print("="*60)
    print(f"mAP50: {metrics.box.map50:.4f}")
    print(f"mAP50-95: {metrics.box.map:.4f}")
    print(f"Precision: {metrics.box.mp:.4f}")
    print(f"Recall: {metrics.box.mr:.4f}")
    
    return model


if __name__ == '__main__':
    model = train_plate_numbers_detector()
   