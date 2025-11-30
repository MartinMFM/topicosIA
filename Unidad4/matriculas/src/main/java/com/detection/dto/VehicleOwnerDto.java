package com.detection.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;


@Data
@NoArgsConstructor
@AllArgsConstructor
public class VehicleOwnerDto {
    private Long id;
    private String name;
    private String email;
    private String phone;
}
