/**
 * Pantalla de captura de placas
 * 
 * Solicita permisos de cámara, captura foto en alta calidad,
 * envía al backend para detección y navega a ResultsScreen.
 */

import { Ionicons } from "@expo/vector-icons";
import { CameraView, useCameraPermissions } from "expo-camera";
import { useRef, useState } from "react";
import {
  Dimensions,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { detectPlate } from "../api/api";

const { width, height } = Dimensions.get("window");

const CameraScreen = ({ navigation }) => {
  const [permission, requestPermission] = useCameraPermissions();
  const [isProcessing, setIsProcessing] = useState(false);
  const cameraRef = useRef(null);
  const insets = useSafeAreaInsets();

  if (!permission) {
    // permiso de cámara aún no verificado
    return <View />;
  }

  if (!permission.granted) {
    // permiso de cámara no concedido aún
    return (
      <View className="flex-1 justify-center items-center bg-gray-900 p-6">
        <Text className="text-white text-center mb-4 text-lg">
          Necesitamos tu permiso para mostrar la cámara
        </Text>
        <TouchableOpacity
          onPress={requestPermission}
          className="bg-indigo-600 px-6 py-3 rounded-lg"
        >
          <Text className="text-white font-bold">Conceder Permiso</Text>
        </TouchableOpacity>
      </View>
    );
  }

  /**
   * Captura foto y envía al backend para detección
   * La imagen se envía completa porque YOLO detecta automáticamente la placa
   */
  const takePicture = async () => {
    if (cameraRef.current) {
      try {
        setIsProcessing(true);

        // Capturar foto en máxima calidad
        const photo = await cameraRef.current.takePictureAsync({
          quality: 1.0, 
          skipProcessing: false,
        });

        console.log("Foto capturada:", {
          width: photo.width,
          height: photo.height,
          screenWidth: width,
          screenHeight: height,
        });

        // En lugar de recortar, enviar la imagen completa
        // El modelo YOLO detectará la placa automáticamente
        const formData = new FormData();
        formData.append("image", {
          uri: photo.uri,
          type: "image/jpeg",
          name: "plate.jpg",
        });

        // Call API - El backend ya maneja la normalización y limpieza
        const response = await detectPlate(formData);

        console.log(
          "Detection Response:",
          JSON.stringify(response.data, null, 2)
        );

        setIsProcessing(false);
        navigation.navigate("Results", {
          imageUri: photo.uri,
          results: response.data,
        });
      } catch (error) {
        console.error("Error taking picture or detecting:", error);
        setIsProcessing(false);
        alert("Failed to process image. Please try again.");
      }
    }
  };

  return (
    <View className="flex-1 bg-black">
      <CameraView style={StyleSheet.absoluteFill} ref={cameraRef} facing="back">
        <View className="flex-1 bg-black/50 justify-between">
          <View
            style={{ paddingTop: insets.top + 10 }}
            className="px-4 flex-row justify-between items-center"
          >
            <TouchableOpacity
              onPress={() => navigation.goBack()}
              className="p-2 bg-black/40 rounded-full"
            >
              <Ionicons name="close" size={24} color="white" />
            </TouchableOpacity>
            <Text className="text-white font-bold text-lg">
              Escanea la Placa
            </Text>
            <View style={{ width: 40 }} />
          </View>

          <View
            style={{ paddingBottom: insets.bottom + 20 }}
            className="flex-row justify-center items-center bg-black/50 pt-8"
          >
            <TouchableOpacity
              onPress={takePicture}
              disabled={isProcessing}
              className="w-20 h-20 rounded-full border-4 border-white flex justify-center items-center bg-white/20"
            >
              <View className="w-16 h-16 rounded-full bg-white" />
            </TouchableOpacity>
          </View>
        </View>
      </CameraView>

      {isProcessing && (
        <View className="absolute inset-0 bg-black/70 justify-center items-center z-50">
          <Text className="text-white text-lg font-bold mb-2">
            Procesando...
          </Text>
          <Text className="text-gray-300">Detectando placa</Text>
        </View>
      )}
    </View>
  );
};

export default CameraScreen;
