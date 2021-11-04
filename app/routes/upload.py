"""
This script is used post a file to a remote endpoint.

Author: Victor Moreno Marin
Date: 03/11/2021
"""

# FastAPI and Pydantic libraries
from fastapi import APIRouter, File, UploadFile
from pydantic import HttpUrl
# import requests

# ApiRouter instance
upload = APIRouter()


# Post a file
@upload.post("/", callbacks=upload.routes, tags=["Upload file to Guane"])
async def create_upload_file(
    file: UploadFile = File(...),
    callback_url: HttpUrl = "https://gttb.guane.dev/api/files"
        ):
    """
    Upload a file.

    This function post a file to a remote endpoint.

    Parameters:
        - file: UploadFile -> File to post.
        - callback_url: HttpUrl -> Url to remote endpoint

    Returns a file name.
    """
    # requests.post(callback_url,file.file)
    return {"filename": file.filename}
