import os
from fastapi import FastAPI, UploadFile, File, Form, APIRouter
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
# from ..models.melody.music_vae_model import MusicGeneratorVAE

class UploadForm(BaseModel):
    beamsize: int
    temperature: float
    branchFactor: int
    notes: str
    totalSteps: int

melody_router = APIRouter()
# music_generator = MusicGeneratorVAE()

@melody_router.post("/upload-music")
async def create_upload_file(file: UploadFile = File(...),
                beamsize: int = Form(...),
                temperature: float = Form(...),
                branchFactor: int = Form(...),
                notes: str = Form(...),
                totalSteps: int = Form(...)):
    
    if not os.path.exists('music'):
        os.makedirs("music")
        file_location = os.path.join("music", file.filename)
        with open(file_location, "wb") as buffer:
            buffer.write(await file.read())
    else:
        file_location = os.path.join("music", file.filename)
        with open(file_location, "wb") as buffer:
            buffer.write(await file.read())  
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "beamsize": beamsize,
        "temperature": temperature,
        "branchFactor": branchFactor,
        "notes": notes,
        "totalSteps": totalSteps
    }


