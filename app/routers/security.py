import jwt
import secrets

from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.security import (
    HTTPBasic, HTTPBasicCredentials,
    OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes
)

from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import ValidationError
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

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={
        "me": "Read information about the current user.",
        "items": "Read items."
    },
)

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

async def get_current_user(
    security_scopes: SecurityScopes, 
    token: Annotated[str, Depends(oauth2_scheme)]
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
        
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
        
        scope: str = payload.get("scope", "")
        token_scopes = scope.split(" ")
        
        token_data = TokenData(scopes=token_scopes, username=username)
        
    except (InvalidTokenError, ValidationError):
        raise credentials_exception
    
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user

async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    return current_user

@router.get("/users/me")
async def read_current_user(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user

@router.get("/users/me/active")
async def read_current_active_user(
    current_user: Annotated[User, Security(get_current_user, scopes=["me"])],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    
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
        data = {
            "sub": user.username, "scope": " ".join(form_data.scopes)
        }, 
        expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")

@router.get("/users/me/items")
async def read_own_items(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["items"])],
):
    return [{"item_id": "Foo", "owner": current_user.username}]

@router.get("/status")
async def read_system_status(current_user: Annotated[User, Depends(get_current_user)]):
    return {"status": "ok"}

# HTTP basic auth

security = HTTPBasic()

def get_current_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    # `secrets.compare_digest()` needs to take bytes or a str that only contains ASCII characters
    # To handle that, we first convert the username and password to bytes encoding them with UTF-8.
    
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"stanley-johnson"
    
    # Use `secrets.compare_digest()` to secure against a type of attacks called `timing attacks`.
    
    # It will take the same time to compare `stanley-john` to `stanley-johnson` than it takes to 
    # compare `john-doe` to `stanley-johnson`.
    
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"swordfish"
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@router.get("/basic-auth/users/me")
def read_basic_auth_current_user(username: Annotated[str, Depends(get_current_username)]):
    return {"username": username}
