import os
from fastapi import FastAPI, UploadFile, File, Form, APIRouter
from fastapi.responses import FileResponse, JSONResponse
from magenta.models.performance_rnn import performance_sequence_generator
from pydantic import BaseModel
from models.melody.rnn_model import RNNModel

class UploadForm(BaseModel):
    beamsize: int
    temperature: float
    branchFactor: int
    notes: str
    totalSteps: int
rna_model = RNNModel("pitch_conditioned_performance_with_dynamics")

melody_router = APIRouter()
# music_generator = MusicGeneratorVAE()

@melody_router.post("/upload-music")
async def create_upload_file(file: UploadFile = File(...),
                beamsize: int = Form(...),
                temperature: float = Form(...),
                branchFactor: int = Form(...),
                notes: str = Form(...),
                totalSteps: int = Form(...)):
    
    target_dir = 'models/melody/primers'
    if not os.path.exists('models/melody/primers'):
        os.makedirs(target_dir)
        file_location = os.path.join(target_dir, file.filename)
        with open(file_location, "wb") as buffer:
            buffer.write(await file.read())
    else:
        file_location = os.path.join(target_dir, file.filename)
        with open(file_location, "wb") as buffer:
            buffer.write(await file.read())  
    # print("filename: ",file.filename)
    rna_model.generate(
        "pitch_conditioned_performance_with_dynamics.mag",
        performance_sequence_generator,
        "pitch_conditioned_performance_with_dynamics",
        primer_filename=file.filename,
        pitch_class_histogram="[1, 0, 1, 0, 1, 2, 0, 1, 0, 1, 0, 1]"
    )
    # generate("performance_with_dynamics.mag",performance_sequence_generator,"performance_with_dynamics",primer_filename=file.filename)
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "beamsize": beamsize,
        "temperature": temperature,
        "branchFactor": branchFactor,
        "notes": notes,
        "totalSteps": totalSteps
    }


