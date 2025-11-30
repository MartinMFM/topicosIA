package com.detection.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;


@Data
@NoArgsConstructor
@AllArgsConstructor
public class VehicleDetailsDto {
    private String plateNumber;
    private String ownerName;
    private String ownerEmail;
    private String ownerPhone;
}
