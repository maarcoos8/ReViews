from bson import ObjectId
from fastapi import HTTPException, status

def ensure_object_id(value: str, *, field: str = "id") -> None:
    if not ObjectId.is_valid(value):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{field} no es un ObjectId válido",
        )
