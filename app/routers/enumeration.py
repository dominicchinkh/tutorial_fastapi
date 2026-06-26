from enum import Enum
from fastapi import APIRouter, Depends

# from ..dependencies import get_token_header

router = APIRouter(
    prefix="/enumeration",
    tags=[
        "enumeration"
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
# Enumeration

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet  = "resnet"
    lenet   = "lenet"

@router.get("/{model_name}")
async def get_enumeration_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}
