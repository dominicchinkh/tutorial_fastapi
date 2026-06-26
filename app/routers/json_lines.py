from collections.abc import AsyncIterable, Iterable
from fastapi import APIRouter, Depends

# from ..dependencies import get_token_header
from ..models.item import Item

router = APIRouter(
    prefix="/json-lines",
    tags=[
        "json lines"
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

items = [
    Item(name="Plumb",      description="A multi-purpose household device."),
    Item(name="Portal Gun", description="A portal opening device."),
    Item(name="Mee Box",    description="A box that summons a Mee."),
]

@router.get("/items/stream")
async def stream_items() -> AsyncIterable[Item]:
    for item in items:
        yield item
        
@router.get("/items/stream-no-async")
def stream_items_in_sync() -> Iterable[Item]:
    for item in items:
        yield item
