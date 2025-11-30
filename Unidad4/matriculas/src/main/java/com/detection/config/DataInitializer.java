package com.detection.config;

import com.detection.entity.Vehicle;
import com.detection.entity.VehicleOwner;
import com.detection.repository.VehicleOwnerRepository;
import com.detection.repository.VehicleRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.util.List;


@Component
@RequiredArgsConstructor
public class DataInitializer implements CommandLineRunner {
    
    private final VehicleOwnerRepository vehicleOwnerRepository;
    private final VehicleRepository vehicleRepository;
    
    @Override
    public void run(String... args) throws Exception {
        // Solo inicializar si no hay datos
        if (vehicleOwnerRepository.count() == 0) {
            initializeTestData();
        } else {
        }
    }
    
    private void initializeTestData() {
        // Crear propietarios de ejemplo
        VehicleOwner owner1 = new VehicleOwner(
            "Juan Pérez García", 
            "juan.perez@email.com",
            "(667) 123-4567"
        );
        
        VehicleOwner owner2 = new VehicleOwner(
            "María López Rodríguez", 
            "maria.lopez@email.com",
            "(667) 234-5678"
        );
        
        VehicleOwner owner3 = new VehicleOwner(
            "Carlos Mendoza Silva", 
            "carlos.mendoza@email.com",
            "(667) 345-6789"
        );
        
        VehicleOwner owner4 = new VehicleOwner(
            "Ana Martínez Torres", 
            "ana.martinez@email.com",
            "(667) 456-7890"
        );
        
        // Guardar propietarios
        vehicleOwnerRepository.saveAll(List.of(owner1, owner2, owner3, owner4));
        
        // Crear vehículos de ejemplo (formato: 3 letras - 2 números - 2 números)
        Vehicle vehicle1 = new Vehicle("ABC-12-34", owner1);
        Vehicle vehicle2 = new Vehicle("XYZ-78-90", owner2);
        Vehicle vehicle3 = new Vehicle("DEF-45-67", owner3);
        Vehicle vehicle4 = new Vehicle("GHI-32-10", owner4);
        
        // Guardar vehículos
        vehicleRepository.saveAll(List.of(vehicle1, vehicle2, vehicle3, vehicle4));
        
    }
}
