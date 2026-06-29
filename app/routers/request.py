from fastapi import APIRouter, Depends, Request

# from ..dependencies import get_token_header

router = APIRouter(
    prefix="/request",
    tags=[
        "request"
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

#---------
# Request

@router.get("/items/{item_id}")
def read_item(item_id: str, request: Request):
    
    # Refer to https://starlette.dev/requests/ for more options
    client_host = request.client.host
    
    return {"client_host": client_host, "item_id": item_id}
