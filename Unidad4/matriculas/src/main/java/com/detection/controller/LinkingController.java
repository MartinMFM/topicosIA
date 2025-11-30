package com.detection.controller;

import com.detection.dto.SystemStatsDto;
import com.detection.dto.VehicleDetailsDto;
import com.detection.service.LinkingService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.List;

@RestController
@RequestMapping("/api/v1/detection")
@RequiredArgsConstructor
public class LinkingController {
    
    private final LinkingService linkingService;
    
    // GET /{plateNumber} - Busca detalles del vehículo por placa
    @GetMapping("/{plateNumber}")
    public ResponseEntity<VehicleDetailsDto> getVehicleDetails(
            @PathVariable String plateNumber) {
        
        VehicleDetailsDto vehicleDetails = linkingService.getVehicleDetailsByPlate(plateNumber);
        return ResponseEntity.ok(vehicleDetails);
    }
    
    // GET /owner/{ownerName} - Busca vehículos por nombre del propietario
    @GetMapping("/owner/{ownerName}")
    public ResponseEntity<List<VehicleDetailsDto>> getVehiclesByOwner(
            @PathVariable String ownerName) {
        
        List<VehicleDetailsDto> vehicles = linkingService.getVehiclesByOwner(ownerName);
        return ResponseEntity.ok(vehicles);
    }
    
    // GET /stats - Stats del sistema
    @GetMapping("/stats")
    public ResponseEntity<SystemStatsDto> getSystemStats() {
        SystemStatsDto stats = linkingService.getSystemStats();
        return ResponseEntity.ok(stats);
    }
    
    // GET /health - Health check
    @GetMapping("/health")
    public ResponseEntity<String> health() {
        return ResponseEntity.ok("""
            {
                "status": "UP",
                "service": "Sistema de Detección de Matrículas",
                "version": "1.0.0",
                "timestamp": "%s"
            }
            """.formatted(LocalDateTime.now()));
    }
}
