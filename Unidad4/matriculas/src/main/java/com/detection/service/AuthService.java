package com.detection.service;

import com.detection.dto.LoginRequestDto;
import com.detection.dto.LoginResponseDto;
import com.detection.dto.RegisterRequestDto;
import com.detection.entity.User;
import com.detection.repository.UserRepository;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Optional;

/**
 * Servicio de Autenticación
 * 
 * Maneja login y registro de usuarios.
 * Valida credenciales contra la BD.
 */
@Service
public class AuthService {
    
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    public AuthService(UserRepository userRepository, PasswordEncoder passwordEncoder) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
    }

    /**
     * Login de usuario
     * Busca por email (case-insensitive) y valida password
     * Retorna: { success: boolean, message: string, user: {...} }
     */
     */
    public LoginResponseDto login(LoginRequestDto request) {
        try {
            Optional<User> userOpt = userRepository.findByEmailIgnoreCase(request.getEmail());
            
            if (userOpt.isEmpty()) {
                return new LoginResponseDto(false, "Usuario no encontrado", null);
            }
            
            User user = userOpt.get();
            
            // Validar contraseña usando BCrypt
            if (!passwordEncoder.matches(request.getPassword(), user.getPassword())) {
                return new LoginResponseDto(false, "Contraseña incorrecta", null);
            }
            
            // Login exitoso
            LoginResponseDto.UserData userData = new LoginResponseDto.UserData(
                user.getId(),
                user.getEmail(),
                user.getName()
            );
            
            return new LoginResponseDto(true, "Login exitoso", userData);
            
        } catch (Exception e) {
            return new LoginResponseDto(false, "Error al iniciar sesión: " + e.getMessage(), null);
        }
    }
    
    /**
     * Registra un nuevo usuario en el sistema
     * 
     * Crea una nueva cuenta de usuario después de validar que el email
     * no esté registrado previamente. El email se normaliza a minúsculas
     * para consistencia en búsquedas futuras.
     * 
     * Args:
     *     request: RegisterRequestDto con name, email y password
     * 
     * Returns:
     *     LoginResponseDto: Respuesta con resultado del registro
     *         - success: true si registro exitoso, false si email duplicado o error
     *         - message: Mensaje descriptivo del resultado
     *         - user: Datos del usuario registrado si exitoso, null si falla
     * 
     * Transactional:
     *     Operación transaccional para garantizar consistencia de datos
     * 
     * Example:
     *     request = {name: "Juan", email: "juan@example.com", password: "pass123"}
     *     → LoginResponseDto(success=true, message="Registro exitoso", user={...})
     */
    @Transactional
    public LoginResponseDto register(RegisterRequestDto request) {
        try {
            // Verificar si el usuario ya existe
            Optional<User> existingUser = userRepository.findByEmailIgnoreCase(request.getEmail());
            
            if (existingUser.isPresent()) {
                return new LoginResponseDto(false, "El correo ya está registrado", null);
            }
            
            // Crear nuevo usuario
            User newUser = new User();
            newUser.setName(request.getName());
            newUser.setEmail(request.getEmail().toLowerCase());
            // Guardar contraseña encriptada
            newUser.setPassword(passwordEncoder.encode(request.getPassword())); 
            
            User savedUser = userRepository.save(newUser);
            
            // Retornar datos del usuario registrado
            LoginResponseDto.UserData userData = new LoginResponseDto.UserData(
                savedUser.getId(),
                savedUser.getEmail(),
                savedUser.getName()
            );
            
            return new LoginResponseDto(true, "Registro exitoso", userData);
            
        } catch (Exception e) {
            return new LoginResponseDto(false, "Error al registrar usuario: " + e.getMessage(), null);
        }
    }
}
