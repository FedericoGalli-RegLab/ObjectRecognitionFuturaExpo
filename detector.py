from calendar import c
from http.client import TOO_MANY_REQUESTS
import logging
from tabnanny import verbose
from ultralytics import YOLO
from PIL import Image
import cv2

class Detector:

    model = None
    cls_pred = None
    cls_prob = None

    def __init__(self, model_name:str):
        
        self.cls_pred = []
        self.model_name = model_name
        self.model = YOLO(model_name)  # pretrained YOLOv8m model best performance/inference_time tradeoff

    def image_inference(self, image):

        image = cv2.imread(image)
        objects = []
        results = self.model([image], verbose=True)
        for r in results:
            
            for item in results[0].boxes.cls.tolist():
                objects.append(results[0].names[item])
            prediction_time = results[0].speed['preprocess'] + results[0].speed['inference'] + results[0].speed['postprocess']
            xyxy = results[0].boxes.xyxy.tolist()

        #print(xyxy)
        #print(probabilities)
        self.cls_pred.append(objects)
        
        if len(self.cls_pred) == 2:
            triggered = self.trigger_logic(self.cls_pred)
        else:
            triggered = False
        
        response_string = {
        "objects": objects,
        "origins": xyxy,
        "prediction_time": prediction_time,
        "triggered": triggered
        }
        return response_string

    '''
    def trigger_logic(self, test_list):

        #flatten_list = self.flatten(self.cls_pred)
        counter = 1
        
        return_object_list = []
        found_pred = []
        for i, item in enumerate(test_list):
            for obj in item:
                if obj not in found_pred:
                    found_pred.append(obj)
                    if i != 2:
                        for entry in test_list[i+1:]:
                            print(entry)
                            for obj2 in entry:
                                if obj2 == obj:
                                    counter +=1
                                print(str(obj) + " == " + str(obj2) + " " + str(obj2 == obj) + " " + str(counter))        
                        if counter > 1:
                            return_object_list.append(obj)
                            counter = 1
        print(found_pred)
        self.cls_pred = []
        self.cls_prob = []
        return return_object_list
    '''

    def trigger_logic(self, test_list):
        
        concatanation_1 = "".join(sorted("".join(test_list[0])))
        concatanation_2 = "".join(sorted("".join(test_list[1])))

        if concatanation_1 == concatanation_2:
            self.flush_images()
        else:
            self.shift_images()
        return concatanation_1 == concatanation_2

    def show_predicted_image(self, image_name):
        #Cropping the image to get just the center of the image
        img = cv2.imread(image_name)

        results = self.model([img], verbose=True)
        # Show the results
        for r in results:
            objects = []
            for item in results[0].boxes.cls.tolist():
                objects.append(results[0].names[item])
            print(objects)
            im_array = r.plot()  # plot a BGR numpy array of predictions
            im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
            im.show() # show image
            im.save("Results/" + 'result.jpg')  # save image
    
    def flush_images(self):
        self.cls_pred = []
        self.cls_prob = []

    def shift_images(self):
        self.cls_pred[0] = self.cls_pred[1]
        self.cls_pred.pop()


test = Detector('yolov8m.pt')

print(test.image_inference("Images/img.jpg"))
print(test.image_inference("Images/img3.jpg"))
print(test.image_inference("Images/img3.jpg"))
#test.show_predicted_image("Images/img3.jpg")

