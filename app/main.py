from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.staticfiles import StaticFiles

from starlette.exceptions import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from .exceptions.unicorn import UnicornException
from .experiment import youtube_downloader
from .middlewares.process_time import add_process_time_header
from .models.subscription import Subscription
from .routers import (
    background_task, body, callback, cookie, database, dependency, enumeration, error, file, frontend,
    form, header, html, home, json_lines, model, query, request, response, security, server_side_event, 
    status, stream, template, websocket
)
from .subapi import subapi

ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ---- Startup Logic ----
    # This runs BEFORE the application starts taking requests
    database.create_db_and_tables() 
    
    # Load the ML model
    ml_models["answer_to_everything"] = "fake_answer_to_everything_ml_model"
        
    yield  # The app runs while paused here
    
    # ---- Shutdown Logic ----
    # This runs AFTER the application finishes handling requests (optional)
    # e.g., close_db_connection()
    
    # Clean up the ML models and release the resources
    ml_models.clear()    

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

#-----------------
# Sub application

app.mount("/subapi", subapi)

#-------
# Route

app.include_router(home.router)
app.include_router(background_task.router)
app.include_router(body.router)
app.include_router(callback.router)
app.include_router(cookie.router)
app.include_router(database.router)
app.include_router(dependency.router)
app.include_router(enumeration.router)
app.include_router(error.router)
app.include_router(file.router)
app.include_router(form.router)
app.include_router(frontend.router)
app.include_router(header.router)
app.include_router(html.router)
app.include_router(json_lines.router)
app.include_router(model.router)
app.include_router(query.router)
app.include_router(request.router)
app.include_router(response.router)
app.include_router(security.router)
app.include_router(server_side_event.router)
app.include_router(status.router)
app.include_router(stream.router)
app.include_router(template.router)
app.include_router(websocket.router)
app.include_router(youtube_downloader.router)

#-------------------
# Exception handler

app.add_exception_handler(UnicornException, error.unicorn_exception_handler)
app.add_exception_handler(HTTPException, error.http_exception_handler)

#------------
# Middleware

app.add_middleware(BaseHTTPMiddleware, add_process_time_header)

app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["127.0.0.1", "localhost", "testserver"]
)

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

#---------
# Webhook

@app.webhooks.post("webhook/new-subscription")
def new_subscription(body: Subscription):
    """
    When a new user subscribes to your service we'll send you a POST request with this
    data to the URL that you register for the event `new-subscription` in the dashboard.
    """
    pass
