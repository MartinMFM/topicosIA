// Formulario de registro de usuario
// Valida nombre, email y contraseña antes de crear la cuenta
// Si todo OK, autentica automáticamente y va al home

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

const RegisterScreen = ({ navigation }) => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const { register, isLoading, error } = useAuthStore();

  const handleRegister = async () => {
    await register(name, email, password);
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
              Crear Cuenta
            </Text>
            <Text className="text-gray-500 dark:text-gray-400 mb-8 text-center">
              Regístrate para comenzar
            </Text>

            {error && (
              <View className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
                <Text className="text-red-500">{error}</Text>
              </View>
            )}

            <Input
              label="Nombre"
              placeholder="Tu nombre"
              value={name}
              onChangeText={setName}
            />
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
                title="Regístrate"
                onPress={handleRegister}
                isLoading={isLoading}
              />
            </View>

            <View className="flex-row justify-center mt-6">
              <Text className="text-gray-600 dark:text-gray-400">
                ¿Ya tienes una cuenta?{" "}
              </Text>
              <TouchableOpacity onPress={() => navigation.navigate("Login")}>
                <Text className="text-indigo-600 font-bold">
                  Iniciar Sesión
                </Text>
              </TouchableOpacity>
            </View>
          </View>
        </KeyboardAvoidingView>
      </SafeAreaView>
    </View>
  );
};

export default RegisterScreen;
