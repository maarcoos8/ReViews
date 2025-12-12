# ReViews - Backend API

API REST para la aplicación ReViews, que permite a los usuarios crear y gestionar reseñas de restaurantes y establecimientos con geolocalización.

## Características Principales

### ✅ Autenticación OAuth 2.0
- Login/Logout mediante Google OAuth
- Tokens JWT para sesiones
- Sistema de cuentas vinculado a proveedores OAuth
- Almacenamiento de tokens OAuth con fechas de emisión y caducidad

### ✅ Reseñas y Geocoding
- Creación de reseñas de establecimientos
- Valoración de 0-5 estrellas
- Geocoding automático usando Nominatim (OpenStreetMap)
- Coordenadas almacenadas en MongoDB
- Asociación de reseñas por email de autor

### ✅ Gestión de Imágenes
- Subida de múltiples imágenes por reseña
- Almacenamiento en Cloudinary
- Endpoint dedicado para upload de imágenes

### ✅ Consulta de Reseñas
- Listado completo de reseñas
- Vista detallada con toda la información (incluido token OAuth)
- Filtrado y paginación

## Estructura del Proyecto

```
backend/
├── app/
│   ├── core/
│   │   ├── auth.py          # JWT y dependencias de autenticación
│   │   ├── config.py        # Configuración y variables de entorno
│   │   ├── geocoding.py     # Utilidades de geocoding
│   │   └── utils.py
│   ├── crud/
│   │   └── marker_crud.py   # Operaciones CRUD para marcadores
│   ├── database/
│   │   └── database.py      # Conexión a MongoDB y Beanie
│   ├── models/
│   │   ├── user.py          # Modelo de Usuario (Beanie Document)
│   │   └── marker.py        # Modelo de Marcador (Beanie Document)
│   ├── routers/
│   │   ├── auth.py          # Endpoints de autenticación
│   │   └── markers.py       # Endpoints de marcadores
│   ├── schemas/
│   │   ├── user.py          # Schemas Pydantic para User
│   │   └── marker.py        # Schemas Pydantic para Marker
│   └── main.py              # FastAPI app y configuración
├── .env                     # Variables de entorno (NO COMMITEAR)
├── .env.example             # Ejemplo de variables de entorno
├── requirements.txt         # Dependencias Python
├── Dockerfile
└── docker-compose.yml
```

## Instalación

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd backend
```

### 2. Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

### 5. Configurar Google OAuth 2.0

1. Ve a [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Crea un nuevo proyecto o selecciona uno existente
3. Ve a "Credenciales" > "Crear credenciales" > "ID de cliente de OAuth 2.0"
4. Configura las URIs de redirección autorizadas:
   - `http://localhost:8000/auth/callback/google`
   - `http://localhost:8000/docs/oauth2-redirect` (para Swagger)
5. Copia el Client ID y Client Secret a tu `.env`

### 6. Ejecutar la aplicación

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

O usando el script de Windows:
```bash
.\run.bat
```

## Endpoints Principales

### Autenticación

- `GET /auth/login/google` - Inicia el flujo de login con Google
- `GET /auth/callback/google` - Callback de Google OAuth
- `POST /auth/logout` - Cierra la sesión
- `GET /auth/me` - Obtiene información del usuario actual

### Marcadores

- `POST /markers/` - Crea un nuevo marcador (con imagen opcional)
- `GET /markers/my-markers` - Obtiene todos los marcadores del usuario actual
- `GET /markers/user/{email}` - Obtiene el mapa de otro usuario
- `DELETE /markers/{marker_id}` - Elimina un marcador
- `PUT /markers/{marker_id}/image` - Actualiza la imagen de un marcador

## Documentación API

Una vez ejecutada la aplicación, accede a:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Stack Tecnológico

- **Framework**: FastAPI 0.118+
- **Base de Datos**: MongoDB
- **ODM**: Beanie (async)
- **Autenticación**: OAuth 2.0 (Google) + JWT
- **Geocoding**: Nominatim (OpenStreetMap)
- **Imágenes**: Cloudinary o Base64 en DB
- **Validación**: Pydantic V2

## Variables de Entorno

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `MONGODB_CONNECTION_STRING` | URI de conexión a MongoDB | `mongodb+srv://user:pass@cluster.mongodb.net/` |
| `MONGODB_DATABASE_NAME` | Nombre de la base de datos | `mimapa_db` |
| `JWT_SECRET_KEY` | Clave secreta para JWT | `your-secret-key` |
| `GOOGLE_CLIENT_ID` | Client ID de Google OAuth | `xxx.apps.googleusercontent.com` |
| `GOOGLE_CLIENT_SECRET` | Client Secret de Google | `GOCSPX-xxx` |
| `FRONTEND_URL` | URL del frontend | `http://localhost:5173` |
| `USE_CLOUDINARY` | Usar Cloudinary para imágenes | `true` o `false` |
| `CLOUDINARY_CLOUD_NAME` | Nombre del cloud de Cloudinary | `your-cloud-name` |
| `CLOUDINARY_API_KEY` | API Key de Cloudinary | `123456789` |
| `CLOUDINARY_API_SECRET` | API Secret de Cloudinary | `your-secret` |

## Docker

### Usando Docker Compose
```bash
docker-compose up -d
```

Esto levantará:
- Backend en puerto 8000
- MongoDB en puerto 27017

## Testing

Para probar el flujo completo:

1. Accede a http://localhost:8000/docs
2. Usa el endpoint `GET /auth/login/google` para iniciar sesión
3. Después de autenticarte, recibirás un token JWT
4. Usa ese token en el botón "Authorize" de Swagger
5. Prueba los endpoints de marcadores

## Notas de Desarrollo

- Todas las operaciones de base de datos son **asíncronas**
- Los marcadores están asociados al email del usuario
- El geocoding usa Nominatim (gratuito, con rate limiting)
- Las imágenes en base64 pueden aumentar el tamaño de la DB significativamente

## Producción

Para desplegar en producción:

1. Cambia `USE_CLOUDINARY=true` y configura Cloudinary
2. Usa una `JWT_SECRET_KEY` segura (generada aleatoriamente)
3. Configura CORS en `main.py` con dominios específicos
4. Usa un servidor ASGI como Gunicorn con workers Uvicorn
5. Configura HTTPS
6. Usa MongoDB Atlas o una instancia dedicada

## Soporte

Para problemas o preguntas, abre un issue en el repositorio.
