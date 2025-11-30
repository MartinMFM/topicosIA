/**
 * Pantalla de resultados de detección
 * 
 * Muestra imagen con placas detectadas e info del propietario.
 * Opciones: reportar, escanear de nuevo, volver al inicio.
 */

import { Ionicons } from "@expo/vector-icons";
import {
  Dimensions,
  Image,
  SafeAreaView,
  ScrollView,
  Text,
  View,
} from "react-native";
import Button from "../components/Button";

const { width } = Dimensions.get("window");

const ResultsScreen = ({ route, navigation }) => {
  const { imageUri, results } = route.params;

  const detectedPlates = results?.plates || [];
  const firstPlate = detectedPlates[0];
  const isRegistered = firstPlate?.owner_info?.is_registered === true;
  const canReport = detectedPlates.length > 0 && isRegistered;

  return (
    <SafeAreaView className="flex-1 bg-gray-900">
      <ScrollView className="flex-1">
        <View className="relative">
          <Image
            source={{ uri: imageUri }}
            style={{ width: width, height: width * 1.33 }}
            resizeMode="contain"
          />
        </View>

        <View className="bg-white dark:bg-gray-800 rounded-t-3xl -mt-6 p-6 flex-1 min-h-[300px]">
          <View className="flex-row justify-center mb-2">
            <View className="w-12 h-1 bg-gray-300 rounded-full" />
          </View>

          <Text className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
            Resultados de la Detección
          </Text>

          {detectedPlates.length > 0 ? (
            detectedPlates.map((plate, index) => (
              <View
                key={index}
                className="bg-gray-50 dark:bg-gray-700 p-4 rounded-xl mb-4 border border-gray-200 dark:border-gray-600"
              >
                <Text className="text-sm text-gray-500 dark:text-gray-400 mb-1">
                  Placa Detectada:
                </Text>
                <Text className="text-3xl font-bold text-indigo-600 dark:text-indigo-400 tracking-widest">
                  {plate.text || plate.plate_number || "N/A"}
                </Text>

                <View className="flex-row items-center mt-2">
                  <Ionicons name="checkmark-circle" size={16} color="#16A34A" />
                  <Text className="text-green-600 ml-1 font-medium">
                    Confianza:{" "}
                    {(
                      (plate.plate_confidence || plate.confidence || 0) * 100
                    ).toFixed(1)}
                    %
                  </Text>
                </View>

                {plate.ocr_confidence && (
                  <Text className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                    OCR: {(plate.ocr_confidence * 100).toFixed(1)}%
                  </Text>
                )}

                {plate.owner_info && (
                  <View className="mt-3 pt-3 border-t border-gray-300 dark:border-gray-600">
                    {plate.owner_info.is_registered ? (
                      <>
                        <View className="flex-row items-center mb-2">
                          <Ionicons
                            name="person-circle"
                            size={18}
                            color="#6366F1"
                          />
                          <Text className="text-sm font-semibold text-gray-700 dark:text-gray-300 ml-2">
                            Información del Propietario
                          </Text>
                        </View>
                        <Text className="text-gray-900 dark:text-white font-medium">
                          {plate.owner_info.name}
                        </Text>
                        <View className="flex-row items-center mt-1">
                          <Ionicons name="mail" size={14} color="#6B7280" />
                          <Text className="text-sm text-gray-600 dark:text-gray-400 ml-2">
                            {plate.owner_info.email}
                          </Text>
                        </View>
                        <View className="flex-row items-center mt-1">
                          <Ionicons name="call" size={14} color="#6B7280" />
                          <Text className="text-sm text-gray-600 dark:text-gray-400 ml-2">
                            {plate.owner_info.phone}
                          </Text>
                        </View>
                      </>
                    ) : (
                      <View className="flex-row items-center">
                        <Ionicons
                          name="alert-circle"
                          size={18}
                          color="#EF4444"
                        />
                        <Text className="text-sm text-red-600 dark:text-red-400 ml-2 font-medium">
                          Vehículo no registrado en la base de datos
                        </Text>
                      </View>
                    )}
                  </View>
                )}
              </View>
            ))
          ) : (
            <View className="items-center py-8">
              <Ionicons name="alert-circle-outline" size={48} color="#EF4444" />
              <Text className="text-gray-900 dark:text-white text-lg font-bold mt-2">
                No se detectaron placas
              </Text>
              <Text className="text-gray-500 text-center mt-1">
                Intenta capturar más cerca o con mejor iluminación.
              </Text>
            </View>
          )}

          <View className="mt-4 space-y-3">
            {detectedPlates.length > 0 && (
              <>
                <Button
                  title={
                    canReport ? "Reportar Vehículo" : "Vehículo no registrado"
                  }
                  onPress={
                    canReport
                      ? () =>
                          navigation.navigate("ReportIncident", {
                            plate: firstPlate?.text || firstPlate?.plate_number,
                          })
                      : undefined
                  }
                  variant="danger"
                  disabled={!canReport}
                />
              </>
            )}
            <Button
              title="Escanear de Nuevo"
              onPress={() => navigation.navigate("Camera")}
              variant="outline"
            />
            <Button
              title="Volver al Inicio"
              onPress={() => navigation.navigate("Home")}
              variant="secondary"
            />
          </View>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

export default ResultsScreen;
