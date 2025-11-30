-- Script de configuración de base de datos para el Sistema de Detección de Matrículas
-- MySQL 8.0+

-- Crear base de datos para desarrollo
CREATE DATABASE IF NOT EXISTS license_plate_detection_dev 
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;

-- Crear base de datos para producción
CREATE DATABASE IF NOT EXISTS license_plate_detection 
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;

-- Crear usuario para desarrollo
CREATE USER IF NOT EXISTS 'root'@'Sistema Matriculas Dev' IDENTIFIED BY 'dev_password';
GRANT ALL PRIVILEGES ON license_plate_detection_dev.* TO 'root'@'localhost';

-- Crear usuario para producción
CREATE USER IF NOT EXISTS 'prod_user'@'localhost' IDENTIFIED BY 'prod_password';
GRANT ALL PRIVILEGES ON license_plate_detection.* TO 'prod_user'@'localhost';

-- Aplicar privilegios
FLUSH PRIVILEGES;

-- Mostrar bases de datos creadas
SHOW DATABASES LIKE 'license_plate_detection%';

-- Mostrar usuarios creados
SELECT User, Host FROM mysql.user WHERE User IN ('root', 'prod_user');
-- Verificar privilegios
SHOW GRANTS FOR 'root'@'Sistema Matriculas Dev';
SHOW GRANTS FOR 'prod_user'@'localhost';

-- Mensaje de confirmación
SELECT 'Base de datos configurada correctamente para el Sistema de Detección de Matrículas' AS Status;