package com.detection.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import lombok.Data;

// DTO para login con email y password
@Data
public class LoginRequestDto {
    
    @NotBlank(message = "El correo es requerido")
    @Email(message = "Debe ser un correo válido")
    private String email;
    
    @NotBlank(message = "La contraseña es requerida")
    private String password;
}
