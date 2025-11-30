package com.detection.entity;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.ArrayList;
import java.util.List;

// Entidad de propietario con datos de contacto
// El campo 'acceso' se marca false automáticamente cuando llega a 3 incidentes
@Entity
@Table(name = "propietarios")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class VehicleOwner {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id_propietario")
    private Long id;
    
    @NotBlank(message = "El nombre no puede estar vacío")
    @Column(name = "nombre", nullable = false, length = 100)
    private String name;
    
    @NotBlank(message = "El email no puede estar vacío")
    @Column(name = "email", nullable = false, length = 100)
    private String email;
    
    @NotBlank(message = "El teléfono no puede estar vacío")
    @Column(name = "telefono", nullable = false, length = 20)
    private String phone;
    
    @Column(name = "acceso", nullable = false, columnDefinition = "TINYINT(1) DEFAULT 1")
    private Boolean acceso = true;
    
    @OneToMany(mappedBy = "owner", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<Vehicle> vehicles = new ArrayList<>();
    
    public VehicleOwner(String name, String email, String phone) {
        this.name = name;
        this.email = email;
        this.phone = phone;
    }
}
