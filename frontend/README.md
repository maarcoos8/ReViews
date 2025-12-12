# ReViews - Frontend

Aplicación móvil/web para crear y consultar reseñas de restaurantes y establecimientos con geolocalización.

## Tech Stack

- **Framework**: Vue 3 (Composition API con `<script setup>`)
- **UI**: Ionic Framework 8
- **Build**: Vite
- **Language**: TypeScript
- **State**: Pinia
- **Maps**: Leaflet
- **Mobile**: Capacitor 7

## Características

### ✅ Autenticación
- Login con Google OAuth 2.0
- Gestión de tokens JWT
- Guard de rutas protegidas
- Logout funcional con redirección

### ✅ Listado de Reseñas
- Vista de todas las reseñas
- Mapa interactivo con Leaflet
- Búsqueda de ubicaciones en el mapa
- Valoración con estrellas

### ✅ Crear Reseña
- Formulario con nombre del establecimiento
- Dirección con geocoding automático
- Sistema de valoración (0-5 estrellas)
- Upload de múltiples imágenes con preview
- Eliminar imágenes antes de subir

### ✅ Detalle de Reseña
- Vista completa con todas las imágenes
- Información del autor
- Datos de token OAuth (emisión, caducidad, token completo)
- Coordenadas geográficas

## Instalación

### 1. Instalar dependencias
```bash
npm install
```

### 2. Configurar variables de entorno
Edita el archivo `.env`:
```env
VITE_API_URL=http://localhost:8000
```

### 3. Ejecutar en desarrollo
```bash
npm run dev
```

La aplicación estará disponible en `http://localhost:5173`

## Estructura del Proyecto

```
src/
├── components/
│   ├── MapViewer.vue        # Componente de mapa con Leaflet
│   └── Layout.vue           # Layout compartido
├── interfaces/
│   └── mimapa.ts            # Tipos TypeScript (User, Marker, etc.)
├── services/
│   ├── auth.service.ts      # Comunicación con API de auth
│   └── marker.service.ts    # Comunicación con API de marcadores
├── stores/
│   ├── auth.ts              # Estado de autenticación (Pinia)
│   └── marker.ts            # Estado de marcadores (Pinia)
├── views/
│   ├── Login.vue            # Pantalla de inicio de sesión
│   ├── AuthCallback.vue     # Callback de OAuth
│   ├── MyMap.vue            # Mapa personal del usuario
│   ├── AddMarker.vue        # Formulario añadir marcador
│   └── VisitMap.vue         # Ver mapa de otro usuario
├── router/
│   └── index.ts             # Configuración de rutas
└── main.ts                  # Entry point
```

## Rutas

| Ruta | Componente | Descripción | Auth |
|------|-----------|-------------|------|
| `/login` | Login.vue | Inicio de sesión con Google | No |
| `/auth/callback` | AuthCallback.vue | Procesa callback de OAuth | No |
| `/my-map` | MyMap.vue | Mapa personal | Sí |
| `/add-marker` | AddMarker.vue | Añadir nuevo marcador | Sí |
| `/visit-map` | VisitMap.vue | Ver mapa de otro usuario | No |

## Stores (Pinia)

### AuthStore (`stores/auth.ts`)
- `user`: Usuario autenticado
- `isAuthenticated`: Boolean de autenticación
- `loadUser()`: Carga datos del usuario
- `loginWithGoogle()`: Inicia OAuth flow
- `handleOAuthCallback(token)`: Procesa token
- `logout()`: Cierra sesión

### MarkerStore (`stores/marker.ts`)
- `myMarkers`: Array de marcadores del usuario
- `visitedUserMap`: Mapa de usuario visitado
- `loadMyMarkers()`: Carga marcadores propios
- `createMarker(data, image)`: Crea nuevo marcador
- `deleteMarker(id)`: Elimina marcador
- `loadUserMap(email)`: Carga mapa de otro usuario

## Servicios

### AuthService (`services/auth.service.ts`)
- Maneja tokens JWT en localStorage
- Comunica con endpoints `/auth/*`
- Valida autenticación

### MarkerService (`services/marker.service.ts`)
- Upload de imágenes con FormData
- CRUD de marcadores
- Consulta de mapas públicos

## Mapas con Leaflet

El componente `MapViewer.vue` implementa:
- OpenStreetMap tiles
- Marcadores interactivos
- Click handlers
- Auto-fit bounds
- Info panels

**Importante**: Los iconos de Leaflet requieren imports específicos para funcionar con Vite.

## Build para Producción

```bash
npm run build
```

Los archivos compilados estarán en `dist/`

## Capacitor (Mobile)

### iOS
```bash
npx cap add ios
npx cap sync ios
npx cap open ios
```

### Android
```bash
npx cap add android
npx cap sync android
npx cap open android
```

## Testing

### Unit Tests
```bash
npm run test:unit
```

### E2E Tests
```bash
npm run test:e2e
```

## Lint

```bash
npm run lint
```

## Flujo de Autenticación

1. Usuario hace clic en "Iniciar sesión con Google"
2. Redirige a `/auth/login/google` (backend)
3. Google OAuth flow
4. Redirige a `/auth/callback?token=xxx`
5. `AuthCallback.vue` guarda el token
6. Redirige a `/my-map`

## Notas de Desarrollo

- Usar **Composition API** con `<script setup lang="ts">`
- Estilos `scoped` en componentes
- Componentes Ionic para UI consistente
- Tipado estricto con TypeScript
- Caché de 5 minutos en stores

## Variables de Entorno

| Variable | Descripción | Default |
|----------|-------------|---------|
| `VITE_API_URL` | URL del backend | `http://localhost:8000` |

## Soporte

Para problemas o preguntas, consulta la documentación de:
- [Vue 3](https://vuejs.org/)
- [Ionic Framework](https://ionicframework.com/docs/)
- [Leaflet](https://leafletjs.com/)
- [Pinia](https://pinia.vuejs.org/)
