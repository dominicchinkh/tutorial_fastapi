from fastapi import APIRouter, Depends, status

# from ..dependencies import get_token_header

router = APIRouter(
    prefix="/status",
    tags=[
        "status"
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

#-------------
# Status code

@router.post("/items", status_code=status.HTTP_201_CREATED)
async def create_item_with_status(name: str):
    return {"name": name}

