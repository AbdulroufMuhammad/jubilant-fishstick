from fastapi import FastAPI, UploadFile, File, HTTPException
import cloudinary
import cloudinary.uploader
import json
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
        link = {"secure_url": result["secure_url"], "public_id": result["public_id"]}
        
        if os.path.exists("uploaded_links.json"):
            with open("uploaded_links.json", "r") as f:
                data = json.load(f)
        else:
            data = []

        data.append(link)
        
        with open("uploaded_links.json", "w") as f:
            json.dump(data, f)

        return link
    except Exception as e:
        return {"error": str(e)}

@app.get("/get_file/{image_id}")
def get_file(image_id: str):
    try:
        with open("uploaded_links.json", "r") as f:
            data = json.load(f)
        
        for link in data:
            if link["public_id"] == image_id:
                return {"secure_url": link["secure_url"]}
        
        raise HTTPException(status_code=404, detail="Image ID not found")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="No files uploaded yet")
    except Exception as e:
        return {"error": str(e)}
