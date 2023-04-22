import os
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form, APIRouter
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

music_router = APIRouter()

@music_router.get("/get-music")
@music_router.get("/get-music")
def get_music():
    music_folder = "music"
    file_list = os.listdir(music_folder)
    files = []

    if file_list:
        # Retrieve file paths along with their created dates
        files_with_dates = []
        for filename in file_list:
            file_path = Path(music_folder) / filename
            created_date = file_path.stat().st_ctime
            files_with_dates.append((file_path, created_date))

        # Sort the files by created date in descending order
        sorted_files = sorted(files_with_dates, key=lambda x: x[1], reverse=True)

        # Generate the file URLs
        file_urls = [{"url": f"/music/{file_path.name}", "filename": file_path.name} for file_path, _ in sorted_files]

        return {"file_urls": file_urls}
    else:
        return {"error": "No files found in the music folder."}