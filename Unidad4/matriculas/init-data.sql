-- Script de inicialización de datos de prueba
-- Sistema de Detección de Matrículas

USE license_plate_detection_dev;

-- Insertar propietarios de prueba
INSERT INTO propietarios (nombre, email, telefono) VALUES
('Juan Pérez García', 'juan.perez@email.com', '(667) 123-4567'),
('María López Rodríguez', 'maria.lopez@email.com', '(667) 234-5678'),
('Carlos Mendoza Silva', 'carlos.mendoza@email.com', '(667) 345-6789'),
('Ana Martínez Torres', 'ana.martinez@email.com', '(667) 456-7890'),
('Desconocido', 'unknown@system.com', 'N/A');

-- Insertar vehículos de prueba (formato: 3 letras - 2 números - 2 números)
INSERT INTO vehiculos (matricula, propietario_id) VALUES
('ABC-12-34', 1),
('XYZ-78-90', 2),
('DEF-45-67', 3),
('GHI-32-10', 4),
('JKL-65-43', 1),
('NCM-68-10', 2),  -- El OCR detectará: NCM6810
('MUG-13-13', 3);  -- El OCR detectará: MUG1313

-- Insertar usuarios de prueba
INSERT INTO usuarios (nombre, email, password) VALUES
('Usuario Sistema', 'system@detection.com', 'N/A'),
('Admin Test', 'admin@test.com', '$2a$10$dummyhash');

SELECT 'Datos de prueba insertados exitosamente' AS resultado;
