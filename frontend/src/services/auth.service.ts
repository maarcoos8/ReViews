// Servicio de autenticación para Eventual
import type { User } from '@/interfaces/eventual';

// En desarrollo (Docker): usa VITE_API_URL del .env (http://localhost:8000)
// En producción (Vercel): usa rutas relativas con prefijo /api
const API_BASE = import.meta.env.VITE_API_URL || '/api';

class AuthService {
  private token: string | null = null;

  constructor() {
    // Cargar token del localStorage al iniciar
    this.token = localStorage.getItem('auth_token');
  }

  loginWithGoogle(): void {
    window.location.href = `${API_BASE}/auth/login/google`;
  }

  /**
   * Guarda el token recibido del callback de OAuth
   */
  setToken(token: string): void {
    this.token = token;
    localStorage.setItem('auth_token', token);
  }

  /**
   * Obtiene el token actual
   */
  getToken(): string | null {
    return this.token;
  }

  /**
   * Cierra sesión (elimina el token)
   */
  async logout(): Promise<void> {
    try {
      // Llamar al endpoint de logout (opcional, ya que JWT es stateless)
      await fetch(`${API_BASE}/auth/logout`, {
        method: 'POST',
        headers: this.getAuthHeaders(),
      });
    } catch (error) {
      console.error('Error al hacer logout:', error);
    } finally {
      // Eliminar token localmente
      this.token = null;
      localStorage.removeItem('auth_token');
      // Redirigir al login
      window.location.href = '/login';
    }
  }

  /**
   * Obtiene la información del usuario actual
   */
  async getCurrentUser(): Promise<User | null> {
    if (!this.token) {
      return null;
    }

    try {
      const response = await fetch(`${API_BASE}/auth/me`, {
        headers: this.getAuthHeaders(),
      });

      if (!response.ok) {
        if (response.status === 401) {
          // Token inválido, limpiar
          this.logout();
        }
        throw new Error('No se pudo obtener la información del usuario');
      }

      return await response.json();
    } catch (error) {
      console.error('Error al obtener usuario:', error);
      return null;
    }
  }

  /**
   * Verifica si el usuario está autenticado
   */
  isAuthenticated(): boolean {
    return this.token !== null;
  }

  /**
   * Obtiene los headers de autenticación
   */
  getAuthHeaders(): HeadersInit {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    return headers;
  }
}

export default new AuthService();
