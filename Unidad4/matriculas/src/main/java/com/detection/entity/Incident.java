package com.detection.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

// Entidad de incidente reportado con GPS y descripción
// Participa en el sistema de auto-bloqueo (3+ incidentes revoca acceso)
@Entity
@Table(name = "incidencias")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Incident {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id_incidencia")
    private Long id;
    
    @Column(name = "fecha", nullable = false)
    private LocalDateTime date;
    
    @Column(name = "descripcion", length = 500)
    private String description;
    
    @Column(name = "longitud", nullable = false)
    private Double longitude;
    
    @Column(name = "latitud", nullable = false)
    private Double latitude;
    
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "vehiculo_id", nullable = false)
    private Vehicle vehicle;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "usuario_reporte_id", nullable = false)
    private User reportingUser;
    
    @PrePersist
    protected void onCreate() {
        if (date == null) {
            date = LocalDateTime.now();
        }
    }
}
