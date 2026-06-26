
from fastapi.encoders import jsonable_encoder
from typing import Annotated

from fastapi import APIRouter, Body, Depends

# from ..dependencies import get_token_header
from ..models.item import Item
from ..models.user import User

router = APIRouter(
    prefix="/body",
    tags=[
        "body"
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

#--------------------------
# Multiple body parameters

items = {
    "foo": {"name": "Foo",                                  "price": 50.2                         },
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62,   "tax": 20.2            },
    "baz": {"name": "Baz", "description": None,             "price": 50.2, "tax": 10.5, "tags": []},
}

# FastAPI will expect a body like
#   {
#       "item": {
#           "name": "Foo",
#           "description": "The pretender",
#           "price": 42.0,
#           "tax": 3.2
#       },
#       "user": {
#           "username": "John",
#           "full_name": "John Smith"
#       },
#       "importance": 5
#   }

# Replacing `item`

@router.put("/items/{item_id}")
async def replace_item_with_body(
    item_id: int, 
    item: Item, 
    user: User, 
    importance: Annotated[int, Body()] # You can instruct FastAPI to treat it as another body key
):
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    return update_item_encoded

# Partial update `item`

@router.patch("/items/{item_id}")
async def update_item_with_body(item_id: str, item: Item) -> Item:
    
    # Retrieve the stored data
    stored_item_data  = items[item_id]
    
    # Put that data in a Pydantic model
    stored_item_model = Item(**stored_item_data)
    
    # Generate a `dict` without default values from the input model (using `exclude_unset``)
    update_data = item.model_dump(exclude_unset=True)
    
    # Create a copy of the stored model, updating its attributes with the received partial updates
    updated_item = stored_item_model.model_copy(update=update_data)

    # Convert the copied model to something that can be stored in your DB
    items[item_id] = jsonable_encoder(updated_item)
    
    # Return the updated model
    return updated_item

# FastAPI will expect a body like
#   {
#       "item": {
#           "name": "Foo",
#           "description": "The pretender",
#           "price": 42.0,
#           "tax": 3.2
#       }
#   }

@router.put("/items/{item_id}/embedded")
async def update_item_with_embedded_body(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results

#--------------------------
# Body with arbitrary dict

@router.post("/dict")
async def create_with_arbitrary_dict(weights: dict[int, float]):
    return weights
