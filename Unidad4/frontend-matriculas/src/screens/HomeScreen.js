/**
 * Dashboard principal
 * 
 * Muestra acciones rápidas: Detectar Placa y Reportar Vehículo.
 * Incluye saludo con nombre del usuario y botón de logout.
 */

import { Ionicons } from "@expo/vector-icons";
import {
  SafeAreaView,
  ScrollView,
  Text,
  TouchableOpacity,
  View,
} from "react-native";
import Card from "../components/Card";
import useAuthStore from "../store/authStore";

const HomeScreen = ({ navigation }) => {
  const { logout, user } = useAuthStore();

  return (
    <SafeAreaView className="flex-1 bg-gray-50 dark:bg-gray-900">
      <ScrollView className="flex-1 px-6 pt-6">
        <View className="flex-row justify-between items-center mb-8">
          <View>
            <Text className="text-gray-500 dark:text-gray-400 text-sm">
              Bienvenido,
            </Text>
            <Text className="text-2xl font-bold text-gray-900 dark:text-white">
              {user?.name || "Usuario"}
            </Text>
          </View>
          <TouchableOpacity
            onPress={logout}
            className="bg-gray-200 dark:bg-gray-800 p-2 rounded-full"
          >
            <Ionicons name="log-out-outline" size={24} color="#4B5563" />
          </TouchableOpacity>
        </View>

        <Text className="text-lg font-bold text-gray-900 dark:text-white mb-4">
          Acciones Rápidas
        </Text>
        <Card
          title="Detectar Placa"
          subtitle="Escanear placa del vehículo"
          icon="camera"
          color="indigo"
          onPress={() => navigation.navigate("Camera")}
        />
        <Card
          title="Reportar Vehículo"
          subtitle="Reportar incidente con vehículo"
          icon="alert-circle"
          color="red"
          onPress={() => navigation.navigate("ReportIncident")}
        />

        <View className="h-20" />
      </ScrollView>
    </SafeAreaView>
  );
};

export default HomeScreen;
