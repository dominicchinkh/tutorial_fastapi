from fastapi import APIRouter, Cookie, Depends
from pydantic import BaseModel
from typing import Annotated

# from ..dependencies import get_token_header

router = APIRouter(
    prefix="/cookie",
    tags=[
        "cookie"
    ],
    dependencies=[
        # Depends(get_token_header)
    ],
    responses={
        404: {
            "description": "Not found"
        }
    },
)

#--------
# Cookie

@router.get("/item")
async def read_cookie_item(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}

class Cookies(BaseModel):
    model_config = {"extra": "forbid"} # Forbid any extra fields
    
    session_id: str
    facebook_tracker: str | None = None
    google_tracker: str | None = None
    
@router.get("/item/model")
async def read_cookie_item_with_model(cookies: Annotated[Cookies, Cookie()]):
    return cookies
