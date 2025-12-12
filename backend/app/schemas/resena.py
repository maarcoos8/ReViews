from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List
from datetime import datetime
from beanie import PydanticObjectId


class ResenaBase(BaseModel):
    """Schema base para Reseña"""
    nombre_establecimiento: str = Field(..., min_length=1, max_length=200)
    direccion: str = Field(..., max_length=300)
    latitud: float = Field(..., ge=-90, le=90)
    longitud: float = Field(..., ge=-180, le=180)
    valoracion: float = Field(..., ge=0, le=5)
    imagenes: List[str] = Field(default_factory=list)
    
    @field_validator('valoracion')
    @classmethod
    def validate_valoracion(cls, v: float) -> float:
        """Valida que la valoración esté entre 0 y 5"""
        if v < 0 or v > 5:
            raise ValueError('La valoración debe estar entre 0 y 5')
        return v


class ResenaCreate(ResenaBase):
    """
    Schema para crear una reseña (Request)
    Los datos del autor y token se extraen automáticamente del token OAuth
    """
    pass


class ResenaUpdate(BaseModel):
    """Schema para actualizar una reseña (Request)"""
    nombre_establecimiento: Optional[str] = Field(None, min_length=1, max_length=200)
    direccion: Optional[str] = Field(None, max_length=300)
    latitud: Optional[float] = Field(None, ge=-90, le=90)
    longitud: Optional[float] = Field(None, ge=-180, le=180)
    valoracion: Optional[float] = Field(None, ge=0, le=5)
    imagenes: Optional[List[str]] = None
    
    @field_validator('valoracion')
    @classmethod
    def validate_valoracion(cls, v: Optional[float]) -> Optional[float]:
        """Valida que la valoración esté entre 0 y 5"""
        if v is not None and (v < 0 or v > 5):
            raise ValueError('La valoración debe estar entre 0 y 5')
        return v


class ResenaResponse(ResenaBase):
    """Schema para respuesta de reseña (Response)"""
    id: str = Field(..., alias="_id")
    email_autor: EmailStr
    nombre_autor: str
    token_emision: datetime
    token_caducidad: datetime
    token_oauth: str
    created_at: datetime
    
    class Config:
        populate_by_name = True
        json_encoders = {
            PydanticObjectId: str
        }


class ResenaListResponse(BaseModel):
    """Schema para lista de reseñas (Response)"""
    resenas: List[ResenaResponse]
    total: int
