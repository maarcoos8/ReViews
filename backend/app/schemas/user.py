from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# Schema para crear usuarios (desde OAuth)
class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="Email del usuario")
    name: str = Field(..., min_length=1, max_length=200, description="Nombre del usuario")
    picture: Optional[str] = Field(None, description="URL de la foto de perfil")
    oauth_provider: str = Field(..., description="Proveedor OAuth (google, facebook, etc.)")
    oauth_id: str = Field(..., description="ID único del proveedor OAuth")

# Schema para actualizar usuarios
class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200, description="Nombre del usuario")
    picture: Optional[str] = Field(None, description="URL de la foto de perfil")
