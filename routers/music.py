import os
from fastapi import FastAPI, UploadFile, File, Form, APIRouter
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

music_router = APIRouter()

@music_router.get("/get-music")
def get_music():
    file_list = os.listdir("music")
    files = []
    if file_list:
        file_urls = [{"url":f"/music/{filename}","filename":{filename}} for filename in file_list]
        return {"file_urls": file_urls}
    else:
        return {"error": "No files found in the music folder."}