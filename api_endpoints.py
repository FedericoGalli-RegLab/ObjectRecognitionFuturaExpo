from codecs import strict_errors
from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import Detector
import ChatGPTService

inference_obj = Detector.Detector('yolov8m.pt')
question_responser = ChatGPTService.GPTService()

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

    responses = []
    kgs = []
    for i, obj in enumerate(item.objects):
        responses.append(question_responser.query_gpt(obj))
        responses[i] = responses[i].lower()
        
        str_tmp = ""
        for j, char in enumerate(responses[i]):
            try:
                if char != ' ':
                    if char != ',':
                        str_tmp += char
                        if j == len(responses[i]) - 1:
                            kgs.append(float(str_tmp))        
                else:
                    if responses[i][j + 1] == 't':
                        kgs.append(float(str_tmp) * 1000)
                    else:
                        kgs.append(float(str_tmp))

                    str_tmp = ""
                    break
            except:
                kgs.append(10)
                str_tmp = ""
            
    response_json = {
        "objects": item.objects,
        "emissions_amount": kgs
    }
    
    return JSONResponse(response_json)


