import jwt

from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from typing import Annotated

from ..crud.user import UserInDB
# from ..dependencies import get_token_header
from ..models.token import Token, TokenData
from ..models.user import User

router = APIRouter(
    prefix="/security",
    tags=[
        "security"
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

#----------
# Security

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# To get a string like this run:
# openssl rand -hex 32

SECRET_KEY = "21e75d3a7ff161c137dafdc339bfea97a6b54e7caead9ace7a34f16ee79d7739"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

@router.get("/items")
async def read_items_with_security(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

# Get current user

fake_users_db = {
    "john": {
        "username": "john",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fake-hashed-secret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonder",
        "email": "alice@example.com",
        "hashed_password": "fake-hashed-secret2",
        "disabled": True,
    },
}

def fake_hash_password(password: str):
    return "fake-hashed-" + password

password_hash = PasswordHash.recommended()

DUMMY_HASH = password_hash.hash("dummy-password")

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password):
    return password_hash.hash(password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
    
        # When authenticate_user is called with a username that doesn't exist in the 
        # database, we still run verify_password against a dummy hash.

        # This ensures the endpoint takes roughly the same amount of time to respond 
        # whether the username is valid or not, preventing timing attacks that could 
        # be used to enumerate existing usernames.

        verify_password(password, DUMMY_HASH)
        return False
    
    if not verify_password(password, user.hashed_password):
        return False
    
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        
        if username is None:
            raise credentials_exception
        
        token_data = TokenData(username=username)
        
    except InvalidTokenError:
        raise credentials_exception
    
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    
    return user

async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    return current_user

@router.get("/users/me")
async def read_current_user(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user

@router.get("/users/me/active")
async def read_current_active_user(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user

# The form

@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")

@router.get("/users/me/items")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]
