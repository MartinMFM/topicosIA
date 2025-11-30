package com.detection.controller;

import com.detection.dto.LoginRequestDto;
import com.detection.dto.LoginResponseDto;
import com.detection.dto.RegisterRequestDto;
import com.detection.service.AuthService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

// Controller de autenticación (login y registro)
@RestController
@RequestMapping("/api/v1/auth")
@CrossOrigin(origins = "*")
public class AuthController {
    
    private final AuthService authService;
    
    public AuthController(AuthService authService) {
        this.authService = authService;
    }
    
    // POST /login - Autentica usuario
    @PostMapping("/login")     * Response Success:
     *     {
     *       "success": true,
     *       "message": "Login exitoso",
     *       "user": {
     *         "id": 1,
     *         "email": "user@example.com",
     *         "name": "Usuario"
     *       }
     *     }
     * 
     * Response Error:
     *     {
     *       "success": false,
     *       "message": "Contraseña incorrecta",
     *       "user": null
     *     }
     */
    @PostMapping("/login")
    public ResponseEntity<LoginResponseDto> login(@Valid @RequestBody LoginRequestDto request) {
        LoginResponseDto response = authService.login(request);
        
        if (response.isSuccess()) {
            return ResponseEntity.ok(response);
        } else {
            return ResponseEntity.status(401).body(response);
        }
    }
    
    /**
     * Endpoint de Registro
     * 
    public ResponseEntity<LoginResponseDto> register(@Valid @RequestBody RegisterRequestDto request) {     
     *         "email": "juan@example.com",
     *         "name": "Juan Pérez"
     *       }
     *     }
     * 
     * Response Error:
     *     {
     *       "success": false,
     *       "message": "El correo ya está registrado",
     *       "user": null
     *     }
     */
    @PostMapping("/register")
    public ResponseEntity<LoginResponseDto> register(@Valid @RequestBody RegisterRequestDto request) {
        LoginResponseDto response = authService.register(request);
        
        if (response.isSuccess()) {
            return ResponseEntity.ok(response);
        } else {
            return ResponseEntity.badRequest().body(response);
        }
    }
}
