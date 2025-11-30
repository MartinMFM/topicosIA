package com.detection.repository;

import com.detection.entity.Vehicle;
import com.detection.entity.VehicleOwner;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

// Repo para buscar vehículos
// findByPlateNumberContaining elimina guiones/espacios para compensar errores del OCR
@Repository
public interface VehicleRepository extends JpaRepository<Vehicle, Long> {
    
    // Busca vehículo por placa exacta
    Optional<Vehicle> findByPlateNumber(String plateNumber);
    
    Optional<Vehicle> findByPlateNumberIgnoreCase(String plateNumber);
    
    // Busca placas sin guiones ni espacios (para errores de OCR)
    @Query("SELECT v FROM Vehicle v WHERE REPLACE(REPLACE(UPPER(v.plateNumber), '-', ''), ' ', '') LIKE %:platePattern%")
    List<Vehicle> findByPlateNumberContaining(@Param("platePattern") String platePattern);
    
    List<Vehicle> findByOwner(VehicleOwner owner);
}