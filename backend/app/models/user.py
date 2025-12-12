from beanie import Document, PydanticObjectId
from pydantic import EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime


class User(Document):
    """
    Modelo de Usuario para autenticación OAuth 2.0
    Almacena la información del usuario autenticado vía Google/Facebook
    """
    id: Optional[PydanticObjectId] = Field(default=None, alias="_id")
    email: EmailStr = Field(..., unique=True, index=True)
    name: str
    picture: Optional[str] = None  # URL de la foto de perfil del proveedor OAuth
    oauth_provider: str  # "google", "facebook", etc.
    oauth_id: str  # ID único del proveedor OAuth
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: datetime = Field(default_factory=datetime.utcnow)
    
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={PydanticObjectId: str},
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "name": "John Doe",
                "picture": "https://example.com/photo.jpg",
                "oauth_provider": "google",
                "oauth_id": "1234567890"
            }
        }
    )
    
    class Settings:
        name = "users"
