// Botón reutilizable con diferentes variantes (primary, secondary, outline, danger)
// Muestra loading spinner cuando isLoading=true

import { ActivityIndicator, Text, TouchableOpacity } from 'react-native';

const Button = ({ title, onPress, variant = 'primary', isLoading, disabled }) => {
  const baseStyle = "rounded-lg py-3 px-4 items-center justify-center";
  const variants = {
    primary: "bg-indigo-600 active:bg-indigo-700",
    secondary: "bg-gray-200 dark:bg-gray-700 active:bg-gray-300 dark:active:bg-gray-600",
    outline: "border border-indigo-600 bg-transparent",
    danger: "bg-red-600 active:bg-red-700",
  };

  const textVariants = {
    primary: "text-white font-bold",
    secondary: "text-gray-900 dark:text-white font-bold",
    outline: "text-indigo-600 font-bold",
    danger: "text-white font-bold",
  };

  return (
    <TouchableOpacity
      className={`${baseStyle} ${variants[variant]} ${disabled ? 'opacity-50' : ''}`}
      onPress={onPress}
      disabled={disabled || isLoading}
    >
      {isLoading ? (
        <ActivityIndicator color={variant === 'outline' ? '#4F46E5' : 'white'} />
      ) : (
        <Text className={textVariants[variant]}>{title}</Text>
      )}
    </TouchableOpacity>
  );
};

export default Button;
