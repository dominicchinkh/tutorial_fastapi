from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from starlette.exceptions import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from .exception.unicorn import UnicornException
from .middleware.process_time import add_process_time_header
from .routers import (
    background_task, body, cookie, database, dependency, enumeration, error, file, frontend, form,  
    header, home, json_lines, model, query, response, security, server_side_event, status
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ---- Startup Logic ----
    # This runs BEFORE the application starts taking requests
    database.create_db_and_tables() 
    
    yield  # The app runs while paused here
    
    # ---- Shutdown Logic ----
    # This runs AFTER the application finishes handling requests (optional)
    # e.g., close_db_connection()
    pass

description = """
FastAPI demo API helps you do awesome stuff. 🚀

## Items
You can **read items**.

## Users
You will be able to:

* **Create users**.
* **Read users**.
"""

app = FastAPI(
    title            = "FastAPI demo app",
    description      = description,
    summary          = "This app is for demo FastAPI features",
    version          = "0.0.1",
    terms_of_service = "https://www.apache.org/licenses/LICENSE-2.0.html",
    contact          = {
        "name":  "Dominic",
        "url":   "https://github.com/dominicchinkh",
        "email": "dominicchinkh@gmail.com",
    },
    license_info     = {
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags     = [
        {
            "name": "home",
            "description": "Home is where the heart is",
        },  
    ],
    lifespan=lifespan
)

#-------
# Route

app.include_router(home.router)
app.include_router(background_task.router)
app.include_router(body.router)
app.include_router(cookie.router)
app.include_router(database.router)
app.include_router(dependency.router)
app.include_router(enumeration.router)
app.include_router(error.router)
app.include_router(file.router)
app.include_router(form.router)
app.include_router(frontend.router)
app.include_router(header.router)
app.include_router(json_lines.router)
app.include_router(model.router)
app.include_router(query.router)
app.include_router(response.router)
app.include_router(security.router)
app.include_router(server_side_event.router)
app.include_router(status.router)

#-------------------
# Exception handler

app.add_exception_handler(UnicornException, error.unicorn_exception_handler)
app.add_exception_handler(HTTPException, error.http_exception_handler)

#------------
# Middleware

app.add_middleware(BaseHTTPMiddleware, add_process_time_header)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#-------------
# Static file

app.mount("/static", StaticFiles(directory="static"), name="static")
