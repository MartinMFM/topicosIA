@echo off
echo ========================================
echo   Sistema de Deteccion de Matriculas
echo   Spring Boot 3.3.x + Java 21 + MySQL
echo ========================================
echo.

:: Verificar Java 21
echo Verificando Java 21...
java -version 2>&1 | findstr "21" >nul
if %errorlevel% neq 0 (
    echo ERROR: Java 21 no encontrado. Por favor instala Java 21.
    pause
    exit /b 1
)
echo ✓ Java 21 detectado

:: Verificar Maven
echo Verificando Maven...
mvn -version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Maven no encontrado. Por favor instala Maven 3.8+.
    pause
    exit /b 1
)
echo ✓ Maven detectado

:: Verificar MySQL (opcional)
echo Verificando conexion MySQL...
mysql --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ADVERTENCIA: MySQL cliente no encontrado en PATH.
    echo Asegurate de que MySQL Server este ejecutandose.
    echo.
) else (
    echo ✓ MySQL cliente detectado
)

:: Compilar proyecto
echo.
echo Compilando proyecto...
call mvn clean compile
if %errorlevel% neq 0 (
    echo ERROR: Fallo la compilacion del proyecto.
    pause
    exit /b 1
)
echo ✓ Proyecto compilado exitosamente

:: Mostrar opciones
echo.
echo Selecciona el modo de ejecucion:
echo 1. Desarrollo (dev) - Configuracion local
echo 2. Produccion (prod) - Configuracion optimizada
echo 3. Solo compilar y salir
echo.
set /p choice="Ingresa tu opcion (1-3): "

if "%choice%"=="1" (
    echo.
    echo Iniciando en modo DESARROLLO...
    echo API disponible en: http://localhost:8080/api/v1/detection
    echo Actuator en: http://localhost:8080/actuator
    echo.
    call mvn spring-boot:run -Dspring-boot.run.profiles=dev
) else if "%choice%"=="2" (
    echo.
    echo Iniciando en modo PRODUCCION...
    echo Asegurate de configurar las variables de entorno necesarias.
    echo API disponible en: http://localhost:8080/api/v1/detection
    echo.
    call mvn spring-boot:run -Dspring-boot.run.profiles=prod
) else if "%choice%"=="3" (
    echo.
    echo Proyecto compilado. Saliendo...
    echo Para ejecutar manualmente usa:
    echo   mvn spring-boot:run
    pause
    exit /b 0
) else (
    echo Opcion invalida. Saliendo...
    pause
    exit /b 1
)

echo.
echo Aplicacion finalizada.
pause