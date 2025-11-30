package com.detection.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class SystemStatsDto {
    private long totalVehicles;
    private long totalOwners;
}
