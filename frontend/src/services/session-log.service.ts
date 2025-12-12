// Servicio para gestión de logs de sesión
import type { SessionLog } from '@/interfaces/eventual';

// En desarrollo (Docker): usa VITE_API_URL del .env (http://localhost:8000)
// En producción (Vercel): usa rutas relativas con prefijo /api
const API_BASE = import.meta.env.VITE_API_URL || '/api';

class SessionLogService {
  private getAuthHeaders(): HeadersInit {
    const token = localStorage.getItem('auth_token');
    return {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
    };
  }

  /**
   * Obtener todos los logs de sesión
   */
  async obtenerLogs(): Promise<SessionLog[]> {
    const response = await fetch(`${API_BASE}/session-logs/`, {
      headers: this.getAuthHeaders(),
    });
    if (!response.ok) {
      throw new Error('Error al obtener logs de sesión');
    }
    return response.json();
  }
}

export default new SessionLogService();
