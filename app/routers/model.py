from fastapi import APIRouter, Depends

# from ..dependencies import get_token_header
from ..models.item import Item

router = APIRouter(
    prefix="/model",
    tags=[
        "model"
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

#-------
# Model

@router.post("/items")
async def create_item_with_model(item: Item):
    return item

@router.post("/items/multiple")
async def create_multiple_items_with_model(items: list[Item]):
    return items
