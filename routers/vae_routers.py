from fastapi import FastAPI, File, UploadFile, APIRouter
from fastapi.responses import FileResponse
from pydantic import BaseModel
from models.Music_VAE.music_vae_model import MusicGeneratorVAE

music_router = APIRouter()
music_generator = MusicGeneratorVAE()

class InterpolationInput(BaseModel):
    num_output: int

@music_router.post("/sample/")
async def sample_midi() -> FileResponse:
    output_path = music_generator.sample()
    return FileResponse(output_path, media_type="audio/midi")

@music_router.post("/interpolate/")
async def interpolate_midi(input_data: InterpolationInput) -> FileResponse:
    output_path = music_generator.interpolate(num_output=input_data.num_output)
    return FileResponse(output_path, media_type="audio/midi")

@music_router.post("/groove/")
async def add_groove() -> FileResponse:
    output_path = music_generator.groove()
    return FileResponse(output_path, media_type="audio/midi")

# @app.post("/upload/")
# async def upload_midi(file: UploadFile = File(...)):
#     music_generator.upload(file.file)
#     return {"status": "File uploaded and processed"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
