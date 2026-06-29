from fastapi import APIRouter, Depends
from typing import Annotated

from ..config import get_settings, Settings
# from ..dependencies import get_token_header

router = APIRouter(
    prefix="/home",
    tags=[
        "home"
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

@router.get("")
def home(settings: Annotated[Settings, Depends(get_settings)]):
    return {"Hello": "World"}
