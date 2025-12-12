# ReViews

Aplicación web/móvil para gestionar y compartir reseñas de restaurantes y establecimientos con geolocalización.

## Características

- ✅ Autenticación OAuth 2.0 con Google
- ✅ Crear reseñas con valoración (0-5 estrellas)
- ✅ Subida de múltiples imágenes por reseña
- ✅ Geolocalización automática con Nominatim
- ✅ Mapa interactivo con Leaflet
- ✅ Vista detallada con información de tokens OAuth

## Tecnologías

**Backend:**
- FastAPI (Python 3.12+)
- MongoDB + Beanie ODM
- Cloudinary para imágenes
- OAuth 2.0 + JWT

**Frontend:**
- Vue 3 + Composition API
- Ionic Framework
- TypeScript
- Pinia (state management)
- Leaflet (mapas)

## Despliegue Local

```bash
docker-compose up
```

Accede a:
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Documentación API: http://localhost:8000/docs


