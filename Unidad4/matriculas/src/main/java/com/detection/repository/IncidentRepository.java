package com.detection.repository;

import com.detection.entity.Incident;
import com.detection.entity.Vehicle;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

// Repo de incidentes
// countByOwnerId cuenta reportes del propietario para auto-bloquearlo si llega a 3+
@Repository
public interface IncidentRepository extends JpaRepository<Incident, Long> {
    
    List<Incident> findByVehicle(Vehicle vehicle);
    
    List<Incident> findByDateBetween(LocalDateTime start, LocalDateTime end);
    
    List<Incident> findByVehiclePlateNumberIgnoreCase(String plateNumber);

    // Cuenta incidentes asociados al propietario del vehículo
    @Query("SELECT COUNT(i) FROM Incident i WHERE i.vehicle.owner.id = :ownerId")
    long countByOwnerId(@Param("ownerId") Long ownerId);
}
