from fastapi import APIRouter, Cookie, Depends, Header, HTTPException
from typing import Annotated

# from ..dependencies import get_token_header

router = APIRouter(
    prefix="/dependency",
    tags=[
        "dependency"
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

#------------
# Dependency

async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

CommonsDep = Annotated[dict, Depends(common_parameters)]

@router.get("/items")
async def read_items_with_dependency(commons: CommonsDep):
    return commons

@router.get("/users")
async def read_users_with_dependency(commons: CommonsDep):
    return commons

# Classes as dependency

class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

@router.get("/items/class-dependency")
async def read_items_with_class_dependency(commons: Annotated[CommonQueryParams, Depends()]):
    return commons

# Sub-dependencies

def query_extractor(q: str | None = None):
    return q

def query_or_cookie_extractor(
    q: Annotated[str, Depends(query_extractor)],
    last_query: Annotated[str | None, Cookie()] = None,
):
    if not q:
        return last_query
    return q

@router.get("/items/sub-dependencies")
async def read_items_with_sub_dependencies(
    query_or_default: Annotated[str, Depends(query_or_cookie_extractor)],
):
    return {"q_or_cookie": query_or_default}

# Dependencies

async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key

@router.get("/items/dependencies", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items_with_dependencies():
    return [{"item": "Foo"}, {"item": "Bar"}]

# Add dependencies to the whole application
# app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])

# Dependencies with yield

class DBSession:
    pass

async def get_db():
    
    # The yielded value is what is injected into path operations and other dependencies
    db = DBSession()
    try:
        yield db
    
    # You can also use except to catch the exception that was raised and do something with it
    except HTTPException as e:
        # If you don't raise it again (or raise a new exception), FastAPI won't be able to 
        # notice there was an exception
        raise Exception(status_code=400, detail=f"HTTP error: {e}")
    
    # The code following the yield statement is executed after the response
    finally:
        db.close()
