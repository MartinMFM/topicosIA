package com.detection.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

// DTO de respuesta al reportar incidente
// Incluye info de auto-bloqueo si el propietario llega a 3 reportes
@Data
@NoArgsConstructor
@AllArgsConstructor
public class IncidentResponseDto {
    private boolean success;
    private String message;
    private IncidentData data;
    private Boolean ownerAlreadyBlocked;
    
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    public static class IncidentData {
        private Long id;
        
        @JsonProperty("plateNumber")
        private String plateNumber;
        
        private String description;
        private Double latitude;
        private Double longitude;
        private LocalDateTime timestamp;
    }

    public IncidentResponseDto(boolean success, String message, IncidentData data) {
        this.success = success;
        this.message = message;
        this.data = data;
    }
}
