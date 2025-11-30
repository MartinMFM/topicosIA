import { Ionicons } from "@expo/vector-icons";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import HomeScreen from "../screens/HomeScreen";
import LoginScreen from "../screens/LoginScreen";
import RegisterScreen from "../screens/RegisterScreen";
import useAuthStore from "../store/authStore";

import CameraScreen from "../screens/CameraScreen";
import ReportIncidentScreen from "../screens/ReportIncidentScreen";
import ResultsScreen from "../screens/ResultsScreen";

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

const AuthStack = () => (
  <Stack.Navigator screenOptions={{ headerShown: false }}>
    <Stack.Screen name="Login" component={LoginScreen} />
    <Stack.Screen name="Register" component={RegisterScreen} />
  </Stack.Navigator>
);

const HomeStack = () => (
  <Stack.Navigator screenOptions={{ headerShown: false }}>
    <Stack.Screen name="HomeScreen" component={HomeScreen} />
    <Stack.Screen name="Camera" component={CameraScreen} />
    <Stack.Screen name="Results" component={ResultsScreen} />
    <Stack.Screen name="ReportIncident" component={ReportIncidentScreen} />
  </Stack.Navigator>
);

const MainTab = () => (
  <Tab.Navigator
    screenOptions={({ route }) => ({
      headerShown: false,
      tabBarIcon: ({ focused, color, size }) => {
        let iconName;

        if (route.name === "Home") {
          iconName = focused ? "home" : "home-outline";
        } else if (route.name === "Camera") {
          iconName = focused ? "camera" : "camera-outline";
        }

        return <Ionicons name={iconName} size={size} color={color} />;
      },
      tabBarActiveTintColor: "#4F46E5",
      tabBarInactiveTintColor: "gray",
    })}
  >
    <Tab.Screen
      name="Home"
      component={HomeStack}
      options={{ tabBarLabel: "Inicio" }}
    />
    <Tab.Screen
      name="Camera"
      component={CameraScreen}
      options={{ tabBarLabel: "Cámara" }}
    />
  </Tab.Navigator>
);

const AppNavigator = () => {
  const { token } = useAuthStore();

  return (
    <NavigationContainer>
      {token ? <MainTab /> : <AuthStack />}
    </NavigationContainer>
  );
};

export default AppNavigator;
