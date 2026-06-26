from pydantic import BaseModel
from .image import Image

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float = 10.5
    tax: float | None = None
    tags: set[str] = []
    image: Image | None = None # Type can itself be another Pydantic model

class BaseItem(BaseModel):
    description: str
    type: str

class CarItem(BaseItem):
    type: str = "car"

class PlaneItem(BaseItem):
    type: str = "plane"
    size: int
