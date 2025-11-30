package com.detection.entity;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

// Entidad de vehículo con placa y propietario
// La placa es única y tiene índice para búsquedas rápidas
@Entity
@Table(name = "vehiculos", 
       indexes = @Index(name = "idx_matricula", columnList = "matricula"))
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Vehicle {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id_vehiculo")
    private Long id;
    
    @NotBlank(message = "La matrícula no puede estar vacía")
    @Column(name = "matricula", nullable = false, unique = true, length = 20)
    private String plateNumber;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "propietario_id", nullable = false)
    private VehicleOwner owner;
    
    public Vehicle(String plateNumber, VehicleOwner owner) {
        this.plateNumber = plateNumber;
        this.owner = owner;
    }
}
