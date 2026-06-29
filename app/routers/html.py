from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse

# from ..dependencies import get_token_header

router = APIRouter(
    prefix="/html",
    tags=[
        "html"
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

@router.get("/items", response_class=HTMLResponse)
async def read_items():
    return """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """

# You can also override the response directly in your path operation, by returning it.

# @router.get("/items")
# async def read_items():
#     html_content = """
#     <html>
#         <head>
#             <title>Some HTML in here</title>
#         </head>
#         <body>
#             <h1>Look ma! HTML!</h1>
#         </body>
#     </html>
#     """
#     return HTMLResponse(content=html_content, status_code=200)
