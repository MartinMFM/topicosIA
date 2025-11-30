package com.detection.mapper;

import com.detection.dto.VehicleDetailsDto;
import com.detection.dto.VehicleOwnerDto;
import com.detection.entity.Vehicle;
import com.detection.entity.VehicleOwner;
import org.springframework.stereotype.Component;


@Component
public class VehicleMapper {
    
    // Convierte Vehicle a DTO con datos del propietario
    public VehicleDetailsDto toDetailsDto(Vehicle vehicle) {
        if (vehicle == null) {
            return null;
        }
        
        return new VehicleDetailsDto(
            vehicle.getPlateNumber(),
            vehicle.getOwner().getName(),
            vehicle.getOwner().getEmail(),
            vehicle.getOwner().getPhone()
        );
    }
    
    // Convierte VehicleOwner a DTO
    public VehicleOwnerDto toDto(VehicleOwner owner) {
        if (owner == null) {
            return null;
        }
        
        return new VehicleOwnerDto(
            owner.getId(),
            owner.getName(),
            owner.getEmail(),
            owner.getPhone()
        );
    }
}
