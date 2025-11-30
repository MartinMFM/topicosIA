package com.detection.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

// DTO para reportar incidente con placa, descripción y GPS
@Data
@NoArgsConstructor
public class IncidentRequestDto {
    
    @NotBlank(message = "El número de placa es requerido")
    @JsonProperty("plateNumber")
    private String plateNumber;
    
    @NotBlank(message = "La descripción es requerida")
    private String description;
    
    @NotNull(message = "La ubicación es requerida")
    private LocationDto location;
    
    private String timestamp;
    
    
    @Data
    @NoArgsConstructor
    public static class LocationDto {
        @NotNull(message = "La latitud es requerida")
        private Double latitude;
        
        @NotNull(message = "La longitud es requerida")
        private Double longitude;
    }
}
