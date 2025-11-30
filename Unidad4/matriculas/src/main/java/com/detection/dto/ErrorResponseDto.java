package com.detection.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class ErrorResponseDto {
    private String message;
    private int status;
    private long timestamp;
    private String path;
    
    public static ErrorResponseDto of(String message, int status, String path) {
        return new ErrorResponseDto(
            message,
            status,
            System.currentTimeMillis(),
            path
        );
    }
}
