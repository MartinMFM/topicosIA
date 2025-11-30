package com.detection;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;


@SpringBootApplication
public class Application {
    
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
        System.out.println("""
             Sistema de Detección de Matrículas iniciado correctamente
             API disponible en: http://localhost:8080/api/v1/detection
             Actuator en: http://localhost:8080/actuator
              Modo de desarrollo activo
            """);
    }
}
