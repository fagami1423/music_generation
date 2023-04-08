import os
from fastapi import FastAPI, File, UploadFile, APIRouter
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
# from ..models.melody.music_vae_model import MusicGeneratorVAE

melody_router = APIRouter()
# music_generator = MusicGeneratorVAE()

@melody_router.post("/generate-music")
async def generate_music(file: UploadFile = File(...)):
    """
        Uploads a music file to the music folder
        returns the filename and status code

    """
    target_dir = "models/melody/primers"
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        file_location = os.path.join(target_dir, file.filename)
        with open(file_location, "wb") as buffer:
            buffer.write(await file.read())
    else:
        file_location = os.path.join("music", file.filename)
        with open(file_location, "wb") as buffer:
            buffer.write(await file.read()) 
     
    return {"filename": file.filename,"status":200}


