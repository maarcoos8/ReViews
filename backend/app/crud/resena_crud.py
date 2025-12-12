from typing import List, Optional
from beanie import PydanticObjectId
from app.models.resena import Resena
from app.schemas.resena import ResenaCreate, ResenaUpdate
from datetime import datetime


class ResenaCRUD:
    """
    CRUD operations para Reseñas
    Separa la lógica de acceso a datos de los endpoints
    """
    
    @staticmethod
    async def create(
        resena_data: ResenaCreate,
        email_autor: str,
        nombre_autor: str,
        token_emision: datetime,
        token_caducidad: datetime,
        token_oauth: str
    ) -> Resena:
        """
        Crea una nueva reseña
        """
        resena = Resena(
            nombre_establecimiento=resena_data.nombre_establecimiento,
            direccion=resena_data.direccion,
            latitud=resena_data.latitud,
            longitud=resena_data.longitud,
            valoracion=resena_data.valoracion,
            email_autor=email_autor,
            nombre_autor=nombre_autor,
            token_emision=token_emision,
            token_caducidad=token_caducidad,
            token_oauth=token_oauth,
            imagenes=resena_data.imagenes
        )
        await resena.insert()
        return resena
    
    @staticmethod
    async def get_all(
        skip: int = 0,
        limit: int = 100,
        email_autor: Optional[str] = None
    ) -> List[Resena]:
        """
        Obtiene todas las reseñas con paginación
        Si se proporciona email_autor, filtra por ese autor
        """
        query = Resena.find()
        
        if email_autor:
            query = query.find(Resena.email_autor == email_autor)
        
        resenas = await query.skip(skip).limit(limit).to_list()
        return resenas
    
    @staticmethod
    async def count(email_autor: Optional[str] = None) -> int:
        """
        Cuenta el total de reseñas
        Si se proporciona email_autor, cuenta solo las de ese autor
        """
        query = Resena.find()
        
        if email_autor:
            query = query.find(Resena.email_autor == email_autor)
        
        return await query.count()
    
    @staticmethod
    async def get_by_id(resena_id: PydanticObjectId) -> Optional[Resena]:
        """
        Obtiene una reseña por su ID
        """
        return await Resena.get(resena_id)
    
    @staticmethod
    async def get_by_establecimiento(
        nombre_establecimiento: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Resena]:
        """
        Obtiene reseñas por nombre del establecimiento (búsqueda parcial)
        """
        resenas = await Resena.find(
            Resena.nombre_establecimiento.contains(nombre_establecimiento, case_insensitive=True)
        ).skip(skip).limit(limit).to_list()
        return resenas
    
    @staticmethod
    async def get_by_location(
        latitud: float,
        longitud: float,
        radio_km: float = 5.0
    ) -> List[Resena]:
        """
        Obtiene reseñas cercanas a una ubicación
        Nota: Implementación básica. Para producción, usar índices geoespaciales de MongoDB
        """
        # Aproximación básica: 1 grado ≈ 111 km
        delta = radio_km / 111.0
        
        resenas = await Resena.find(
            Resena.latitud >= latitud - delta,
            Resena.latitud <= latitud + delta,
            Resena.longitud >= longitud - delta,
            Resena.longitud <= longitud + delta
        ).to_list()
        
        return resenas
    
    @staticmethod
    async def update(
        resena_id: PydanticObjectId,
        resena_data: ResenaUpdate,
        email_autor: str
    ) -> Optional[Resena]:
        """
        Actualiza una reseña
        Solo el autor puede actualizarla
        """
        resena = await Resena.get(resena_id)
        
        if not resena or resena.email_autor != email_autor:
            return None
        
        update_data = resena_data.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(resena, field, value)
        
        await resena.save()
        return resena
    
    @staticmethod
    async def delete(
        resena_id: PydanticObjectId,
        email_autor: str
    ) -> bool:
        """
        Elimina una reseña
        Solo el autor puede eliminarla
        """
        resena = await Resena.get(resena_id)
        
        if not resena or resena.email_autor != email_autor:
            return False
        
        await resena.delete()
        return True
    
    @staticmethod
    async def get_by_valoracion(
        min_valoracion: float = 0,
        max_valoracion: float = 5,
        skip: int = 0,
        limit: int = 100
    ) -> List[Resena]:
        """
        Obtiene reseñas por rango de valoración
        """
        resenas = await Resena.find(
            Resena.valoracion >= min_valoracion,
            Resena.valoracion <= max_valoracion
        ).skip(skip).limit(limit).to_list()
        
        return resenas
