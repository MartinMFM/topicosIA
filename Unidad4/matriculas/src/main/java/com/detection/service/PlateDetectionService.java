package com.detection.service;

import com.detection.dto.PlateDetectionResponseDto;
import com.detection.entity.Vehicle;
import com.detection.repository.VehicleRepository;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;
import java.util.Optional;
import org.springframework.transaction.annotation.Transactional;
import com.fasterxml.jackson.databind.ObjectMapper;

/**
 * Servicio de Detección de Placas
 * 
 * Coordina la detección de placas con la API Python (YOLO + OCR) y busca
 * información del propietario en la base de datos.
 * 
 * Flujo:
 * 1. Recibe imagen del frontend
 * 2. Envía a API Python para detección
 * 3. Limpia y normaliza el texto detectado
 * 4. Busca vehículo en BD (3 estrategias: exacta, normalizada, parcial)
 * 5. Agrega datos del propietario a la respuesta
 */
@Service
public class PlateDetectionService {

    private final RestTemplate restTemplate;
    private final VehicleRepository vehicleRepository;
    
    @Value("${plate-detector.api.url}")
    private String plateDetectorUrl;

    public PlateDetectionService(RestTemplate restTemplate, VehicleRepository vehicleRepository) {
        this.restTemplate = restTemplate;
        this.vehicleRepository = vehicleRepository;
    }

    /**
     * Detecta placa en imagen y agrega info del propietario
     * 
     * Envía imagen a Python API, recibe texto de placa, busca en BD
     * y retorna respuesta con datos del propietario si existe.
     */
    @Transactional(readOnly = true)
    public PlateDetectionResponseDto detectPlate(MultipartFile image) throws IOException {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.MULTIPART_FORM_DATA);

        MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
        body.add("image", new ByteArrayResource(image.getBytes()) {
            @Override
            public String getFilename() {
                return image.getOriginalFilename();
            }
        });

        HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(body, headers);

        String detectUrl = plateDetectorUrl + "/detect";
        
        try {
            // Aceptar respuestas con distintos content-types (application/json o text/plain)
            headers.setAccept(List.of(MediaType.APPLICATION_JSON, MediaType.TEXT_PLAIN, MediaType.ALL));

            ResponseEntity<String> response = restTemplate.postForEntity(
                    detectUrl,
                    requestEntity,
                    String.class
            );

            String responseStr = response.getBody();
            PlateDetectionResponseDto responseBody = null;

            if (responseStr != null && !responseStr.isBlank()) {
                try {
                    ObjectMapper mapper = new ObjectMapper();
                    responseBody = mapper.readValue(responseStr, PlateDetectionResponseDto.class);
                } catch (Exception parseEx) {
                    PlateDetectionResponseDto errorResponse = new PlateDetectionResponseDto();
                    errorResponse.setSuccess(false);
                    errorResponse.setError("Unable to parse detector response: " + parseEx.getMessage());
                    return errorResponse;
                }
            }

            if (responseBody == null) {
                PlateDetectionResponseDto errorResponse = new PlateDetectionResponseDto();
                errorResponse.setSuccess(false);
                errorResponse.setError("Empty response from detector service");
                return errorResponse;
            }

            // Enriquecer la respuesta con información del propietario si existe
            if (responseBody.getPlates() != null && !responseBody.getPlates().isEmpty()) {
                for (PlateDetectionResponseDto.PlateData plate : responseBody.getPlates()) {
                    try {
                        enrichWithOwnerInfo(plate);
                    } catch (Exception ex) {
                        // Registrar y continuar con el siguiente plate
                        System.err.println("Error enriching plate data: " + ex.getMessage());
                        ex.printStackTrace();
                    }
                }
                responseBody.setSuccess(true);
                responseBody.setCount(responseBody.getPlates().size());
            } else {
                responseBody.setSuccess(false);
                responseBody.setCount(0);
                responseBody.setError("No plates detected or processed.");
            }

            return responseBody;
        } catch (Exception e) {
            PlateDetectionResponseDto errorResponse = new PlateDetectionResponseDto();
            errorResponse.setSuccess(false);
            errorResponse.setError("Error connecting to detection service: " + e.getMessage());
            return errorResponse;
        }
    }
    
    /**
     * Enriquece los datos de la placa con información del propietario
     * 
     * Busca el vehículo en la base de datos usando el texto de placa detectado
     * por OCR. Limpia el texto, normaliza el formato y realiza búsquedas con
     * múltiples estrategias para maximizar la probabilidad de encontrar coincidencias.
     * 
     * Args:
     *     plateData: Objeto PlateData con texto de placa detectado por OCR
     * 
     * Side Effects:
     *     - Modifica plateData agregando objeto OwnerInfo
     *     - Actualiza el texto de placa si se limpia/normaliza
     *     - Imprime logs de debug en consola
     * 
     * Note:
     *     Si no se encuentra el vehículo, agrega OwnerInfo con is_registered=false
     */
    private void enrichWithOwnerInfo(PlateDetectionResponseDto.PlateData plateData) {
        if (plateData.getText() == null || plateData.getText().isEmpty()) {
            return;
        }
        
        String detectedPlate = plateData.getText().toUpperCase();
        
        // Limpiar el texto: eliminar caracteres en posiciones 4 y 7 si parecen guiones
        // Ejemplo: "NCMJ68210" → intentar detectar y limpiar caracteres extra
        String cleanedPlate = cleanOCRText(detectedPlate);
        
        System.out.println("Buscando propietario para placa: " + detectedPlate);
        if (!detectedPlate.equals(cleanedPlate)) {
            System.out.println("Placa limpiada: " + detectedPlate + " → " + cleanedPlate);
            plateData.setText(cleanedPlate); // Actualizar el texto en la respuesta
        }
        
        Optional<Vehicle> vehicleOpt = findVehicleByPlate(cleanedPlate);
        
        if (vehicleOpt.isPresent()) {
            Vehicle vehicle = vehicleOpt.get();
            System.out.println("Vehículo encontrado: " + vehicle.getPlateNumber() + " - Propietario: " + vehicle.getOwner().getName());
            
            PlateDetectionResponseDto.OwnerInfo ownerInfo = new PlateDetectionResponseDto.OwnerInfo(
                vehicle.getOwner().getName(),
                vehicle.getOwner().getEmail(),
                vehicle.getOwner().getPhone(),
                true
            );
            plateData.setOwnerInfo(ownerInfo);
        } else {
            System.out.println("No se encontró vehículo para: " + detectedPlate);
            // Placa no registrada
            PlateDetectionResponseDto.OwnerInfo ownerInfo = new PlateDetectionResponseDto.OwnerInfo(
                "No registrado",
                "N/A",
                "N/A",
                false
            );
            plateData.setOwnerInfo(ownerInfo);
        }
        
        System.out.println("Placa detectada: " + plateData.getText());
        System.out.println("Propietario encontrado: " + (plateData.getOwnerInfo() != null ? plateData.getOwnerInfo().getName() : "No registrado"));
    }
    
    /**
     * Busca un vehículo por placa usando múltiples estrategias
     * 
     * Implementa 3 estrategias de búsqueda en orden de especificidad:
     * 1. Búsqueda exacta (case-insensitive)
     * 2. Normalización a formato mexicano ABC-12-34
     * 3. Búsqueda parcial con LIKE para manejar errores de OCR
     * 
     * Esta lógica coincide con IncidentService para consistencia.
     * 
     * Args:
     *     plateNumber: Texto de placa a buscar (puede tener o no guiones)
     * 
     * Returns:
     *     Optional<Vehicle>: Vehículo encontrado, o Optional.empty() si no existe
     * 
     * Example:
     *     findVehicleByPlate("NCM6810") → busca "NCM6810", "NCM-68-10", y "%NCM6810%"
     */
    private Optional<Vehicle> findVehicleByPlate(String plateNumber) {
        System.out.println("Placa detectada: " + plateNumber);
        
        // 1. Buscar sin guiones (tal cual viene)
        System.out.println("   [Intento 1] Búsqueda exacta: " + plateNumber);
        Optional<Vehicle> vehicle = vehicleRepository.findByPlateNumberIgnoreCase(plateNumber);
        if (vehicle.isPresent()) {
            System.out.println(" ENCONTRADO en intento 1!");
            return vehicle;
        }
        System.out.println(" No encontrado");
        
        // 2. Buscar con formato mexicano (ABC-12-34)
        String mexicanFormat = normalizeToMexicanFormat(plateNumber);
        System.out.println("   [Intento 2] Búsqueda normalizada: " + mexicanFormat);
        vehicle = vehicleRepository.findByPlateNumberIgnoreCase(mexicanFormat);
        if (vehicle.isPresent()) {
            System.out.println("ENCONTRADO en intento 2!");
            return vehicle;
        }
        System.out.println("No encontrado");
        
        // 3. Búsqueda parcial
        if (plateNumber.length() >= 4) {
            String cleanPlate = plateNumber.replaceAll("[^A-Z0-9]", "").toUpperCase();
            System.out.println("   [Intento 3] Búsqueda parcial con: " + cleanPlate);
            List<Vehicle> partialMatches = vehicleRepository.findByPlateNumberContaining(cleanPlate);
            System.out.println("   Coincidencias parciales: " + partialMatches.size());
            
            if (!partialMatches.isEmpty()) {
                // Retornar la primera coincidencia
                Vehicle match = partialMatches.get(0);
                System.out.println("ENCONTRADO en intento 3: " + match.getPlateNumber());
                return Optional.of(match);
            }
            System.out.println("No encontrado");
        }
        
        System.out.println("VEHÍCULO NO ENCONTRADO");
        return Optional.empty();
    }
    
    /**
     * Limpia errores comunes de OCR en texto de placas
     * 
     * Corrige detecciones incorrectas donde el OCR interpreta guiones como
     * caracteres adicionales. Si el texto tiene 9+ caracteres, elimina las
     * posiciones 3 y 6 (donde estarían los guiones en formato ABC-12-34).
     * 
     * Args:
     *     text: Texto de placa detectado por OCR
     * 
     * Returns:
     *     String: Texto limpiado sin caracteres espurios
     * 
     * Example:
     *     cleanOCRText("NCMJ68210") → "NCM6810" (elimina posiciones 3 y 6)
     *     cleanOCRText("NCM6810") → "NCM6810" (no modifica, longitud correcta)
     *     cleanOCRText("NCM-68-10") → "NCM6810" (remueve guiones)
     */
    private String cleanOCRText(String text) {
        if (text == null || text.isEmpty()) {
            return text;
        }
        
        // Si tiene 9 caracteres o más, probablemente detectó guiones como caracteres extra
        // Formato esperado: ABC-12-34 (7 alfanuméricos + 2 guiones = 9 caracteres totales)
        if (text.length() >= 9) {
            StringBuilder cleaned = new StringBuilder();
            for (int i = 0; i < text.length(); i++) {
                // Saltar posiciones 3 y 6 (índices donde estarían los guiones)
                if (i != 3 && i != 6) {
                    cleaned.append(text.charAt(i));
                }
            }
            return cleaned.toString();
        }
        
        // Si tiene longitud correcta (7 caracteres), solo remover guiones y caracteres especiales
        return text.replaceAll("[-_|/\\\\]", "");
    }

    /**
     * Normaliza placa al formato mexicano estándar
     * 
     * Convierte placas sin formato (ej. "NCM6810") al formato oficial
     * mexicano con guiones: ABC-12-34 (3 letras - 2 dígitos - 2 dígitos).
     * Útil para estandarizar búsquedas en la base de datos.
     * 
     * Args:
     *     plate: Texto de placa sin formato o con formato inconsistente
     * 
     * Returns:
     *     String: Placa en formato ABC-12-34 si tiene 7+ caracteres alfanuméricos
     * 
     * Example:
     *     normalizeToMexicanFormat("NCM6810") → "NCM-68-10"
     *     normalizeToMexicanFormat("ncm-68-10") → "NCM-68-10"
     *     normalizeToMexicanFormat("ABC") → "ABC" (sin cambios, muy corta)
     */
    private String normalizeToMexicanFormat(String plate) {
        String cleanPlate = plate.replaceAll("[^A-Z0-9]", "").toUpperCase();
        
        if (cleanPlate.length() >= 7) {
            // Formato: 3 letras - 2 números - 2 números
            String letters = cleanPlate.substring(0, 3);
            String firstNumbers = cleanPlate.substring(3, 5);
            String secondNumbers = cleanPlate.substring(5, 7);
            return letters + "-" + firstNumbers + "-" + secondNumbers;
        }
        
        return cleanPlate;
    }
}
