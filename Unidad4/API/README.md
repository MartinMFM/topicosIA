# API de Detección de Placas Vehiculares

API REST para detectar y reconocer placas vehiculares usando YOLOv8 + EasyOCR.

## 🚀 Despliegue Local con Ngrok

### Paso 1: Instalar Ngrok

```powershell
winget install --id=Ngrok.Ngrok -e
```

### Paso 2: Iniciar la API

```powershell
python app.py
```

La API se ejecutará en `http://localhost:10000`

### Paso 3: Exponer con Ngrok

En otra terminal:

```powershell
ngrok http 10000
```

Ngrok te dará una URL pública como: `https://xxxx-xxxx-xxxx.ngrok-free.app`

**⚠️ Importante:** La URL cambia cada vez que reinicias ngrok.

---

## 📡 Endpoints

### GET /

Información general de la API

**Ejemplo:**

```bash
curl https://0956163272c1.ngrok-free.app/ \
  -H "ngrok-skip-browser-warning: true"
```

### GET /health

Verificar estado de la API

**Ejemplo:**

```bash
curl https://0956163272c1.ngrok-free.app/health \
  -H "ngrok-skip-browser-warning: true"
```

### POST /detect

Detectar y reconocer placas vehiculares

**Parámetros:**

- `image`: archivo de imagen (required)
- `conf`: umbral de confianza 0.0-1.0 (optional, default: 0.25)

**Ejemplo con curl:**

```bash
curl -X POST "https://0956163272c1.ngrok-free.app/detect" \
  -H "ngrok-skip-browser-warning: true" \
  -F "image=@placa.jpg" \
  -F "conf=0.25"
```

**Ejemplo con Postman:**

1. URL: `https://0956163272c1.ngrok-free.app/detect`
2. Method: `POST`
3. Headers:
   - Key: `ngrok-skip-browser-warning`
   - Value: `true`
4. Body → form-data:
   - Key: `image` (File)
   - Key: `conf` (Text) = `0.25`

**Respuesta:**

```json
{
  "success": true,
  "plates": [
    {
      "text": "ABC1234",
      "confidence": 0.92,
      "ocr_confidence": 0.88,
      "bbox": [245, 180, 420, 265]
    }
  ],
  "count": 1
}
```
