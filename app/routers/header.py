from fastapi import APIRouter, Depends, Header
from pydantic import BaseModel
from typing import Annotated

# from ..dependencies import get_token_header

router = APIRouter(
    prefix="/header",
    tags=[
        "header"
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

#--------
# Header

@router.get("/items")
async def read_header_items(
    user_agent: Annotated[
        str | None,
        Header()
    ],
    
    x_token: Annotated[
        list[str] | None,  # `x-token` can appear more than once
        
        # By default, Header will convert the parameter names characters from 
        # underscore (_) to hyphen (-). If for some reason you need to disable 
        # automatic conversion of underscores to hyphens, set the parameter 
        # `convert_underscores`` of Header to False
        
        Header(convert_underscores=False) 
    ] = None):
    
    return {"X-token": x_token}

class CommonHeaders(BaseModel):
    model_config = {"extra": "forbid"} # Forbid any extra fields
    
    host: str
    save_data: bool
    if_modified_since: str | None = None
    trace_parent: str | None = None
    x_tag: list[str] = []
    
@router.get("/items/model")
async def read_header_items_with_model(headers: Annotated[CommonHeaders, Header()]):
    return headers
