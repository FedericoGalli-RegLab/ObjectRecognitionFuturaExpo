import logging
from tabnanny import verbose
from ultralytics import YOLO
from PIL import Image
import cv2

class detector:

    model = None
    cls_pred = None
    prob_pred = None

    def __init__(self, model_name:str):
        
        self.cls_pred = []
        self.prob_pred = []
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
        print(objects)
        
        if len(self.cls_pred) == 3:
            triggered = self.trigger_logic()
        else:
            self.cls_pred.append(objects)
            self.prob_pred.append(probabilities)
        
        response_string = {
        "objects": objects,
        "probabilities": probabilities,
        "origins": xyxy,
        "prediction_time": prediction_time,
        "triggered": True
        }
        return response_string

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
        self.prob_pred = []
        return return_object_list

    def show_predicted_image(self, image_name):
        #Cropping the image to get just the center of the image
        img = cv2.imread(image_name)

        results = self.model([img], verbose=True)
        # Show the results
        for r in results:
            im_array = r.plot()  # plot a BGR numpy array of predictions
            im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
            im.show() # show image
            im.save("Results/" + 'result.jpg')  # save image        

#test = detector('yolov8m.pt')
#test.show_predicted_image('Images/img3.jpg')
#print(test.trigger_logic([['a', 'b', 'f'], ['c', 'b'], ['d', 'e', 'u', 'f']]))