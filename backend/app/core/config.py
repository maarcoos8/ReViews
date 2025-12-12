from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # MongoDB Configuration
    MONGODB_CONNECTION_STRING: str
    MONGODB_DATABASE_NAME: str
    
    # JWT Authentication
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    
    # OAuth 2.0 Google
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    
    # Frontend URL (para redirección después de OAuth)
    FRONTEND_URL: str = "http://localhost:5173"
    
    # Cloudinary Configuration (requerido)
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str

    class Config:
        env_file = ".env"

settings = Settings()

# EJEMPLO DE .ENV ACTUALIZADO:
# MONGODB_CONNECTION_STRING=mongodb+srv://<user>:<pass>@cluster.mongodb.net/
# MONGODB_DATABASE_NAME=mimapa_db
# JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
# JWT_ALGORITHM=HS256
# GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
# GOOGLE_CLIENT_SECRET=your-google-client-secret
# FRONTEND_URL=http://localhost:5173
# CLOUDINARY_CLOUD_NAME=your-cloud-name
# CLOUDINARY_API_KEY=your-api-key
# CLOUDINARY_API_SECRET=your-api-secret