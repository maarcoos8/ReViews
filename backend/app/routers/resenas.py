from fastapi import APIRouter, HTTPException, status, Depends, Query, UploadFile, File
from typing import List, Optional
from beanie import PydanticObjectId
from app.models.user import User
from app.models.resena import Resena
from app.schemas.resena import ResenaCreate, ResenaUpdate, ResenaResponse, ResenaListResponse
from app.crud.resena_crud import ResenaCRUD
from app.core.auth import get_current_user
from app.core.cloudinary_service import upload_image
from datetime import datetime
from jose import JWTError, jwt
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import UploadFile, File
from app.core.config import settings
import logging

router = APIRouter(prefix="/resenas", tags=["Reseñas"])
security = HTTPBearer()


async def extract_token_info(credentials: HTTPAuthorizationCredentials = Depends(security)) -> tuple:
    """
    Extrae la información del token OAuth (emisión, caducidad y el propio token)
    """
    try:
        token = credentials.credentials
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        
        # Extraer timestamps del token
        token_emision = datetime.fromtimestamp(payload.get("iat", datetime.utcnow().timestamp()))
        token_caducidad = datetime.fromtimestamp(payload.get("exp"))
        
        return token_emision, token_caducidad, token
    except JWTError as e:
        logging.error(f"Error al extraer información del token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )


@router.post("/", response_model=ResenaResponse, status_code=status.HTTP_201_CREATED)
async def crear_resena(
    resena_data: ResenaCreate,
    current_user: User = Depends(get_current_user),
    token_info: tuple = Depends(extract_token_info)
):
    """
    Crea una nueva reseña
    Requiere autenticación OAuth
    """
    try:
        token_emision, token_caducidad, token_oauth = token_info
        
        resena = await ResenaCRUD.create(
            resena_data=resena_data,
            email_autor=current_user.email,
            nombre_autor=current_user.name,
            token_emision=token_emision,
            token_caducidad=token_caducidad,
            token_oauth=token_oauth
        )
        
        logging.info(f"Reseña creada por {current_user.email}: {resena.id}")
        
        # Convertir a ResenaResponse
        return ResenaResponse(
            _id=str(resena.id),
            nombre_establecimiento=resena.nombre_establecimiento,
            direccion=resena.direccion,
            latitud=resena.latitud,
            longitud=resena.longitud,
            valoracion=resena.valoracion,
            email_autor=resena.email_autor,
            nombre_autor=resena.nombre_autor,
            token_emision=resena.token_emision,
            token_caducidad=resena.token_caducidad,
            token_oauth=resena.token_oauth,
            imagenes=resena.imagenes,
            created_at=resena.created_at
        )
    except Exception as e:
        logging.error(f"Error al crear reseña: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear la reseña: {str(e)}"
        )


@router.get("/", response_model=ResenaListResponse)
async def listar_resenas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    email_autor: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """
    Lista todas las reseñas con paginación
    Si se proporciona email_autor, filtra por ese autor
    Requiere autenticación OAuth
    """
    try:
        resenas = await ResenaCRUD.get_all(skip=skip, limit=limit, email_autor=email_autor)
        total = await ResenaCRUD.count(email_autor=email_autor)
        
        resenas_response = [
            ResenaResponse(
                _id=str(r.id),
                nombre_establecimiento=r.nombre_establecimiento,
                direccion=r.direccion,
                latitud=r.latitud,
                longitud=r.longitud,
                valoracion=r.valoracion,
                email_autor=r.email_autor,
                nombre_autor=r.nombre_autor,
                token_emision=r.token_emision,
                token_caducidad=r.token_caducidad,
                token_oauth=r.token_oauth,
                imagenes=r.imagenes,
                created_at=r.created_at
            )
            for r in resenas
        ]
        
        return ResenaListResponse(resenas=resenas_response, total=total)
    except Exception as e:
        logging.error(f"Error al listar reseñas: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar reseñas: {str(e)}"
        )


@router.get("/mis-resenas", response_model=ResenaListResponse)
async def mis_resenas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_user)
):
    """
    Lista las reseñas del usuario autenticado
    Requiere autenticación OAuth
    """
    return await listar_resenas(skip=skip, limit=limit, email_autor=current_user.email, current_user=current_user)


@router.get("/establecimiento/{nombre}", response_model=List[ResenaResponse])
async def buscar_por_establecimiento(
    nombre: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_user)
):
    """
    Busca reseñas por nombre del establecimiento (búsqueda parcial)
    Requiere autenticación OAuth
    """
    try:
        resenas = await ResenaCRUD.get_by_establecimiento(nombre, skip=skip, limit=limit)
        
        return [
            ResenaResponse(
                _id=str(r.id),
                nombre_establecimiento=r.nombre_establecimiento,
                direccion=r.direccion,
                latitud=r.latitud,
                longitud=r.longitud,
                valoracion=r.valoracion,
                email_autor=r.email_autor,
                nombre_autor=r.nombre_autor,
                token_emision=r.token_emision,
                token_caducidad=r.token_caducidad,
                token_oauth=r.token_oauth,
                imagenes=r.imagenes,
                created_at=r.created_at
            )
            for r in resenas
        ]
    except Exception as e:
        logging.error(f"Error al buscar reseñas por establecimiento: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar reseñas: {str(e)}"
        )


@router.get("/ubicacion", response_model=List[ResenaResponse])
async def buscar_por_ubicacion(
    latitud: float = Query(..., ge=-90, le=90),
    longitud: float = Query(..., ge=-180, le=180),
    radio_km: float = Query(5.0, ge=0.1, le=100),
    current_user: User = Depends(get_current_user)
):
    """
    Busca reseñas cercanas a una ubicación
    Requiere autenticación OAuth
    """
    try:
        resenas = await ResenaCRUD.get_by_location(latitud, longitud, radio_km)
        
        return [
            ResenaResponse(
                _id=str(r.id),
                nombre_establecimiento=r.nombre_establecimiento,
                direccion=r.direccion,
                latitud=r.latitud,
                longitud=r.longitud,
                valoracion=r.valoracion,
                email_autor=r.email_autor,
                nombre_autor=r.nombre_autor,
                token_emision=r.token_emision,
                token_caducidad=r.token_caducidad,
                token_oauth=r.token_oauth,
                imagenes=r.imagenes,
                created_at=r.created_at
            )
            for r in resenas
        ]
    except Exception as e:
        logging.error(f"Error al buscar reseñas por ubicación: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar reseñas por ubicación: {str(e)}"
        )


@router.get("/valoracion", response_model=List[ResenaResponse])
async def buscar_por_valoracion(
    min_valoracion: float = Query(0, ge=0, le=5),
    max_valoracion: float = Query(5, ge=0, le=5),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_user)
):
    """
    Busca reseñas por rango de valoración
    Requiere autenticación OAuth
    """
    try:
        if min_valoracion > max_valoracion:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="min_valoracion no puede ser mayor que max_valoracion"
            )
        
        resenas = await ResenaCRUD.get_by_valoracion(min_valoracion, max_valoracion, skip, limit)
        
        return [
            ResenaResponse(
                _id=str(r.id),
                nombre_establecimiento=r.nombre_establecimiento,
                direccion=r.direccion,
                latitud=r.latitud,
                longitud=r.longitud,
                valoracion=r.valoracion,
                email_autor=r.email_autor,
                nombre_autor=r.nombre_autor,
                token_emision=r.token_emision,
                token_caducidad=r.token_caducidad,
                token_oauth=r.token_oauth,
                imagenes=r.imagenes,
                created_at=r.created_at
            )
            for r in resenas
        ]
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error al buscar reseñas por valoración: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar reseñas por valoración: {str(e)}"
        )


@router.get("/{resena_id}", response_model=ResenaResponse)
async def obtener_resena(
    resena_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Obtiene una reseña por su ID
    Requiere autenticación OAuth
    """
    try:
        resena = await ResenaCRUD.get_by_id(PydanticObjectId(resena_id))
        
        if not resena:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reseña no encontrada"
            )
        
        return ResenaResponse(
            _id=str(resena.id),
            nombre_establecimiento=resena.nombre_establecimiento,
            direccion=resena.direccion,
            latitud=resena.latitud,
            longitud=resena.longitud,
            valoracion=resena.valoracion,
            email_autor=resena.email_autor,
            nombre_autor=resena.nombre_autor,
            token_emision=resena.token_emision,
            token_caducidad=resena.token_caducidad,
            token_oauth=resena.token_oauth,
            imagenes=resena.imagenes,
            created_at=resena.created_at
        )
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error al obtener reseña: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener reseña: {str(e)}"
        )


@router.put("/{resena_id}", response_model=ResenaResponse)
async def actualizar_resena(
    resena_id: str,
    resena_data: ResenaUpdate,
    current_user: User = Depends(get_current_user)
):
    """
    Actualiza una reseña
    Solo el autor puede actualizar su reseña
    Requiere autenticación OAuth
    """
    try:
        resena = await ResenaCRUD.update(
            resena_id=PydanticObjectId(resena_id),
            resena_data=resena_data,
            email_autor=current_user.email
        )
        
        if not resena:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reseña no encontrada o no tienes permisos para actualizarla"
            )
        
        logging.info(f"Reseña {resena_id} actualizada por {current_user.email}")
        
        return ResenaResponse(
            _id=str(resena.id),
            nombre_establecimiento=resena.nombre_establecimiento,
            direccion=resena.direccion,
            latitud=resena.latitud,
            longitud=resena.longitud,
            valoracion=resena.valoracion,
            email_autor=resena.email_autor,
            nombre_autor=resena.nombre_autor,
            token_emision=resena.token_emision,
            token_caducidad=resena.token_caducidad,
            token_oauth=resena.token_oauth,
            imagenes=resena.imagenes,
            created_at=resena.created_at
        )
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error al actualizar reseña: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar reseña: {str(e)}"
        )


@router.delete("/{resena_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_resena(
    resena_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Elimina una reseña
    Solo el autor puede eliminar su reseña
    Requiere autenticación OAuth
    """
    try:
        deleted = await ResenaCRUD.delete(
            resena_id=PydanticObjectId(resena_id),
            email_autor=current_user.email
        )
        
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reseña no encontrada o no tienes permisos para eliminarla"
            )
        
        logging.info(f"Reseña {resena_id} eliminada por {current_user.email}")
        return None
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error al eliminar reseña: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar reseña: {str(e)}"
        )


@router.post("/upload-image", response_model=dict)
async def upload_resena_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """
    Subir una imagen a Cloudinary (requiere autenticación)
    
    Returns:
        {"url": "https://res.cloudinary.com/..."}
    """
    # Validar tipo de archivo
    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo debe ser una imagen"
        )
    
    # Validar tamaño (max 10MB)
    file_content = await file.read()
    if len(file_content) > 10 * 1024 * 1024:  # 10MB
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La imagen no puede superar los 10MB"
        )
    
    try:
        url = await upload_image(file_content, file.filename or "resena.jpg")
        return {"url": url}
    except Exception as e:
        logging.error(f"Error al subir imagen: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al subir imagen: {str(e)}"
        )
