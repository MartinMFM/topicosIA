// Tarjeta con icono y texto para acciones del home
// Tiene variantes de color (indigo, red, green, blue)

import { Ionicons } from '@expo/vector-icons';
import { Text, TouchableOpacity, View } from 'react-native';

const Card = ({ title, subtitle, icon, onPress, color = 'indigo' }) => {
  const colorVariants = {
    indigo: 'bg-indigo-100 text-indigo-600',
    red: 'bg-red-100 text-red-600',
    green: 'bg-green-100 text-green-600',
    blue: 'bg-blue-100 text-blue-600',
  };

  return (
    <TouchableOpacity 
      className="bg-white dark:bg-gray-800 p-4 rounded-xl shadow-sm mb-4 flex-row items-center"
      onPress={onPress}
    >
      <View className={`p-3 rounded-full mr-4 ${colorVariants[color].split(' ')[0]}`}>
        <Ionicons name={icon} size={24} className={colorVariants[color].split(' ')[1]} color={color === 'indigo' ? '#4F46E5' : color === 'red' ? '#DC2626' : color === 'green' ? '#16A34A' : '#2563EB'} />
      </View>
      <View className="flex-1">
        <Text className="text-lg font-bold text-gray-900 dark:text-white">{title}</Text>
        {subtitle && <Text className="text-gray-500 dark:text-gray-400 text-sm">{subtitle}</Text>}
      </View>
      <Ionicons name="chevron-forward" size={20} color="#9CA3AF" />
    </TouchableOpacity>
  );
};

export default Card;
