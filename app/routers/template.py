from pathlib import Path
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# from ..dependencies import get_token_header

router = APIRouter(
    prefix="/template",
    tags=[
        "template"
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

router.mount("/static", StaticFiles(directory="static"), name="static")

#----------
# Template

# Dynamically find the templates folder

# `__file__` is this current route file.
# `.resolve().parents.parent` goes up TWO levels (from routers/ -> app/)

BASE_DIR = Path(__file__).resolve().parent.parent 
TEMPLATES_DIR = BASE_DIR / "templates"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

@router.get("/items/{id}", response_class=HTMLResponse)
async def read_template_item(request: Request, id: str):
    return templates.TemplateResponse(
        request=request, name="item.html", context={"id": id}
    )
