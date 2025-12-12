// Servicio para gestión de reseñas
import type { Resena, ResenaCreate, ResenaUpdate } from '@/interfaces/eventual';

// En desarrollo (Docker): usa VITE_API_URL del .env (http://localhost:8000)
// En producción (Vercel): usa rutas relativas con prefijo /api
const API_BASE = import.meta.env.VITE_API_URL || '/api';

class ResenaService {
  private getAuthHeaders(): HeadersInit {
    const token = localStorage.getItem('auth_token');
    return {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
    };
  }

  /**
   * Obtener todas las reseñas
   */
  async obtenerTodas(skip = 0, limit = 100): Promise<{ resenas: Resena[]; total: number }> {
    const response = await fetch(
      `${API_BASE}/resenas/?skip=${skip}&limit=${limit}`,
      {
        headers: this.getAuthHeaders(),
      }
    );
    if (!response.ok) {
      throw new Error('Error al obtener reseñas');
    }
    return response.json();
  }

  /**
   * Obtener una reseña por ID
   */
  async obtenerPorId(id: string): Promise<Resena> {
    const response = await fetch(`${API_BASE}/resenas/${id}`, {
      headers: this.getAuthHeaders(),
    });
    if (!response.ok) {
      throw new Error('Error al obtener reseña');
    }
    return response.json();
  }

  /**
   * Crear una nueva reseña
   */
  async crear(resena: ResenaCreate): Promise<Resena> {
    const response = await fetch(`${API_BASE}/resenas/`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(resena),
    });
    if (!response.ok) {
      throw new Error('Error al crear reseña');
    }
    return response.json();
  }

  /**
   * Actualizar una reseña
   */
  async actualizar(id: string, resena: ResenaUpdate): Promise<Resena> {
    const response = await fetch(`${API_BASE}/resenas/${id}`, {
      method: 'PUT',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(resena),
    });
    if (!response.ok) {
      throw new Error('Error al actualizar reseña');
    }
    return response.json();
  }

  /**
   * Eliminar una reseña
   */
  async eliminar(id: string): Promise<void> {
    const response = await fetch(`${API_BASE}/resenas/${id}`, {
      method: 'DELETE',
      headers: this.getAuthHeaders(),
    });
    if (!response.ok) {
      throw new Error('Error al eliminar reseña');
    }
  }

  /**
   * Obtener mis reseñas
   */
  async obtenerMisResenas(skip = 0, limit = 100): Promise<{ resenas: Resena[]; total: number }> {
    const response = await fetch(
      `${API_BASE}/resenas/mis-resenas?skip=${skip}&limit=${limit}`,
      {
        headers: this.getAuthHeaders(),
      }
    );
    if (!response.ok) {
      throw new Error('Error al obtener mis reseñas');
    }
    return response.json();
  }

  /**
   * Buscar reseñas por establecimiento
   */
  async buscarPorEstablecimiento(nombre: string, skip = 0, limit = 100): Promise<Resena[]> {
    const response = await fetch(
      `${API_BASE}/resenas/establecimiento/${encodeURIComponent(nombre)}?skip=${skip}&limit=${limit}`,
      {
        headers: this.getAuthHeaders(),
      }
    );
    if (!response.ok) {
      throw new Error('Error al buscar reseñas por establecimiento');
    }
    return response.json();
  }

  /**
   * Buscar reseñas por ubicación
   */
  async buscarPorUbicacion(
    latitud: number,
    longitud: number,
    radio_km = 5.0
  ): Promise<Resena[]> {
    const response = await fetch(
      `${API_BASE}/resenas/ubicacion?latitud=${latitud}&longitud=${longitud}&radio_km=${radio_km}`,
      {
        headers: this.getAuthHeaders(),
      }
    );
    if (!response.ok) {
      throw new Error('Error al buscar reseñas por ubicación');
    }
    return response.json();
  }

  /**
   * Buscar reseñas por valoración
   */
  async buscarPorValoracion(
    min_valoracion = 0,
    max_valoracion = 5,
    skip = 0,
    limit = 100
  ): Promise<Resena[]> {
    const response = await fetch(
      `${API_BASE}/resenas/valoracion?min_valoracion=${min_valoracion}&max_valoracion=${max_valoracion}&skip=${skip}&limit=${limit}`,
      {
        headers: this.getAuthHeaders(),
      }
    );
    if (!response.ok) {
      throw new Error('Error al buscar reseñas por valoración');
    }
    return response.json();
  }

  /**
   * Subir una imagen
   */
  async subirImagen(file: File): Promise<{ url: string }> {
    const formData = new FormData();
    formData.append('file', file);

    const token = localStorage.getItem('auth_token');
    const response = await fetch(`${API_BASE}/resenas/upload-image`, {
      method: 'POST',
      headers: {
        ...(token && { Authorization: `Bearer ${token}` }),
      },
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Error al subir imagen');
    }
    return response.json();
  }
}

export const resenaService = new ResenaService();
