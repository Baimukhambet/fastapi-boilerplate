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

class UpdateAccountRequest(AppModel):
    name: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    city: Optional[str]
    password: Optional[str]



@router.patch("/users/me")
def update_my_account(
    input: UpdateAccountRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    user = svc.repository.get_user_by_id(jwt_data.user_id)

    # if svc.repository.get_user_by_email(input["email"]):
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Email is already taken.",
    #     )

    svc.repository.update_user_by_id(jwt_data.user_id, input.dict(exclude_unset=True))
    return {"user": "updated"}
