from fastapi import APIRouter, Depends, Form
from typing import Annotated

# from ..dependencies import get_token_header
from ..models.form_data import FormData

router = APIRouter(
    prefix="/form",
    tags=[
        "form"
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

#------
# Form

@router.post("/login")
async def login(
    username: Annotated[str, Form()], 
    password: Annotated[str, Form()]
):
    return {"username": username}

@router.post("/login/model")
async def login_with_model(data: Annotated[FormData, Form()]):
    return data
