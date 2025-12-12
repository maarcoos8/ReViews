from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import logging
from app.database.database import init_db
from app.routers import auth, resenas
from app.core.config import settings

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI(
    title="ReViews API",
    description="API para la aplicación ReViews - Gestión de reseñas de establecimientos con geolocalización",
    version="1.0.0",
    root_path="/api"  # Para Vercel deployment
)

# Inicializar DB en el startup (compatible con serverless)
@app.on_event("startup")
async def startup_event():
    await init_db()

# Configurar SessionMiddleware (requerido para OAuth)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.JWT_SECRET_KEY
)

# Configurar CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router)
app.include_router(resenas.router)

@app.get("/")
def read_root():
    return {
        "status": "ok", 
        "service": "ReViews API", 
        "version": "1.0.0",
        "description": "API para gestión de reseñas de establecimientos con OAuth 2.0, geocoding e imágenes"
    }