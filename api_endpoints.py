from random import Random, random
import time
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import random
import detector

def dummy_method():
    random_time = random.uniform(0.4, 0.6)
    time.sleep(random_time)
    return random_time

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
class ObjectRecognitionItem(BaseModel):
    image: str

@app.post("/apis/get_object_predictions")
async def request_predictions(item: ObjectRecognitionItem):
    
    prediction_time = dummy_method()

    response_json = {
        "objects": ['sofa', 'pen', 'pencil'],
        "probabilities": [0.932, 0.23, 0.53],
        "origins": [[256, 452, 356, 492],[112, 143, 224, 200], [622, 342, 740, 400]],
        "prediction_time": prediction_time,
        "triggered": random.random() >= 0.65
    }
    
    return JSONResponse(response_json)

class EmissionsTextItem(BaseModel):
    object: str

@app.post("/apis/get_emissions_text")
async def request_emissions(item: EmissionsTextItem):
    
    dummy_method()

    response_json = {
        "response": "The emission is 10 Kg of CO2"
    }
    
    return JSONResponse(response_json)