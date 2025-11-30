package com.detection.controller;

import com.detection.dto.IncidentRequestDto;
import com.detection.dto.IncidentResponseDto;
import com.detection.service.IncidentService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

// Controller para reportar incidentes
// Al 3er reporte revoca acceso al propietario automáticamente
@RestController
@RequestMapping("/api/v1/incidents")
@CrossOrigin(origins = "*")
@RequiredArgsConstructor
public class IncidentController {
    
    private final IncidentService incidentService;
    
    // POST /report - Reporta incidente (auto-bloquea al 3er reporte)
    @PostMapping("/report")     *       "location": {
     *         "latitude": 19.4326,
     *         "longitude": -99.1332
     *       },
     *       "timestamp": "2025-11-29T10:30:00Z"
     *     }
     * 
     * Response Example (Primer reporte):
     *     {
     *       "success": true,
     *       "message": "Incidente reportado exitosamente (1 reportes totales)",
     *       "ownerBlocked": false,
     *       "totalReports": 1
     *     }
     * 
     * Response Example (Tercer reporte - auto-bloqueo):
     *     {
     *       "success": true,
     *       "message": "Incidente reportado. ALERTA: Acceso revocado al propietario (3 reportes)",
     *       "ownerBlocked": true,
     *       "totalReports": 3
     *     }
     * 
     * Response Example (Propietario ya bloqueado):
     *     {
     *       "success": true,
     *       "message": "Incidente reportado (Propietario ya tenía acceso revocado previamente)",
     *       "ownerAlreadyBlocked": true
     *     }
     */
    @PostMapping("/report")
    public ResponseEntity<IncidentResponseDto> reportIncident(
            @Valid @RequestBody IncidentRequestDto request) {
        
        IncidentResponseDto response = incidentService.reportIncident(request);
        
        // Si el propietario ya estaba bloqueado devolvemos 200 para que el cliente
        // pueda mostrar un mensaje específico en lugar de recibir un error HTTP
        if (Boolean.TRUE.equals(response.getOwnerAlreadyBlocked())) {
            return ResponseEntity.ok(response);
        }

        if (response.isSuccess()) {
            return ResponseEntity.ok(response);
        } else {
            return ResponseEntity.badRequest().body(response);
        }
    }
}
