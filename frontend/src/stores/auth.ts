// Store de autenticación para Eventual
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { User } from '@/interfaces/eventual';
import authService from '@/services/auth.service';

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);

  const isAuthenticated = computed(() => user.value !== null);

  /**
   * Carga la información del usuario actual
   */
  async function loadUser(): Promise<void> {
    if (!authService.isAuthenticated()) {
      user.value = null;
      return;
    }

    loading.value = true;
    error.value = null;

    try {
      const userData = await authService.getCurrentUser();
      user.value = userData;
    } catch (err: any) {
      error.value = err.message || 'Error al cargar usuario';
      user.value = null;
    } finally {
      loading.value = false;
    }
  }

  /**
   * Inicia el flujo de login con Google
   */
  function loginWithGoogle(): void {
    authService.loginWithGoogle();
  }

  /**
   * Guarda el token del callback de OAuth
   */
  async function handleOAuthCallback(token: string): Promise<void> {
    authService.setToken(token);
    await loadUser();
  }

  /**
   * Cierra la sesión del usuario
   */
  async function logout(): Promise<void> {
    loading.value = true;
    try {
      await authService.logout();
      user.value = null;
    } catch (err: any) {
      error.value = err.message || 'Error al cerrar sesión';
    } finally {
      loading.value = false;
    }
  }

  return {
    user,
    loading,
    error,
    isAuthenticated,
    loadUser,
    loginWithGoogle,
    handleOAuthCallback,
    logout,
  };
});
