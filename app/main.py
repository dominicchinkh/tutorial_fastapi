import time

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware

from starlette.exceptions import HTTPException as StarletteHTTPException

from .exception.unicorn import UnicornException
from .routers import (
    body, cookie, database, dependency, enumeration, error, file, form, header, home, 
    jsonlines, model, query, response, security, sse, status
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

app = FastAPI(lifespan=lifespan)

app.include_router(home.router)

app.include_router(body.router)
app.include_router(cookie.router)
app.include_router(database.router)
app.include_router(dependency.router)
app.include_router(enumeration.router)
app.include_router(error.router)
app.include_router(file.router)
app.include_router(form.router)
app.include_router(header.router)
app.include_router(jsonlines.router)
app.include_router(model.router)
app.include_router(query.router)
app.include_router(response.router)
app.include_router(security.router)
app.include_router(sse.router)
app.include_router(status.router)

app.add_exception_handler(UnicornException, error.unicorn_exception_handler)
app.add_exception_handler(StarletteHTTPException, error.http_exception_handler)

#------------
# Middleware

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

#------
# CORS

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
