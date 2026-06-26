from pydantic import BaseModel

class FormData(BaseModel):
    model_config = {"extra": "forbid"} # Forbid any extra fields
    
    username: str
    password: str
