import io,os
from fastapi import FastAPI, UploadFile, File, APIRouter
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from routers import music_router, melody_router

app = FastAPI()

prefix = "/api/v1"

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Mount the "music" folder as a static directory
# app.mount("/music", StaticFiles(directory="music"), name="music")
app.include_router(music_router, prefix=prefix)  
app.include_router(melody_router, prefix=prefix)  
# @app.post("/upload-music")
# async def create_upload_file(file: UploadFile = File(...)):
#     """
#         Uploads a music file to the music folder
#         returns the filename and status code

#     """
#     if not os.path.exists('music'):
#         os.makedirs("music")
#         file_location = os.path.join("music", file.filename)
#         with open(file_location, "wb") as buffer:
#             buffer.write(await file.read())
#     else:
#         file_location = os.path.join("music", file.filename)
#         with open(file_location, "wb") as buffer:
#             buffer.write(await file.read())  
#     return {"filename": file.filename,"status":200}

# @app.get("/get-music")
# def get_music():
#     file_list = os.listdir("music")
#     files = []
#     if file_list:
#         file_urls = [{"url":f"/music/{filename}","filename":{filename}} for filename in file_list]
#         return {"file_urls": file_urls}
#     else:
#         return {"error": "No files found in the music folder."}
    
# @app.get("/developers")
# def get_developers():
#     """
#         Returns the list of developers
#     """
#     developers = [
#         {
#             "id":1,
#             "name":'Raj Kumar Phagami',
#             "profession":"AI Engineer",
#             "email":"magar.fagami@gmail.com",
#             "phone":"+1 647 404 7685",
#             "image":"", 
#             "text":""   
#         },
#         {
#             "id":2,
#             "name":'Mandil Karki',
#             "profession":"NLP Engineer",
#             "email":"mandilkarki4444@gmail.com",
#             "phone":"+1 647 404 7685",
#             "image":"", 
#             "text":""   
#         },
#         {
#             "id":3,
#             "name":'Kshitiz Bhattarai',
#             "profession":"ML Engineer",
#             "email":"xhitiz1@gmail.com",
#             "phone":"+1 672 985 0615",
#             "image":"", 
#             "text":""   
#         },
#         {
#             "id":4,
#             "name":'Rajiv Karki',
#             "profession":"Data Engineer",
#             "email":"raziv.luilel@gmail.com",
#             "phone":"+1 672 985 0615",
#             "image":"", 
#             "text":""   
#         },
#         {
#             "id":5,
#             "name":'Trishala Pradhan',
#             "profession":"Data Analyst",
#             "email":"trishalapradhan.tp@gmail.com",
#             "phone":"+1 672 985 0615",
#             "image":"", 
#             "text":""   
#         }
#     ]
#     return {"persons":developers}

# @app.get("/chatbot")
# def get_chatbot():
#     """load the model that predicts the response for the text given by the users

#     Returns:
#         string: it returns the text predicted by the model
#     """
#     return {"response":"Chatbot Response Here Please"} 


# @app.post("/get-parameters")
# def get_parameters(parameters:list):
#     """
#     Load the parameters and let the model 
#     """
#     return {"response":"model generates music"}