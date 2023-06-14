from fastapi import Depends, UploadFile

from typing import Optional, List

from app.utils import AppModel

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data


# class GetMyAccountResponse(AppModel):
#     id: Any = Field(alias="_id")
#     email: str


@router.patch("/posts/{post_id:str}/media")
def post_media(
    files: List[UploadFile],
    post_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    
    result = List[str]
    for file in files:
        url = svc.s3_service.upload_file(file.file, file.filename)
        result.append(url)
    media = {"media": result}
    svc.repository.update_post_by_id(post_id,
                                    media(exclude_unset=True),
                                    jwt_data.user_id)

    return {"posted_media": "true"}
