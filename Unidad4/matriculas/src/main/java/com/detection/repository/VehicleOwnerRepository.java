package com.detection.repository;

import com.detection.entity.VehicleOwner;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

// Repo para buscar propietarios de vehículos
// El campo 'acceso' se pone en false cuando tiene 3+ incidentes
@Repository
public interface VehicleOwnerRepository extends JpaRepository<VehicleOwner, Long> {
    
    Optional<VehicleOwner> findByName(String name);
    
    List<VehicleOwner> findByNameContainingIgnoreCase(String name);
}