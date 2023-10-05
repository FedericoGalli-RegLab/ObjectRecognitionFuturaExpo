from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import Detector
import ChatGPTService

inference_model = Detector.Detector('yolov8m.pt')
question_responser = ChatGPTService.GPTService(use_gpt=False)

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
    
    return JSONResponse(inference_model.image_inference(image.file))

class EmissionsTextItem(BaseModel):
    objects: list = []

@app.post("/apis/get_emissions_text")
async def request_emissions(item: EmissionsTextItem):
    responses = []

    for obj in item.objects:
        responses.append(question_responser.query_no_gpt(obj))
            
    response_json = {
        "objects": item.objects,
        "emissions_amount": responses
    }
    
    return JSONResponse(response_json)


