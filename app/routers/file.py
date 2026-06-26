from fastapi import APIRouter, Depends, File, UploadFile
from typing import Annotated

# from ..dependencies import get_token_header

router = APIRouter(
    prefix="/file",
    tags=[
        "file"
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

#------
# File

@router.post("/bytes")
async def create_file_with_bytes(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}

@router.post("/bytes/multiple")
async def create_multiple_files_with_bytes(files: Annotated[list[bytes], File()]):
    return {"file_sizes": [len(file) for file in files]}

# Using UploadFile has several advantages over bytes

#   1. A file stored in memory up to a maximum size limit, and after passing 
#      this limit it will be stored on disk. This means that it will work well 
#      for large files like images, videos, large binaries, etc. without consuming 
#      all the memory.

#   2. You can get metadata from the uploaded file. It has a file-like async interface.
#      (https://fastapi.tiangolo.com/tutorial/request-files/#uploadfile)


@router.post("")
async def create_file_with_upload_file(file: UploadFile):
    return {"filename": file.filename}

@router.post("/multiple")
async def create_multiple_files_upload_file(files: list[UploadFile]):
    return {"filenames": [file.filename for file in files]}
