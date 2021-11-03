from fastapi import APIRouter, File, UploadFile
from pydantic import HttpUrl
# import requests

upload = APIRouter()

@upload.post("/", callbacks=upload.routes, tags=["Upload file to Guane"])
async def create_upload_file(file: UploadFile = File(...), callback_url: HttpUrl="https://gttb.guane.dev/api/files"):
    # requests.post(callback_url,file.file)
    return {"filename": file.filename}
