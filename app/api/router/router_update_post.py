from fastapi import Depends, HTTPException, status
from pydantic import Field
from typing import Optional

from app.utils import AppModel

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data


# class GetMyAccountResponse(AppModel):
#     id: Any = Field(alias="_id")
#     email: str

class UpdatePostRequest(AppModel):
    type: Optional[str]
    price: Optional[int]
    address: Optional[str]
    area: Optional[float]
    rooms_count: Optional[int]
    description: Optional[str]



@router.patch("/posts/{post_id:str}")
def update_post(
    input: UpdatePostRequest,
    post_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    
    svc.repository.update_post_by_id(post_id, input.dict(exclude_unset=True))

    return {"updated": "true"}
