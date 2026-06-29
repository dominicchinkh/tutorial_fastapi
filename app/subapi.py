from fastapi import FastAPI

subapi = FastAPI()

@subapi.get("/")
def read_hello_world():
    return {"message": "Hello World from sub API"}
