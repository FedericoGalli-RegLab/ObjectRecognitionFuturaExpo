import logging
from tabnanny import verbose
from ultralytics import YOLO
from PIL import Image
import cv2

class detector:

    model = None
    cls_queue = None
    prob_queue = None

    def __init__(self, model_name:str):
        
        self.cls_queue = []
        self.prob_queue = []
        self.model_name = model_name
        self.model = YOLO(model_name)  # pretrained YOLOv8m model best performance/inference_time tradeoff

    def image_inference(self, image):

        image = cv2.imread(image)
        cropped_img = image[195: 395, 340: 940] # y, x
        results = self.model([cropped_img], verbose=False)

        prediction_time = results[0].speed['preprocess'] + results[0].speed['inference'] + results[0].speed['postprocess']
        xyxy = results[0].boxes.xyxy.tolist()
        objects = []
        for item in results[0].boxes.cls.tolist():
            objects.append(results[0].names[item])

        probabilities = results[0].boxes.conf.tolist()

        if len(self.cls_queue) == 5:
            triggered = self.trigger_logic()
        else:
            self.cls_queue.append(objects)
            self.prob_queue.append(probabilities)

        response_string = {
        "objects": objects,
        "probabilities": probabilities,
        "origins": xyxy,
        "prediction_time": prediction_time,
        "triggered": triggered
        }
        return response_string

    def trigger_logic(self):
        
        self.cls_queue = []
        self.prob_queue = []
    
    def show_predicted_image(self, image_name):
        #Cropping the image to get just the center of the image
        img = cv2.imread(image_name)

        results = self.model([img], verbose=False)
        # Show the results
        for r in results:
            im_array = r.plot()  # plot a BGR numpy array of predictions
            im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
            im.show() # show image
            im.save("Results/" + 'result.jpg')  # save image        

test = detector('yolov8m.pt')
test.show_predicted_image('Images/img3.jpg')