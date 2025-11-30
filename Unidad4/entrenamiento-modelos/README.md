# Entrenamiento de modelos (Unidad 4)

Repositorio que contiene los scripts para entrenar los modelos de detección de placas vehiculares:

- Detector de placas completas (`train.py`).
- Detector de la región de NÚMEROS dentro de las placas (`train_numbers.py`).
- Archivo de configuración del dataset (`dataset.yaml`).
- Resultados de entrenamiento guardados en `runs/train/` (checkpoints, métricas y gráficas).

---

## Estructura principal

- `train.py` — Script para entrenar el detector de placas (usa `dataset.yaml`).
- `train_numbers.py` — Script para entrenar un detector que localiza sólo la región de números (usa `data/detect_numbers/data.yaml`).
- `runs/train/` — Carpeta donde Ultralytics guarda los experimentos (subcarpetas por `name`, dentro `weights/best.pt`, `last.pt`, imágenes de validación y gráficas).

---

## Requisitos

Recomendado: Python 3.8+ y GPU con CUDA para entrenamientos rápidos.

Instalación de dependencias:

```powershell
# Instalar PyTorch
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# Instalar dependencias
pip install -r requirements.txt
```

## Datasets

- **Detector de placas (placas completas)**

  - Fuente: Kaggle — Large License Plate Dataset
  - URL: https://www.kaggle.com/datasets/fareselmenshawii/large-license-plate-dataset

- **Detector de región de números (sub-región dentro de la placa)**

  - Fuente: Roboflow — Plate Detection Numbers
  - URL: https://app.roboflow.com/platedetectornumbers/plate-detection-qg1vf/1
  - Recomendación: desde la interfaz de Roboflow exporta el dataset en formato YOLOv5/YOLOv8 (ZIP) y descomprímelo en `data/detect_numbers/` o en la ruta que uses en `train_numbers.py`.

---

## Cómo entrenar

1. Entrenar detector de placas:

```powershell
python train.py
```

2. Entrenar detector de números (detecta solo la región de números dentro de la placa):

```powershell
python train_numbers.py
```

## Resultados

Después de cada experimento encontrarás en `runs/train/<name>/`:

- `weights/best.pt` — mejores pesos según métrica (guardar para inferencia).
- `weights/last.pt` — último checkpoint.
- `results.csv`, `results.png`, curvas de loss y métricas (mAP, precisión, recall).
- Imágenes de validación con predicciones (`val_batch*.jpg`) y `labels.jpg`.

---
