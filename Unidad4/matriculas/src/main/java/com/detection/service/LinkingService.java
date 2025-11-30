package com.detection.service;

import com.detection.dto.SystemStatsDto;
import com.detection.dto.VehicleDetailsDto;
import com.detection.entity.Vehicle;
import com.detection.entity.VehicleOwner;
import com.detection.exception.ResourceNotFoundException;
import com.detection.mapper.VehicleMapper;
import com.detection.repository.VehicleOwnerRepository;
import com.detection.repository.VehicleRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class LinkingService {
    
    private final VehicleRepository vehicleRepository;
    private final VehicleOwnerRepository vehicleOwnerRepository;
    private final VehicleMapper vehicleMapper;
    
    // Busca vehículo por placa usando búsqueda inteligente (exacta, normalizada, parcial)
    public VehicleDetailsDto getVehicleDetailsByPlate(String plateNumber) {
        if (plateNumber == null || plateNumber.trim().isEmpty()) {
            throw new ResourceNotFoundException("La matrícula no puede estar vacía");
        }
        
        System.out.println("LinkingService: Buscando matrícula: " + plateNumber);
        
        // Usa búsqueda inteligente con múltiples estrategias
        Optional<Vehicle> vehicle = findVehicleByPlate(plateNumber.trim());
        
        if (vehicle.isEmpty()) {
            System.out.println("LinkingService: No se encontró la matrícula");
            throw new ResourceNotFoundException("Matrícula no encontrada: " + plateNumber);
        }
        
        System.out.println("LinkingService: Matrícula encontrada: " + vehicle.get().getPlateNumber());
        return vehicleMapper.toDetailsDto(vehicle.get());
    }
    
    /**
     * Busca un vehículo por placa con múltiples estrategias
     * 1. Búsqueda exacta
     * 2. Búsqueda normalizada (ABC6810 -> ABC-68-10)
     * 3. Búsqueda parcial (contiene)
     * 4. Búsqueda fuzzy (tolerante a errores)
     */
    private Optional<Vehicle> findVehicleByPlate(String detectedPlate) {
        String cleanDetected = detectedPlate.replaceAll("[^A-Z0-9]", "").toUpperCase();
        System.out.println("   Placa limpia: " + cleanDetected);
        
        // 1. Búsqueda exacta
        System.out.println("   [Intento 1] Búsqueda exacta: " + detectedPlate);
        Optional<Vehicle> vehicle = vehicleRepository.findByPlateNumberIgnoreCase(detectedPlate);
        if (vehicle.isPresent()) {
            System.out.println("    Encontrado con búsqueda exacta");
            return vehicle;
        }
        
        // 2. Búsqueda normalizada: ABC6810 -> ABC-68-10
        if (cleanDetected.length() >= 7 && !detectedPlate.contains("-")) {
            String normalized = normalizeToMexicanFormat(detectedPlate);
            System.out.println("   [Intento 2] Búsqueda normalizada: " + normalized);
            vehicle = vehicleRepository.findByPlateNumberIgnoreCase(normalized);
            if (vehicle.isPresent()) {
                System.out.println("   Encontrado con búsqueda normalizada");
                return vehicle;
            }
        }
        
        // 3. Búsqueda parcial
        if (cleanDetected.length() >= 4) {
            System.out.println("   [Intento 3] Búsqueda parcial con: " + cleanDetected);
            List<Vehicle> partialMatches = vehicleRepository.findByPlateNumberContaining(cleanDetected);
            System.out.println("   Coincidencias encontradas: " + partialMatches.size());
            
            if (!partialMatches.isEmpty()) {
                Vehicle best = findBestMatch(cleanDetected, partialMatches);
                System.out.println("   Encontrado con búsqueda parcial: " + best.getPlateNumber());
                return Optional.of(best);
            }
        }
        
        // 4. Búsqueda fuzzy (tolerante a errores OCR)
        if (cleanDetected.length() >= 6) {
            System.out.println("   [Intento 4] Búsqueda fuzzy");
            List<Vehicle> allVehicles = vehicleRepository.findAll();
            Vehicle bestMatch = null;
            int minDistance = Integer.MAX_VALUE;
            int threshold = 2;
            
            for (Vehicle candidate : allVehicles) {
                String cleanCandidate = candidate.getPlateNumber().replaceAll("[^A-Z0-9]", "").toUpperCase();
                
                if (Math.abs(cleanCandidate.length() - cleanDetected.length()) <= 1) {
                    int distance = levenshteinDistance(cleanDetected, cleanCandidate);
                    
                    if (distance < minDistance && distance <= threshold) {
                        minDistance = distance;
                        bestMatch = candidate;
                    }
                }
            }
            
            if (bestMatch != null) {
                return Optional.of(bestMatch);
            }
        }
        
        return Optional.empty();
    }
    
    /**
     * Normaliza una placa al formato mexicano ABC-12-34
     */
    private String normalizeToMexicanFormat(String plate) {
        String cleanPlate = plate.replaceAll("[^A-Z0-9]", "").toUpperCase();
        
        if (cleanPlate.length() == 7) {
            return cleanPlate.substring(0, 3) + "-" + 
                   cleanPlate.substring(3, 5) + "-" + 
                   cleanPlate.substring(5, 7);
        }
        
        return plate;
    }
    
    /**
     * Encuentra la mejor coincidencia de una lista
     */
    private Vehicle findBestMatch(String target, List<Vehicle> candidates) {
        return candidates.stream()
            .min((v1, v2) -> {
                String clean1 = v1.getPlateNumber().replaceAll("[^A-Z0-9]", "").toUpperCase();
                String clean2 = v2.getPlateNumber().replaceAll("[^A-Z0-9]", "").toUpperCase();
                
                int dist1 = levenshteinDistance(target, clean1);
                int dist2 = levenshteinDistance(target, clean2);
                
                return Integer.compare(dist1, dist2);
            })
            .orElse(candidates.get(0));
    }
    
    /**
     * Calcula la distancia de Levenshtein entre dos cadenas
     */
    private int levenshteinDistance(String s1, String s2) {
        int[][] dp = new int[s1.length() + 1][s2.length() + 1];
        
        for (int i = 0; i <= s1.length(); i++) {
            for (int j = 0; j <= s2.length(); j++) {
                if (i == 0) {
                    dp[i][j] = j;
                } else if (j == 0) {
                    dp[i][j] = i;
                } else {
                    dp[i][j] = Math.min(
                        dp[i - 1][j - 1] + (s1.charAt(i - 1) == s2.charAt(j - 1) ? 0 : 1),
                        Math.min(dp[i - 1][j] + 1, dp[i][j - 1] + 1)
                    );
                }
            }
        }
        
        return dp[s1.length()][s2.length()];
    }
    
    // Busca vehículos de un propietario por nombre
    public List<VehicleDetailsDto> getVehiclesByOwner(String ownerName) {
        VehicleOwner owner = vehicleOwnerRepository.findByName(ownerName)
            .orElseThrow(() -> new ResourceNotFoundException(
                "Propietario no encontrado: " + ownerName));
        
        return vehicleRepository.findByOwner(owner)
            .stream()
            .map(vehicleMapper::toDetailsDto)
            .toList();
    }
    
    // Stats del sistema (total vehículos y propietarios)
    public SystemStatsDto getSystemStats() {
        long totalVehicles = vehicleRepository.count();
        long totalOwners = vehicleOwnerRepository.count();
        
        return new SystemStatsDto(totalVehicles, totalOwners);
    }
}
