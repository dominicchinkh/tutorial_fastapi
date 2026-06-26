from fastapi import APIRouter, Depends, Path, Query
from pydantic import AfterValidator, BaseModel, Field
from typing import Annotated, Literal

# from ..dependencies import get_token_header

router = APIRouter(
    prefix="/query",
    tags=[
        "query"
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

#--------------
# Query string

# Note: `short` can be 1, True, true, on, yes
# Note: when you want to make a query parameter required (e.g. `needy`), you can just not declare any default value

@router.get("/items/{item_id}")
async def read_query_items(
    # item_id: str, 
    
    item_id: Annotated[
        int, 
        Path(
            title="The ID of the item to get", 
            ge=1    # item_id will need to be an integer number "greater than or equal" to 1
        )],
    
    needy: str, 
    q: str | None = None, 
    short: bool = False
):
    item = {"item_id": item_id, "needy": needy}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

#---------------------------------
# Query parameters and validation

def check_valid_id(id: str):
    if not id.startswith(("isbn-")):
        raise ValueError('Invalid ID format, it must start with "isbn-"')
    return id

@router.get("/items")
async def read_query_items_with_validation(
    # q: str | None = None
    
    q1: Annotated[str, Query(min_length=3)], # q1 is required, must be `str`
    
    q2: Annotated[str | None, Query(min_length=3)], # q2 is required, can be `None`
    
    q3: Annotated[str | None, Query(min_length=3)] = 'query', # q3 is optional. The default value is `query`. 
    
    q4: Annotated[str | None,
                Query(
                    min_length=3,       # Whenever it is provided, its length doesn't less than 3 characters.
                    max_length=50,      # Whenever it is provided, its length doesn't exceed 50 characters.
                    pattern="^query$"   # A regular expression pattern that the parameter should match.
                )] = None,              # q4 is optional. The default value is `None`.
    
    q5: Annotated[list[str] | None, Query()] = None, # q5 that can appear multiple times in the URL
    
    q6: Annotated[list[str], Query()] = ["foo", "bar"],
    
    id: Annotated[str | None, AfterValidator(check_valid_id)] = None, # With customer validator
):
    results = {"items": [
        {"id": id}, {"q1": q1}, {"q2": q2}, {"q3": q3}, {"q4": q4}, {"q5": q5}, {"q6": q6}]
    }
    return results

#------------------------
# Query parameters model

class FilterParams(BaseModel):
    model_config = {"extra": "forbid"} # forbid any extra fields
    
    limit:    int = Field(100, gt=0, le=100)
    offset:   int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags:     list[str] = []

@router.get("/items/model")
async def read_query_items_with_model(filter_query: Annotated[FilterParams, Query()]):
    return filter_query
