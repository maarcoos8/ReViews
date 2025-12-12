"""
Servicio para subir imágenes a Cloudinary
"""
import cloudinary
import cloudinary.uploader
from app.core.config import settings
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# Configurar Cloudinary
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True
)


async def upload_image(file_content: bytes, filename: str) -> Optional[str]:
    """
    Sube una imagen a Cloudinary y retorna la URL segura
    
    Args:
        file_content: Contenido del archivo en bytes
        filename: Nombre del archivo original
        
    Returns:
        URL de la imagen subida o None si falla
    """
    try:
        # Subir imagen a Cloudinary
        result = cloudinary.uploader.upload(
            file_content,
            folder="eventual/eventos",  # Carpeta en Cloudinary
            resource_type="image",
            allowed_formats=["jpg", "jpeg", "png", "gif", "webp"],
            transformation=[
                {"width": 1200, "height": 800, "crop": "limit"},  # Limitar tamaño
                {"quality": "auto:good"}  # Optimizar calidad
            ]
        )
        
        logger.info(f"Imagen subida exitosamente: {result['secure_url']}")
        return result["secure_url"]
        
    except Exception as e:
        logger.error(f"Error al subir imagen a Cloudinary: {str(e)}")
        raise Exception(f"Error al subir imagen: {str(e)}")
