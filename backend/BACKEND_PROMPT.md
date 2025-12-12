# Backend Development Guidelines & Architecture

## Tech Stack
- **Framework:** FastAPI (Python 3.12+)
- **Database:** MongoDB
- **ODM (Object Document Mapper):** Beanie (asynchronous)
- **Driver:** Motor (AsyncIOMotorClient)
- **Validation:** Pydantic V2
- **Architecture:** Microservices (managed via Docker Compose)

## Project Structure (Microservices)
El proyecto sigue una arquitectura de microservicios. 
Se implementará todo en el microservicio.

### Estructura de Directorios
app/
├── core/           # Configuración (config.py) y utilidades
├── crud/           # Lógica de acceso a datos (CRUD operations separadas)
├── database/       # Conexión a DB y configuración de Beanie
├── models/         # Modelos de base de datos (Beanie Documents)
├── routers/        # Endpoints de la API (APIRouter)
├── schemas/        # Esquemas Pydantic (Request/Response DTOs)
└── main.py         # Entry point y configuración de la App

## Coding Standards & Patterns

1. **Asincronía:** Todo el código de base de datos y endpoints debe ser `async`.
2. **Separación de Modelos:**
   - **Models (`models/`):** Clases que heredan de `beanie.Document`. Representan la colección en MongoDB.
   - **Schemas (`schemas/`):** Clases que heredan de `pydantic.BaseModel`. Se usan para validación de entrada (Requests) y salida (Responses).
3. **CRUD Pattern:** No escribir lógica de base de datos directamente en los `routers`. Usar clases o funciones en la carpeta `crud/` para encapsular las operaciones de base de datos (ej. `CalendarCRUD.get_all()`).
4. **Dependency Injection:** Utilizar el sistema de inyección de dependencias de FastAPI donde sea necesario.
5. **Configuración:** Las variables de entorno se gestionan mediante `pydantic-settings` en `core/config.py`.

## Specific Implementation Details
- **Beanie Initialization:** Se realiza en el evento `lifespan` en `main.py`.
- **IDs:** Uso de `PydanticObjectId` para manejar los `_id` de MongoDB.
- **Docker:** Cada servicio tiene su propio `Dockerfile` y se orquesta con `docker-compose.yml`. El desarrollo se realiza con hot-reload (`uvicorn --reload`).

## Instrucción para el Agente
Cuando generes código para el backend:
1. Verifica si la funcionalidad requiere un nuevo modelo, esquema o endpoint.
2. Mantén la separación estricta entre capa de datos (CRUD) y capa de presentación (Routers).
3. Asegúrate de actualizar los modelos Pydantic para reflejar cualquier cambio en los documentos de base de datos.
4. Sigue las convenciones de nombres existentes (snake_case para Python).