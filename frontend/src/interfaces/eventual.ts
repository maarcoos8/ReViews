// Interfaces para la aplicación ReViews

export interface User {
  id: string;
  email: string;
  name: string;
  picture?: string;
  oauth_provider: string;
  created_at: string;
  last_login: string;
}

export interface Resena {
  _id: string;
  nombre_establecimiento: string;
  direccion: string;
  latitud: number;
  longitud: number;
  valoracion: number;
  email_autor: string;
  nombre_autor: string;
  token_emision: string;
  token_caducidad: string;
  token_oauth: string;
  imagenes: string[];
  created_at: string;
}

export interface ResenaCreate {
  nombre_establecimiento: string;
  direccion: string;
  latitud: number;
  longitud: number;
  valoracion: number;
  imagenes: string[];
}

export interface ResenaUpdate {
  nombre_establecimiento?: string;
  direccion?: string;
  latitud?: number;
  longitud?: number;
  valoracion?: number;
  imagenes?: string[];
}

export interface AuthCallbackParams {
  token?: string;
  error?: string;
}
