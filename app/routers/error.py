from fastapi import APIRouter, Depends, HTTPException, Request
# from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import JSONResponse, PlainTextResponse

# from ..dependencies import get_token_header
from ..exceptions.unicorn import UnicornException

router = APIRouter(
    prefix="/error",
    tags=[
        "error"
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

#-----------------
# Handling errors

items = {
    "foo": {"name": "Foo",                                  "price": 50.2                         },
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62,   "tax": 20.2            },
    "baz": {"name": "Baz", "description": None,             "price": 50.2, "tax": 10.5, "tags": []},
}

@router.get("/items/{item_id}")
async def read_item_with_http_exception(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404, 
            
            # You can pass any value that can be converted to JSON
            detail="Item not found",
            
            # Add optional custom headers to the HTTP error
            headers={"X-Error": "There goes my error"},
        )
    return {"item": items[item_id]}

# Custom exception handler

async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )

@router.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}

# Override HTTPException error handler

# FastAPI's HTTPException error class inherits from Starlette's HTTPException 
# error class. When you register an exception handler, you should register it 
# for Starlette's HTTPException. This way, if any part of Starlette's internal 
# code, or a Starlette extension or plug-in, raises a Starlette HTTPException, 
# your handler will be able to catch and handle it.

async def http_exception_handler(request, exc):

    # Reuse FastAPI's default exception handlers
    # return await http_exception_handler(request, exc)

    return PlainTextResponse(str('Custom exception handler: ' + exc.detail), status_code=exc.status_code)
