from fastapi import FastAPI, UploadFile, File
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
import os

app = FastAPI()

load_dotenv()

cloudinary.config(
    cloud_name="dl581kkmn",
    api_key=os.getenv('API_KEY'),
    api_secret=os.getenv('API_SECRET'),
    secure=True
)

@app.get("/")
def Home():
    return {"message": "Welcome"}

@app.post("/upload_file")
async def upload_file(file: UploadFile = File(...)):
    try:
        result = cloudinary.uploader.upload(file.file, public_id="profile")
        return {"secure_url": result["secure_url"]}
    except Exception as e:
        return {"error": str(e)}
