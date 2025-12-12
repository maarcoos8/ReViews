## 1. Contexto del Proyecto
Este proyecto es el **Frontend** de una aplicación de gestión de calendarios y eventos ("Kalendas"). Se comunica con una arquitectura de microservicios (Backend en FastAPI + MongoDB/Beanie) a través de un API Gateway.

La aplicación debe permitir la creación jerárquica de calendarios, gestión de eventos con multimedia/mapas, y un sistema social de comentarios y notificaciones.

## 2. Stack Tecnológico
* **Framework:** Vue.js 3 (Composition API con `<script setup>`).
* **UI Library:** Ionic Framework 8 (Componentes web nativos).
* **Lenguaje:** TypeScript (Estricto).
* **Build Tool:** Vite.
* **Gestión de Estado:** Reactividad nativa de Vue (`ref`, `reactive`, `computed`) y Composables.
* **Testing:** Cypress (E2E) y Vitest (Unit).
* **Comunicación HTTP:** Fetch API nativa (encapsulada en servicios).

## 3. Estructura del Proyecto y Arquitectura
Debes seguir estrictamente la estructura de carpetas existente:

* **`src/views/`**: Páginas principales (ej. `Home.vue`, `Calendar.vue`).
    * *Patrón:* Si la lógica es compleja, sepárala en un archivo `.ts` (ej. `Home.ts` contiene la lógica de `Home.vue`).
    * *Estilos:* Si el CSS es extenso, sepáralo en un archivo `.css` (ej. `CreateCalendar.css`).
* **`src/components/`**: Componentes reutilizables (ej. `CalendarMonth.vue`, `Layout.vue`).
* **`src/services/`**: Capa de comunicación con la API. Patrón Singleton.
* **`src/interfaces/`**: Definiciones de tipos TypeScript (DTOs).
* **`src/theme/`**: Variables globales de CSS y configuración de Ionic.

## 4. Reglas de Desarrollo

### 4.1. Componentes y UI (Ionic + Vue)
* Utiliza siempre **Composition API** (`<script setup lang="ts">`).
* Usa componentes de **Ionic** (`<ion-page>`, `<ion-content>`, `<ion-item>`, etc.) para mantener el diseño adaptativo (móvil/escritorio).
* Implementa `MainLayout` (`src/components/Layout.vue`) en todas las vistas principales para mantener la cabecera y navegación consistentes.
* **Modo Oscuro:** Respeta las variables CSS de Ionic. Usa `ThemeService` para la gestión del tema (claro/oscuro/sistema).

### 4.2. Comunicación con Backend (Servicios)
* No realices llamadas `fetch` dentro de los componentes `.vue`.
* Crea o extiende archivos en `src/services/`.
* Usa las variables de entorno para las URLs base:
    * `import.meta.env.VITE_CALENDAR_API_URL`
    * `import.meta.env.VITE_EVENTS_API_URL`
    * `import.meta.env.VITE_NOTIFICATIONS_API_URL`
* **Manejo de IDs:** MongoDB devuelve `_id`. El frontend debe ser capaz de manejar `_id` o mapearlo a `id` según sea necesario en las interfaces.

**Ejemplo de patrón de servicio:**
```typescript
class EntityService {
    private baseUrl = import.meta.env.VITE_API_URL;

    async getAll(): Promise<Entity[]> {
        const res = await fetch(`${this.baseUrl}/entity`);
        if (!res.ok) throw new Error("Error fetching");
        return res.json();
    }
}
export default new EntityService();
```

### 4.3. Tipado (TypeScript)
* Define todas las entidades en `src/interfaces/`.
* Mantén la sincronización con los modelos de Pydantic del backend.
    * *Nota:* Las fechas suelen llegar como `string` (ISO 8601).
    * *Nota:* Los arrays opcionales deben manejarse con `?` (ej. `events?: Event[]`).

## 5. Funcionalidades Específicas a Implementar/Mantener

### 5.1. Calendarios y Jerarquía
* Los calendarios pueden tener un `parent_id`.
* En la vista `Home`, se debe mostrar la jerarquía (padres e hijos desplegables).
* La navegación debe permitir filtrar por calendarios específicos o grupos.

### 5.2. Eventos y Mapas
* **Mapas:** Implementar visualización usando **OpenStreetMap** (se recomienda usar la libreria Leaflet para la integración).
* Los eventos tienen `location_latitude` y `location_longitude` para posicionar el marcador.
* **No uses Google Maps**, ya que el requisito explícito es usar OpenStreetMap para la visualización de ubicaciones.

### 5.3. Imágenes y Archivos (Cloudinary)
* El modelo de evento soporta `media: MediaItem[]`.
* **Gestión con Cloudinary:** Se debe utilizar el servicio de Cloudinary para la subida y alojamiendo de archivos multimedia.
* El flujo debe ser:
    * El usuario selecciona el archivo en el frontend
    * El frontend sube el archivo directamente a cloudinary (o a través de un endpoint firmado si se implementa)
    * Cloudinary devuelve la URL pública del recurso
    * El frontend envía esta URL en el objeto del evento al backend para persistirla en base de datos.

### 5.4. Comentarios y Notificaciones
* Utiliza el `notificacion.service.ts` existente para la gestión de notificaciones.
* Las notificaciones tienen estado `visto`. Implementar la lógica para marcar como vista al hacer clic.
* La "campanita" en el `Layout` debe actualizarse reactivamente. Se recomienda usar un **Bus de Eventos** simple (como `mitt` o `CustomEvent` del navegador) o un estado global (Pinia) para que el contador baje sin recargar la página.

## 6. Testing
* **E2E (Cypress):** Los tests deben simular flujos completos de usuario:
    1. Entrar a la Home.
    2. Crear un Calendario.
    3. Entrar al Calendario y crear un Evento.
* **Unit (Vitest):** Testear la lógica de los servicios (`calendar.service.ts`, `event.service.ts`) y el renderizado básico de componentes aislados.

## 7. Manejo de Errores
* Usa `alertController` o `toastController` de Ionic para mostrar feedback visual al usuario en caso de fallos (ej. error 500 del backend, error de red).
* Implementa validación básica en los formularios (campos requeridos como `title`) antes de permitir el envío al backend.