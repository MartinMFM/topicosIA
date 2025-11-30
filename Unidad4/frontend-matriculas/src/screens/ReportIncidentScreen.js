/**
 * Pantalla de reporte de incidentes
 * 
 * Formulario para reportar infracciones con placa, descripción y ubicación GPS.
 * Muestra mapa con posición actual del usuario.
 */

import { Ionicons } from "@expo/vector-icons";
import * as Location from "expo-location";
import { useEffect, useState } from "react";
import {
  KeyboardAvoidingView,
  Platform,
  SafeAreaView,
  ScrollView,
  Text,
  TouchableOpacity,
  View,
} from "react-native";
import MapView, { Marker } from "react-native-maps";
import { reportIncident } from "../api/api";
import Button from "../components/Button";
import Input from "../components/Input";

const ReportIncidentScreen = ({ route, navigation }) => {
  const [plateNumber, setPlateNumber] = useState(route.params?.plate || "");
  const [description, setDescription] = useState("");
  const [location, setLocation] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [region, setRegion] = useState({
    latitude: 37.78825,
    longitude: -122.4324,
    latitudeDelta: 0.0922,
    longitudeDelta: 0.0421,
  });

  useEffect(() => {
    (async () => {
      let { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== "granted") {
        alert("Permiso para acceder a la ubicación denegado");
        return;
      }

      let location = await Location.getCurrentPositionAsync({});
      setLocation(location.coords);
      setRegion({
        latitude: location.coords.latitude,
        longitude: location.coords.longitude,
        latitudeDelta: 0.005,
        longitudeDelta: 0.005,
      });
    })();
  }, []);

  // Envía reporte al backend y maneja respuesta (incluye auto-bloqueo)
  const handleSubmit = async () => {
    if (!plateNumber || !description || !location) {
      alert(
        "Por favor, complete todos los campos y asegúrese de que la ubicación esté establecida."
      );
      return;
    }

    setIsSubmitting(true);
    try {
      const resp = await reportIncident({
        plateNumber,
        description,
        location: {
          latitude: location.latitude,
          longitude: location.longitude,
        },
        timestamp: new Date().toISOString(),
      });

      const body = resp && resp.data ? resp.data : {};
      console.log("reportIncident response:", body);

      const ownerBlocked =
        body.ownerAlreadyBlocked === true ||
        body.ownerAlreadyBlocked === "true" ||
        body.ownerAlreadyBlocked === 1 ||
        body.ownerAlreadyBlocked === "1";

      const success =
        body.success === true ||
        body.success === "true" ||
        body.success === 1 ||
        body.success === "1";

      if (ownerBlocked) {
        alert(
          body.message ||
            "El propietario del vehículo ya tiene el acceso revocado."
        );
        navigation.navigate("Home");
      } else if (success) {
        alert(body.message || "Incidente reportado con éxito!");
        navigation.navigate("Home");
      } else {
        alert((body && body.message) || "Error al reportar el incidente.");
      }
    } catch (_error) {
      alert("Error al reportar el incidente.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <SafeAreaView className="flex-1 bg-gray-50 dark:bg-gray-900">
      <KeyboardAvoidingView
        behavior={Platform.OS === "ios" ? "padding" : "height"}
        className="flex-1"
      >
        <ScrollView className="flex-1">
          <View className="h-64 bg-gray-200 relative">
            <MapView
              style={{ flex: 1 }}
              region={region}
              onRegionChangeComplete={setRegion}
            >
              {location && (
                <Marker
                  coordinate={{
                    latitude: location.latitude,
                    longitude: location.longitude,
                  }}
                  title="Incident Location"
                />
              )}
            </MapView>
            <TouchableOpacity
              onPress={() => navigation.goBack()}
              className="absolute top-12 left-4 bg-white p-2 rounded-full shadow-md"
            >
              <Ionicons name="arrow-back" size={24} color="black" />
            </TouchableOpacity>
          </View>

          <View className="p-6 -mt-6 bg-gray-50 dark:bg-gray-900 rounded-t-3xl flex-1">
            <Text className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
              Reportar Vehículo
            </Text>

            <Input
              label="Placa del Vehículo"
              placeholder="AB-12-345"
              value={plateNumber}
              onChangeText={setPlateNumber}
            />

            <Input
              label="Descripción"
              placeholder="Describe el incidente..."
              value={description}
              onChangeText={setDescription}
              multiline
              numberOfLines={4}
            />

            <View className="mb-6">
              <Text className="text-gray-700 dark:text-gray-300 mb-2 font-medium">
                Ubicación
              </Text>
              <View className="bg-white dark:bg-gray-800 p-4 rounded-lg border border-gray-300 dark:border-gray-600 flex-row items-center">
                <Ionicons name="location" size={20} color="#4F46E5" />
                <Text
                  className="ml-2 text-gray-700 dark:text-gray-300 flex-1"
                  numberOfLines={1}
                >
                  {location
                    ? `${location.latitude.toFixed(
                        4
                      )}, ${location.longitude.toFixed(4)}`
                    : "Obteniendo ubicación..."}
                </Text>
              </View>
            </View>

            <Button
              title="Enviar Reporte"
              onPress={handleSubmit}
              isLoading={isSubmitting}
              variant="danger"
            />
          </View>
        </ScrollView>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
};

export default ReportIncidentScreen;
