package com.detection.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

// DTO de respuesta de login/registro
// Incluye success, mensaje y datos del usuario
@Data
@NoArgsConstructor
@AllArgsConstructor
public class LoginResponseDto {
    
    private boolean success;
    private String message;
    private UserData user;
    
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    public static class UserData {
        private Long id;
        private String email;
        private String name;
    }
}
