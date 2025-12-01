# Frontend — App Matriculas (Unidad 4)

Aplicación móvil construida en React Native con Expoque consume el backend del proyecto para:

- Capturar imagen desde cámara y enviar al backend para detección de placa.
- Mostrar resultados de detección.
- Registrar usuarios y reportar incidentes.

---

Requisitos

- Node.js (16+ recomendado)
- npm o yarn
- Expo CLI (opcional, puedes usar `npx expo`)
- Dispositivo físico con Expo Go o emulador Android/iOS

Instalación

```powershell
# Instalar dependencias
npm install
# o con yarn
# yarn install
```

Ejecutar la app

```powershell
# Iniciar servidor de desarrollo (abrirá Metro / Expo)
npm run start

# Ejecutar en Android conectado/emulador
npm run android

# Ejecutar en iOS (macOS + Xcode)
npm run ios

# Ejecutar en web
npm run web
```

Configuración del backend

Edita `src/api/api.js` para apuntar al backend correcto según tu entorno:

- En desarrollo con dispositivo físico: usa la IP local de tu pc, p.ej. `http://192.168.1.0:8080/api/v1`.
- En emulador Android: `http://10.0.2.2:8080/api/v1`.
- En simulador iOS o web: `http://localhost:8080/api/v1`.
