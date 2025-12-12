import logging
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.config import settings
from app.models.user import User
from app.models.resena import Resena

# Cliente global para reutilización en serverless
_client = None

async def init_db():
    """Inicializa la conexión a MongoDB (compatible con serverless)"""
    global _client
    
    if _client is None:
        logging.info("Conectando a MongoDB...")
        _client = AsyncIOMotorClient(settings.MONGODB_CONNECTION_STRING)
        
        await init_beanie(
            database=_client[settings.MONGODB_DATABASE_NAME],
            document_models=[User, Resena]
        )
        
        logging.info("Conexión a MongoDB y Beanie inicializados exitosamente.")
    
    return _client

async def connect_to_mongo():
    """Mantener compatibilidad con código existente"""
    return await init_db()

async def close_mongo_connection(client: AsyncIOMotorClient):
    logging.info("Cerrando conexión a MongoDB...")
    if client:
        client.close()
    logging.info("Conexión a MongoDB cerrada.")