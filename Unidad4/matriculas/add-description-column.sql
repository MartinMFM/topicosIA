-- Agregar columna description a la tabla incidents
ALTER TABLE incidents 
ADD COLUMN description VARCHAR(500);

-- Actualizar registros existentes con una descripción por defecto
UPDATE incidents 
SET description = 'Sin descripción' 
WHERE description IS NULL;
