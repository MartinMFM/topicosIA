package com.detection.exception;

import com.detection.dto.ErrorResponseDto;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;


@ControllerAdvice
public class GlobalExceptionHandler {
    
    // Maneja 404 cuando no se encuentra un recurso
    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ErrorResponseDto> handleResourceNotFound(
            ResourceNotFoundException ex,
            HttpServletRequest request) {
        
        ErrorResponseDto error = ErrorResponseDto.of(
            ex.getMessage(),
            404,
            request.getRequestURI()
        );
        
        return ResponseEntity.status(404).body(error);
    }
    
    // Maneja 400 cuando hay errores de validación
    @ExceptionHandler(jakarta.validation.ConstraintViolationException.class)
    public ResponseEntity<ErrorResponseDto> handleValidationError(
            jakarta.validation.ConstraintViolationException ex,
            HttpServletRequest request) {
        
        ErrorResponseDto error = ErrorResponseDto.of(
            "Error de validación: " + ex.getMessage(),
            400,
            request.getRequestURI()
        );
        
        return ResponseEntity.status(400).body(error);
    }
    
    // Maneja 500 para errores no contemplados
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponseDto> handleGenericError(
            Exception ex,
            HttpServletRequest request) {
        
        ErrorResponseDto error = ErrorResponseDto.of(
            "Error interno del servidor: " + ex.getMessage(),
            500,
            request.getRequestURI()
        );
        
        return ResponseEntity.status(500).body(error);
    }
}
