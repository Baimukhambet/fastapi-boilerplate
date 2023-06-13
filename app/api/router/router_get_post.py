from typing import Any

from fastapi import Depends, Response
from pydantic import Field

from app.utils import AppModel

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data


class GetPostResponse(AppModel):
    id: Any = Field(alias="_id")
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str
    user_id: Any


@router.get("/posts/{post_id:str}", response_model=GetPostResponse)
def get_post(
    post_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    post = svc.repository.get_post_by_id(post_id)
    if not post: 
        return Response(status_code=404)
    return GetPostResponse(**post)
