# Frontend Development Guidelines & Architecture

## Tech Stack
- **Framework:** Vue 3 (Composition API, `<script setup lang="ts">`)
- **UI Library:** Ionic Framework 8 (`@ionic/vue`)
- **Build Tool:** Vite
- **Language:** TypeScript
- **State Management:** Pinia
- **Maps:** Leaflet
- **Native/Mobile:** Capacitor 7
- **CSS:** CSS Modules / Scoped CSS + Ionic CSS Utilities

## Project Structure
src/
├── components/     # Componentes reutilizables (ej. MapPicker.vue, Layout.vue)
├── interfaces/     # Definiciones de tipos TypeScript
├── services/       # Comunicación HTTP con el Backend
├── stores/         # Gestión de estado con Pinia
├── theme/          # Variables CSS globales (variables.css)
├── views/          # Páginas principales (Vistas de Ionic)
└── main.ts         # Inicialización de la app

## Implementation Patterns

### 1. Componentes & Vistas
- Usar **Composition API** con `<script setup lang="ts">`.
- Usar componentes de Ionic (`ion-page`, `ion-content`, `ion-list`, etc.) para asegurar compatibilidad móvil.
- Los estilos deben ser `scoped` a menos que sean utilidades globales.

### 2. Gestión de Estado (Pinia)
- Los `stores` (ej. `stores/calendar.ts`) manejan la lógica de negocio y el estado global.
- **Caché manual:** Se implementa lógica para evitar fetch innecesarios (ej. verificar `lastFetch` < 5 min).
- Procesamiento de datos: La lógica compleja (como jerarquías de calendarios) se procesa en el store o helpers, no en la vista.

### 3. Servicios (API Layer)
- Toda comunicación HTTP reside en `src/services/`.
- Usar `fetch` nativo (o wrapper configurado) apuntando a las variables de entorno (`import.meta.env.VITE_...`).
- Tipar siempre las respuestas con las interfaces de `src/interfaces/`.

### 4. Mapas (Leaflet)
- Implementación manual en `components/MapPicker.vue`.
- **Importante:** Leaflet requiere corrección manual de iconos en Vite (`iconUrl`, `shadowUrl` imports).
- No usar librerías wrapper de Vue-Leaflet a menos que sea necesario; la implementación actual usa `L.map` directamente sobre un `ref` del DOM.
- Integración con Nominatim (OpenStreetMap) para geocodificación inversa y búsqueda.

### 5. Navegación
- Uso de `vue-router` integrado con `IonRouterOutlet`.
- Rutas definidas en `router/index.ts`.

## Instrucción para el Agente
Al desarrollar para el frontend:
1. Respeta el diseño móvil-primero de Ionic.
2. Si añades llamadas a la API, crea primero el método en el `service` correspondiente, luego la acción en el `store`, y finalmente úsalo en el componente.
3. Tipa estrictamente todas las props y emits.
4. Para mapas, referencia `MapPicker.vue` como ejemplo de integración correcta con Vite.