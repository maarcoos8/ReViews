from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request
from app.models.user import User
from app.core.auth import create_access_token, get_current_user
from app.core.config import settings
from datetime import datetime, timedelta
import logging

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Configurar OAuth
oauth = OAuth()

# Registrar Google OAuth
oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)


@router.get("/login/google")
async def login_google(request: Request):
    """
    Inicia el flujo de autenticación con Google OAuth 2.0
    Redirige al usuario a la página de login de Google
    """
    # Construir redirect_uri manualmente para Vercel
    base_url = str(request.base_url).rstrip('/')
    redirect_uri = f"{base_url}/api/auth/callback/google"
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/callback/google", name="auth_google")
async def auth_google(request: Request):
    """
    Callback de Google OAuth 2.0
    Procesa la respuesta de Google y crea/actualiza el usuario
    """
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get('userinfo')
        
        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se pudo obtener información del usuario desde Google"
            )
        
        # Buscar o crear usuario
        email = user_info.get('email')
        user = await User.find_one(User.email == email)
        
        if not user:
            # Crear nuevo usuario
            user = User(
                email=email,
                name=user_info.get('name', ''),
                picture=user_info.get('picture'),
                oauth_provider='google',
                oauth_id=user_info.get('sub')
            )
            await user.insert()
            logging.info(f"Nuevo usuario creado: {email}")
        else:
            # Actualizar último login
            user.last_login = datetime.utcnow()
            await user.save()
            logging.info(f"Usuario existente logueado: {email}")
        
        # Crear token JWT
        access_token = await create_access_token(data={"sub": user.email})
        
        # Redirigir al frontend con el token
        # El frontend debe estar configurado para recibir el token en la URL
        frontend_url = f"{settings.FRONTEND_URL}/auth/callback?token={access_token}"
        logging.info(f"Redirigiendo a: {frontend_url}")
        return RedirectResponse(url=frontend_url, status_code=302)
        
    except Exception as e:
        logging.error(f"Error en autenticación de Google: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en la autenticación: {str(e)}"
        )


@router.post("/logout")
async def logout():
    """
    Cierra la sesión del usuario
    En un sistema JWT stateless, el logout se maneja principalmente en el cliente
    eliminando el token. Este endpoint es principalmente informativo.
    """
    return {"message": "Sesión cerrada correctamente. Elimina el token del cliente."}


@router.get("/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Obtiene la información del usuario actual autenticado
    Requiere token JWT válido
    """
    return current_user
