from fastapi import FastAPI, File, UploadFile, APIRouter
from fastapi.responses import FileResponse
from pydantic import BaseModel
from models.Music_VAE.music_vae_model import MusicGeneratorVAE

vae_router = APIRouter()
music_generator = MusicGeneratorVAE()

class RequestData(BaseModel):
    numbars: int
    numSample: int
    instrument: str
    filename: str

@vae_router.post("/drum")
async def sample_midi(request_data: RequestData):
   
    output_path = music_generator.sample("nade-drums_2bar_full",request_data.numSample,request_data.filename,True)
    return {
                "numbars":request_data.numbars,
                "numSample":request_data.numSample,
                "instrument":request_data.instrument,
                "filename":request_data.filename
            }

@vae_router.post("/piano")
async def interpolate_midi(request_data: RequestData):
    output_path = music_generator.interpolate("cat-mel_2bar_big",request_data.numSample,6,request_data.filename,True)
    return {
                "numbars":request_data.numbars,
                "numSample":request_data.numSample,
                "instrument":request_data.instrument,
                "filename":request_data.filename
            }

@vae_router.post("/groove")
async def add_groove(request_data: RequestData):
    output_path = music_generator.groove("groovae_2bar_humanize",2,request_data.numSample,6,request_data.filename)
    return {
                "numbars":request_data.numbars,
                "numSample":request_data.numSample,
                "instrument":request_data.instrument,
                "filename":request_data.filename
            }

# @app.post("/upload/")
# async def upload_midi(file: UploadFile = File(...)):
#     music_generator.upload(file.file)
#     return {"status": "File uploaded and processed"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
