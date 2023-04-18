import io,os
from fastapi import FastAPI, UploadFile, File, APIRouter
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from routers import vae_router, melody_router, music_router

app = FastAPI()

prefix = "/api/v1"

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Mount the "music" folder as a static directory
app.mount("/music", StaticFiles(directory="music"), name="music")
app.include_router(music_router, prefix=prefix)
app.include_router(vae_router, prefix=prefix)  
app.include_router(melody_router, prefix=prefix)  


