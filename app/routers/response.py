from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse, RedirectResponse
from typing import Any

# from ..dependencies import get_token_header
from ..models.item import CarItem, Item, PlaneItem
from ..models.user import UserIn, UserOut

router = APIRouter(
    prefix="/response",
    tags=[
        "response"
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

#----------------
# Response model

@router.post("/items", response_model=Item)
async def create_item_with_response_model(item: Item):
    return item

@router.get("/items", response_model=list[Item])
async def read_items_with_response_model():
    return [
        Item(name="Portal Gun", price=42.0),
        Item(name="Plumb", price=32.0),
    ]

@router.post("/users", response_model=UserOut)
async def create_user(user: UserIn) -> Any:
    return user

# Response class

@router.get("/portal")
async def get_portal(teleport: bool = False) -> Response:
    
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=paQ4r1HKFnY")
    
    return JSONResponse(content={"message": "Here's your inter-dimensional portal."})

# Response model with default value

items = {
    "foo": {"name": "Foo",                                  "price": 50.2                         },
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62,   "tax": 20.2            },
    "baz": {"name": "Baz", "description": None,             "price": 50.2, "tax": 10.5, "tags": []},
}

@router.get(
    "/items/{item_id}", 
    response_model=Item, 
    
    # Default values won't be included in the response, only the values actually set

    # You can also use:
    #   response_model_exclude_defaults=True
    #   response_model_exclude_none=True

    response_model_exclude_unset=True
)
async def read_item_with_response_model(item_id: str):
    return items[item_id]

# Union

@router.get(
    "/items/{item_id}/union", 
    
    # Include the most specific type first, followed by the less specific type
    response_model=PlaneItem | CarItem
)
async def read_union_item(item_id: str):
    return items[item_id]

# Response with arbitrary dict

@router.get("/dict", response_model=dict[str, float])
async def read_dict():
    return {"foo": 2.3, "bar": 3.4}

