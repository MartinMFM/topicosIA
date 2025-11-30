/**
 * Store de autenticación (Zustand)
 * 
 * Maneja estado global de usuario: login, registro, logout.
 * Estado: { user, token, isLoading, error }
 */

import { create } from 'zustand';
import { loginUser, registerUser } from '../api/api';

const useAuthStore = create((set) => ({
  user: null,
  token: null,
  isLoading: false,
  error: null,

  /**
   * Login: autentica usuario y actualiza estado
   */
  login: async (email, password) => {
    set({ isLoading: true, error: null });
    try {
      const response = await loginUser(email, password);
      
      if (response.data.success) {
        set({ 
          user: response.data.user, 
          token: 'logged-in',
          isLoading: false 
        });
      } else {
        set({ 
          error: response.data.message || 'Error al iniciar sesión', 
          isLoading: false 
        });
      }
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Error de conexión. Verifica que el backend esté corriendo.';
      set({ 
        error: errorMessage, 
        isLoading: false 
      });
    }
  },

  /**
   * Registro: crea cuenta y autentica automáticamente
   */
  register: async (name, email, password) => {
    set({ isLoading: true, error: null });
    try {
      const response = await registerUser(name, email, password);
      
      if (response.data.success) {
        set({ 
          user: response.data.user, 
          token: 'logged-in',
          isLoading: false 
        });
      } else {
        set({ 
          error: response.data.message || 'Error al registrar', 
          isLoading: false 
        });
      }
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Error de conexión. Verifica que el backend esté corriendo.';
      set({ 
        error: errorMessage, 
        isLoading: false 
      });
    }
  },

  logout: () => set({ user: null, token: null }),
}));

export default useAuthStore;
