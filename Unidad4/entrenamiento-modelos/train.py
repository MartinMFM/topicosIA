"""
Script para entrenar modelo YOLO de detección de placas vehiculares
"""
from ultralytics import YOLO
import torch
from pathlib import Path

"""
    Función principal para entrenar el modelo YOLOv8
"""
def main():
    # Verificar si hay GPU disponible
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Usando dispositivo: {device}")
    
    # Verificar si existe un checkpoint para reanudar
    checkpoint_path = Path('runs/train/plate_detector/weights/last.pt')
    
    if checkpoint_path.exists():
        print(f"\nCheckpoint encontrado: {checkpoint_path}")
        print("Reanudando entrenamiento desde checkpoint...\n")
        model = YOLO(checkpoint_path)
        resume = True
    else:
        print("\nIniciando entrenamiento desde cero con YOLOv8s\n")
        model = YOLO('yolov8s.pt')
        resume = False
    
    # Entrenar el modelo
    results = model.train(
        data='dataset.yaml',           # Archivo de configuración del dataset
        epochs=50,                     # Número de épocas
        imgsz=640,                      # Tamaño de imagen
        batch=24,                       # Tamaño de batch, se usa 24 por limitación de GPU
        patience=20,                    # Parametro para detener temprano si no hay mejora
        save=True,                      # Guardar checkpoints
        device=device,                  # Selección de dispositivo (GPU o CPU)
        project='runs/train',           # Carpeta donde guardar resultados
        name='plate_detector',          # Nombre del experimento
        exist_ok=True,                  # Sobrescribir si existe
        pretrained=True,                # Usar pesos preentrenados
        optimizer='auto',               # Optimizador automático
        verbose=True,                   # Mostrar progreso detallado
        plots=True,                     # Generar gráficas de entrenamiento
        lr0=0.01,                       # Tasa de aprendizaje inicial
        lrf=0.01,                       # Tasa de aprendizaje final
        momentum=0.937,                 # Momentum SGD
        weight_decay=0.0005,            # Decaimiento de peso (regularización)
        warmup_epochs=3.0,              # Épocas de warmup
        warmup_momentum=0.8,            # Momentum inicial para warmup
        box=7.5,                        # Peso de loss de bounding box
        cls=0.5,                        # Peso de loss de clasificación
        dfl=1.5,                        # Peso de loss de distribución
        augment=True,                   # Usar augmentación de datos
        workers=4,                      # Reducido para ahorrar RAM
        cache=False,                    # No cache
        amp=True,                       # Entrenamiento de precisión mixta
        resume=resume,                  # Reanudar si existe checkpoint
    )
    
    # Mostrar resultados finales
    print("\n" + "="*50)
    print("Entrenamiento completado!")
    print("="*50)
    print(f"Mejor modelo guardado en: {model.trainer.best}")
    print(f"Último modelo guardado en: {model.trainer.last}")
    
    # Validar el modelo
    print("\nValidando modelo...")
    metrics = model.val()
    print(f"\nmAP50: {metrics.box.map50:.4f}")
    print(f"mAP50-95: {metrics.box.map:.4f}")

if __name__ == '__main__':
    main()
