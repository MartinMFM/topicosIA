// Input de texto reutilizable con label opcional
// Muestra borde rojo y mensaje de error si hay problema de validación

import { Text, TextInput, View } from 'react-native';

const Input = ({ label, value, onChangeText, placeholder, secureTextEntry, error }) => {
  return (
    <View className="mb-4">
      {label && <Text className="text-gray-700 dark:text-gray-300 mb-1 font-medium">{label}</Text>}
      <TextInput
        className={`bg-white dark:bg-gray-800 border ${error ? 'border-red-500' : 'border-gray-300 dark:border-gray-600'} rounded-lg px-4 py-3 text-gray-900 dark:text-white`}
        value={value}
        onChangeText={onChangeText}
        placeholder={placeholder}
        placeholderTextColor="#9CA3AF"
        secureTextEntry={secureTextEntry}
      />
      {error && <Text className="text-red-500 text-sm mt-1">{error}</Text>}
    </View>
  );
};

export default Input;
