from fastapi import APIRouter, Depends
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
def home():
    return {"Hello": "World"}
