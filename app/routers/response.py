from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import JSONResponse, RedirectResponse
from typing import Any

# from ..dependencies import get_token_header
from ..models.item import CarItem, Item, PlaneItem
from ..models.message import Message
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

# if you want the maximum performance, use a Response Model and don't declare 
# a response_class in the path operation decorator

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

@router.get(
    "/users/{user_name}", 
    response_model=UserOut,
    responses={
        404: {
            "model": Message, 
            "description": "The user was not found"
        },
        200: {
            "description": "User requested by ID",
            "content": {
                "application/json": {
                    "example": {"id": 1, "username": "bar"}
                }
            },
        },
    },
)
async def read_user(user_name: str) -> Any:
    
    if user_name == "roo":
        raise HTTPException(
            status_code=404, 
            detail="Item not found"
        )
    return {"username": user_name, "email": user_name + "@example.com"}

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

# Change status code

tasks = {"foo": "Listen to the Bar Fighters"}

@router.put("/tasks/{task_id}", status_code=200)
def get_or_create_task(task_id: str, response: Response):
    if task_id not in tasks:
        tasks[task_id] = "This didn't exist before"
        response.status_code = status.HTTP_201_CREATED
    return tasks[task_id]
