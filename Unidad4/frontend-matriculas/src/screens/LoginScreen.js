/**
 * Pantalla de login
 * 
 * Formulario de inicio de sesión con email y password.
 * Maneja estados de carga y errores.
 */

import { useState } from "react";
import {
  KeyboardAvoidingView,
  Platform,
  SafeAreaView,
  Text,
  TouchableOpacity,
  View,
} from "react-native";
import Button from "../components/Button";
import Input from "../components/Input";
import useAuthStore from "../store/authStore";

const LoginScreen = ({ navigation }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const { login, isLoading, error } = useAuthStore();

  const handleLogin = async () => {
    await login(email, password);
  };

  return (
    <View className="flex-1 bg-indigo-600">
      <SafeAreaView className="flex-1">
        <KeyboardAvoidingView
          behavior={Platform.OS === "ios" ? "padding" : "height"}
          className="flex-1 justify-center px-6"
        >
          <View className="bg-white dark:bg-gray-900 p-8 rounded-2xl shadow-xl">
            <Text className="text-3xl font-bold text-gray-900 dark:text-white mb-2 text-center">
              Bienvenido
            </Text>
            <Text className="text-gray-500 dark:text-gray-400 mb-8 text-center">
              Inicia sesión para continuar
            </Text>

            {error && (
              <View className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
                <Text className="text-red-500">{error}</Text>
              </View>
            )}

            <Input
              label="Correo Electrónico"
              placeholder="nombre@ejemplo.com"
              value={email}
              onChangeText={setEmail}
            />
            <Input
              label="Contraseña"
              placeholder="••••••••"
              secureTextEntry
              value={password}
              onChangeText={setPassword}
            />

            <View className="mt-6">
              <Button
                title="Iniciar Sesión"
                onPress={handleLogin}
                isLoading={isLoading}
              />
            </View>

            <View className="flex-row justify-center mt-6">
              <Text className="text-gray-600 dark:text-gray-400">
                ¿No tienes una cuenta?{" "}
              </Text>
              <TouchableOpacity onPress={() => navigation.navigate("Register")}>
                <Text className="text-indigo-600 font-bold">Regístrate</Text>
              </TouchableOpacity>
            </View>
          </View>
        </KeyboardAvoidingView>
      </SafeAreaView>
    </View>
  );
};

export default LoginScreen;
