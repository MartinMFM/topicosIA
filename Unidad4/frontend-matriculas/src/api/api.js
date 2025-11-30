import axios from "axios";

// CONFIGURACIÓN DE LA URL BASE
// Para pruebas en dispositivo físico, usa tu IP local: http://192.168.x.x:8080/api/v1
// Para emulador Android: http://10.0.2.2:8080/api/v1
// Para simulador iOS o web: http://localhost:8080/api/v1
const BASE_URL = __DEV__
  ? "http://192.168.1.6:8080/api/v1" 
  : "https://tu-api-produccion.com/api/v1";

const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 10000, 
});

if (__DEV__) {
  api.interceptors.request.use(
    (config) => {
      console.log("API Request:", config.method?.toUpperCase(), config.url);
      return config;
    },
    (error) => {
      console.error(" API Request Error:", error);
      return Promise.reject(error);
    }
  );

  api.interceptors.response.use(
    (response) => {
      console.log("API Response:", response.status, response.config.url);
      return response;
    },
    (error) => {
      console.error("API Response Error:", error.message);
      if (error.response) {
        console.error("Response data:", error.response.data);
        console.error("Response status:", error.response.status);
      } else if (error.request) {
        console.error("No response received. Check if backend is running.");
      }
      return Promise.reject(error);
    }
  );
}

// Login de usuario
// Envía email y password al backend
// Retorna: { success: boolean, user: {...} }
export const loginUser = async (email, password) => {
  try {
    const response = await api.post("/auth/login", {
      email,
      password,
    });
    return response;
  } catch (error) {
    console.error("Error logging in:", error);
    throw error;
  }
};

// Registro de nuevo usuario
// Retorna: { success: boolean, user: {...} }
export const registerUser = async (name, email, password) => {
  try {
    const response = await api.post("/auth/register", {
      name,
      email,
      password,
    });
    return response;
  } catch (error) {
    console.error("Error registering:", error);
    throw error;
  }
};

// Detección de placa con YOLO + OCR
// Envía imagen al backend que llama a la API Python
// Retorna: { success: true, plates: [{text, owner_info}] }
export const detectPlate = async (formData) => {
  try {
    const response = await api.post("/plates/detect", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response;
  } catch (error) {
    console.error("Error detecting plate:", error);

    // Si hay error de red, devolver respuesta mock para desarrollo
    if (
      __DEV__ &&
      (error.message === "Network Error" || error.code === "ECONNABORTED")
    ) {
      console.warn("Using mock response - Backend not available");
      return {
        data: {
          plate: "ABC-1234",
          confidence: 0.95,
          timestamp: new Date().toISOString(),
        },
      };
    }

    throw error;
  }
};

// Reportar incidente de tráfico
// incidentData: { plateNumber, description, location: {latitude, longitude}, timestamp }
// El backend bloquea automáticamente propietarios con 3+ reportes
export const reportIncident = async (incidentData) => {
  try {
    console.log("Reporting incident:", incidentData);
    const response = await api.post("/incidents/report", incidentData);
    return response;
  } catch (error) {
    console.error("Error reporting incident:", error);
    throw error;
  }
};

export default api;
