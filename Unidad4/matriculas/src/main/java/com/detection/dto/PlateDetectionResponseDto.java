package com.detection.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

// DTO de respuesta con placas detectadas por YOLO+OCR
// Incluye confidence scores y owner_info desde la BD
@Data
@NoArgsConstructor
public class PlateDetectionResponseDto {
    private boolean success;
    private int count;
    private List<PlateData> plates;
    private String error;

    @Data
    @NoArgsConstructor
    public static class PlateData {
        private String text;
        
        @JsonProperty("plate_confidence")
        private Double plateConfidence;
        
        @JsonProperty("numbers_confidence")
        private Double numbersConfidence;
        
        @JsonProperty("ocr_confidence")
        private Double ocrConfidence;
        
        @JsonProperty("plate_bbox")
        private List<Integer> plateBbox;
        
        @JsonProperty("numbers_bbox")
        private List<Integer> numbersBbox;
        
        // Información del propietario si existe en la BD
        @JsonProperty("owner_info")
        private OwnerInfo ownerInfo;
    }
    
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    public static class OwnerInfo {
        private String name;
        private String email;
        private String phone;
        @JsonProperty("is_registered")
        private boolean isRegistered;
    }
}
