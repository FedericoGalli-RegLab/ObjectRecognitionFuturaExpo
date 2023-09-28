from random import Random, random
from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import Detector

inference_obj = Detector.Detector('yolov8m.pt')

origins = [
    "http://localhost",
    "http://localhost:8000",
    "*"
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/api", StaticFiles(directory="api"), name="api")

#POST RESPONSE API

@app.post("/apis/get_object_predictions")
async def request_predictions(image: UploadFile):
    
    return JSONResponse(inference_obj.image_inference(image.file))

class EmissionsTextItem(BaseModel):
    objects: list = []

@app.post("/apis/get_emissions_text")
async def request_emissions(item: EmissionsTextItem):

    response_json = {
        "objects": item.objects,
        "responses": ["The emission for a chaise lounge sofa is 100 Kg of CO2", "The emission for a ink pen 2 Kg of CO2", "The emission for a pencil is 5 Kg of CO2"],
        "emission_amount": [100, 2, 5]
    }
    
    return JSONResponse(response_json)