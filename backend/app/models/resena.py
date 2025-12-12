from beanie import Document, PydanticObjectId
from pydantic import EmailStr, Field, ConfigDict, field_validator
from typing import Optional, List
from datetime import datetime


class Resena(Document):
    """
    Modelo de Reseña de Establecimiento
    Almacena reseñas de establecimientos con ubicación, valoración, autor OAuth e imágenes
    """
    id: Optional[PydanticObjectId] = Field(default=None, alias="_id")
    nombre_establecimiento: str = Field(..., min_length=1, max_length=200)
    direccion: str = Field(..., max_length=300)  # Dirección postal del establecimiento
    latitud: float = Field(..., ge=-90, le=90)  # Coordenada GPS latitud (-90 a 90)
    longitud: float = Field(..., ge=-180, le=180)  # Coordenada GPS longitud (-180 a 180)
    valoracion: float = Field(..., ge=0, le=5)  # Valoración de 0 a 5
    email_autor: EmailStr = Field(..., index=True)  # Email del autor de la reseña (del token OAuth)
    nombre_autor: str  # Nombre del autor de la reseña (del token OAuth)
    token_emision: datetime  # Timestamp de emisión del token OAuth
    token_caducidad: datetime  # Timestamp de caducidad del token OAuth
    token_oauth: str  # Token de identificación OAuth con el que se creó la reseña
    imagenes: List[str] = Field(default_factory=list)  # URLs de imágenes en Cloudinary
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    @field_validator('valoracion')
    @classmethod
    def validate_valoracion(cls, v: float) -> float:
        """Valida que la valoración esté entre 0 y 5"""
        if v < 0 or v > 5:
            raise ValueError('La valoración debe estar entre 0 y 5')
        return v
    
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={PydanticObjectId: str},
        json_schema_extra={
            "example": {
                "nombre_establecimiento": "Restaurante El Buen Sabor",
                "direccion": "Calle Mayor 123, Madrid",
                "latitud": 40.4168,
                "longitud": -3.7038,
                "valoracion": 4.5,
                "email_autor": "usuario@example.com",
                "nombre_autor": "Juan Pérez",
                "token_emision": "2025-12-12T10:00:00",
                "token_caducidad": "2025-12-12T11:00:00",
                "token_oauth": "ya29.a0AfH6SMBx...",
                "imagenes": [
                    "https://res.cloudinary.com/demo/image/upload/restaurante1.jpg",
                    "https://res.cloudinary.com/demo/image/upload/restaurante2.jpg"
                ]
            }
        }
    )
    
    class Settings:
        name = "resenas"
