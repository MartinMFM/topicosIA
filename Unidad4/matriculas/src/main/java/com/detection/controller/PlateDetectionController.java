package com.detection.controller;

import com.detection.dto.PlateDetectionResponseDto;
import com.detection.service.PlateDetectionService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;

// Controller para detección de placas
// Recibe imagen y la envía a la API Python (YOLO + OCR)
@RestController
@RequestMapping("/api/v1/plates")
@CrossOrigin(origins = "*")
public class PlateDetectionController {

    private final PlateDetectionService plateDetectionService;

    public PlateDetectionController(PlateDetectionService plateDetectionService) {
        this.plateDetectionService = plateDetectionService;
    }

    /**
     * POST /detect - Detecta placa en imagen
     * 
     * Recibe una imagen, la envía a la API Python (YOLO + OCR) y retorna las placas detectadas
     * con información del propietario si está registrado en la base de datos.
     * 
     * @param image archivo de imagen (JPG, PNG, etc.)
     * @return PlateDetectionResponseDto con las placas detectadas y sus propietarios
     * 
     * Ejemplo de respuesta:
     * {
     *   "success": true,
     *   "plates": [{
     *     "plate_number": "NCM-68-10",
     *     "confidence": 0.95,
     *     "owner_info": {
     *       "is_registered": true,
     *       "name": "Juan Pérez",
     *       "email": "juan@example.com",
     *       "phone": "+52 55 1234 5678"
     *     }
     *   }],
     *   "count": 1
     * }
     */
    @PostMapping("/detect")
    public ResponseEntity<PlateDetectionResponseDto> detectPlate(@RequestParam("image") MultipartFile image) {
        try {
            if (image.isEmpty()) {
                PlateDetectionResponseDto response = new PlateDetectionResponseDto();
                response.setSuccess(false);
                response.setError("No image provided");
                return ResponseEntity.badRequest().body(response);
            }

            PlateDetectionResponseDto response = plateDetectionService.detectPlate(image);
            return ResponseEntity.ok(response);
        } catch (IOException e) {
            PlateDetectionResponseDto response = new PlateDetectionResponseDto();
            response.setSuccess(false);
            response.setError("Error processing image: " + e.getMessage());
            return ResponseEntity.internalServerError().body(response);
        }
    }
}
