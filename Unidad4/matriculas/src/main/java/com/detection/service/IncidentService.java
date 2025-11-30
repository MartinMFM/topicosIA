package com.detection.service;

import com.detection.dto.IncidentRequestDto;
import com.detection.dto.IncidentResponseDto;
import com.detection.entity.Incident;
import com.detection.entity.User;
import com.detection.entity.Vehicle;
import com.detection.entity.VehicleOwner;
import com.detection.repository.IncidentRepository;
import com.detection.repository.UserRepository;
import com.detection.repository.VehicleOwnerRepository;
import com.detection.repository.VehicleRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.Optional;

/**
 * Servicio de Incidencias
 * 
 * Registra incidentes de tráfico asociados a vehículos.
 * Bloquea automáticamente propietarios con 3+ reportes.
 */
@Service
@RequiredArgsConstructor
@Slf4j
public class IncidentService {
    
    private final IncidentRepository incidentRepository;
    private final VehicleRepository vehicleRepository;
    private final VehicleOwnerRepository vehicleOwnerRepository;
    private final UserRepository userRepository;
    
    /**
     * Registra incidente de tráfico
     * 
     * Crea incidente con ubicación GPS. Si el propietario acumula 3+ reportes,
     * se bloquea automáticamente.
     */
    @Transactional
    public IncidentResponseDto reportIncident(IncidentRequestDto request) {
        try {
            // Normalizar la placa detectada
            String normalizedPlate = normalizePlate(request.getPlateNumber());
            
            // Buscar o crear el vehículo
            Vehicle vehicle = findOrCreateVehicle(normalizedPlate);
            
            User reportingUser = userRepository.findById(1L)
                    .orElseGet(() -> createDefaultUser());
            
            // Parsear timestamp
            LocalDateTime incidentDate;
            if (request.getTimestamp() != null && !request.getTimestamp().isEmpty()) {
                incidentDate = LocalDateTime.parse(request.getTimestamp(), 
                        DateTimeFormatter.ISO_DATE_TIME);
            } else {
                incidentDate = LocalDateTime.now();
            }
            
            // Antes de crear un incidente, verificar si el propietario ya está bloqueado.
            boolean ownerAlreadyBlocked = false;
            if (vehicle != null && vehicle.getOwner() != null && vehicle.getOwner().getId() != null) {
                Long ownerId = vehicle.getOwner().getId();
                Optional<VehicleOwner> maybeOwner = vehicleOwnerRepository.findById(ownerId);
                if (maybeOwner.isPresent()) {
                    VehicleOwner owner = maybeOwner.get();
                    if (Boolean.FALSE.equals(owner.getAcceso())) {
                        // No crear incidente si el propietario ya está bloqueado
                        ownerAlreadyBlocked = true;
                        IncidentResponseDto response = new IncidentResponseDto(
                                false,
                                "El propietario ya tiene el acceso revocado",
                                null
                        );
                        response.setOwnerAlreadyBlocked(true);
                        return response;
                    }
                }
            }

            // Crear el incidente
            Incident incident = new Incident();
            incident.setVehicle(vehicle);
            incident.setReportingUser(reportingUser);
            incident.setDate(incidentDate);
            incident.setDescription(request.getDescription());
            incident.setLatitude(request.getLocation().getLatitude());
            incident.setLongitude(request.getLocation().getLongitude());

            Incident savedIncident = incidentRepository.save(incident);

            // Después de guardar, contar incidentes y bloquear si alcanza 3
            if (vehicle != null && vehicle.getOwner() != null && vehicle.getOwner().getId() != null) {
                Long ownerId = vehicle.getOwner().getId();
                Optional<VehicleOwner> maybeOwner = vehicleOwnerRepository.findById(ownerId);
                if (maybeOwner.isPresent()) {
                    VehicleOwner owner = maybeOwner.get();
                    long reports = incidentRepository.countByOwnerId(ownerId);
                    log.info("Owner id={} reports={}", ownerId, reports);
                    if (reports >= 3 && Boolean.TRUE.equals(owner.getAcceso())) {
                        owner.setAcceso(false);
                        vehicleOwnerRepository.save(owner);
                        log.info("Owner id={} blocked (acceso=false)", ownerId);
                    }
                }
            }
            
            // Construir respuesta
            IncidentResponseDto.IncidentData data = new IncidentResponseDto.IncidentData(
                    savedIncident.getId(),
                    vehicle.getPlateNumber(),
                    savedIncident.getDescription(),
                    savedIncident.getLatitude(),
                    savedIncident.getLongitude(),
                    savedIncident.getDate()
            );
            
                IncidentResponseDto response = new IncidentResponseDto(
                    true,
                    "Incidente reportado exitosamente",
                    data
                );
                response.setOwnerAlreadyBlocked(ownerAlreadyBlocked);
                return response;
            
        } catch (Exception e) {
            return new IncidentResponseDto(
                    false,
                    "Error al reportar incidente: " + e.getMessage(),
                    null
            );
        }
    }
    
    /**
     * Busca un vehículo por placa normalizada o lo crea si no existe
     */
    private Vehicle findOrCreateVehicle(String plateNumber) {
        // 1. Buscar sin guiones
        Optional<Vehicle> vehicle = vehicleRepository.findByPlateNumberIgnoreCase(plateNumber);
        if (vehicle.isPresent()) {
            return vehicle.get();
        }
        
        // 2. Buscar con formato mexicano
        String mexicanFormat = normalizePlate(plateNumber);
        vehicle = vehicleRepository.findByPlateNumberIgnoreCase(mexicanFormat);
        if (vehicle.isPresent()) {
            return vehicle.get();
        }
        
        // 3. Búsqueda parcial
        if (plateNumber.length() >= 4) {
            String cleanPlate = plateNumber.replaceAll("[^A-Z0-9]", "").toUpperCase();
            List<Vehicle> partialMatches = vehicleRepository.findByPlateNumberContaining(cleanPlate);
            
            if (!partialMatches.isEmpty()) {
                // Retornar la primera coincidencia
                return partialMatches.get(0);
            }
        }
        
        // No existe, crear uno nuevo con formato mexicano
        return createUnknownVehicle(mexicanFormat);
    }
    
    /**
     * Normaliza una placa al formato ABC-12-34
     */
    private String normalizePlate(String plate) {
        if (plate == null || plate.isEmpty()) {
            return plate;
        }
        
        String cleanPlate = plate.replaceAll("[^A-Z0-9]", "").toUpperCase();
        
        if (cleanPlate.length() >= 7 && !plate.contains("-")) {
            // Formato: 3 letras - 2 números - 2 números
            String letters = cleanPlate.substring(0, 3);
            String firstNumbers = cleanPlate.substring(3, 5);
            String secondNumbers = cleanPlate.substring(5, 7);
            return letters + "-" + firstNumbers + "-" + secondNumbers;
        }
        
        return plate.toUpperCase();
    }
    
    private Vehicle createUnknownVehicle(String plateNumber) {
        // Crear un propietario desconocido si no existe
        VehicleOwner unknownOwner = vehicleOwnerRepository.findByName("Desconocido")
                .orElseGet(() -> {
                    VehicleOwner owner = new VehicleOwner();
                    owner.setName("Desconocido");
                    owner.setEmail("unknown@system.com");
                    owner.setPhone("N/A");
                    return vehicleOwnerRepository.save(owner);
                });
        
        Vehicle vehicle = new Vehicle();
        vehicle.setPlateNumber(plateNumber.toUpperCase());
        vehicle.setOwner(unknownOwner);
        
        return vehicleRepository.save(vehicle);
    }
    
    private User createDefaultUser() {
        User user = new User();
        user.setName("Usuario Sistema");
        user.setEmail("system@detection.com");
        user.setPassword("N/A");
        return userRepository.save(user);
    }
}
