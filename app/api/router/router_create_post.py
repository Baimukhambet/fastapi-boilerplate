from fastapi import Depends, HTTPException, status
from typing import Any
from pydantic import Field
from app.utils import AppModel
from ..adapters.jwt_service import JWTData
from ..service import Service, get_service

from . import router
from .dependencies import parse_jwt_user_data


class CreatePostRequest(AppModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str


class CreatePostResponse(AppModel):
    id: Any = Field(alias="_id")


@router.post(
    "/posts", status_code=status.HTTP_201_CREATED,

)
def create_post(
    input: CreatePostRequest,
    svc: Service = Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
):
    # if svc.repository.get_user_by_email(input.email):
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Email is already taken.",
    #     )

    post = svc.repository.create_post(jwt_data.user_id, input.dict())

    return CreatePostResponse(id=post)