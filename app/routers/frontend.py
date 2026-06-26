from fastapi import APIRouter

router = APIRouter()

#----------
# Frontend

router.frontend(
    "/", 
    directory="dist", 
    
    # If there is an index.html file, missing browser navigation paths serve index.html
    fallback="auto"
)
