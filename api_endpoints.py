from random import Random, random
import time
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import random

def dummy_method():
    random_time = random.random() * 4
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

@app.post("/api/get_object_prediction")
async def request_prediction(item: ObjectRecognitionItem):
    
    prediction_time = dummy_method()

    response_json = {
        "objects": ['sofa', 'pen', 'pencil'],
        "prediction_time": prediction_time,
        "triggered": random.random() >= 0.8
    }
    
    return JSONResponse(response_json)

class EmissionsTextItem(BaseModel):
    object: str

@app.post("/api/get_emissions_text")
async def request_prediction(item: EmissionsTextItem):
    
    dummy_method()

    response_json = {
        "response": "The emission is 10 Kg of CO2"
    }
    
    return JSONResponse(response_json)