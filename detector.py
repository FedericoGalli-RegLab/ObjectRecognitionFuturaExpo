from calendar import c
from http.client import TOO_MANY_REQUESTS
import logging
from tabnanny import verbose
from ultralytics import YOLO
from PIL import Image
import cv2

'''  0: person
  1: bicycle
  2: car
  3: motorcycle
  4: airplane
  5: bus
  6: train
  7: truck
  8: boat
  9: traffic light
  10: fire hydrant
  11: stop sign
  12: parking meter
  13: bench
  14: bird
  15: cat
  16: dog
  17: horse
  18: sheep
  19: cow
  20: elephant
  21: bear
  22: zebra
  23: giraffe
  24: backpack
  25: umbrella
  26: handbag
  27: tie
  28: suitcase
  29: frisbee
  30: skis
  31: snowboard
  32: sports ball
  33: kite
  34: baseball bat
  35: baseball glove
  36: skateboard
  37: surfboard
  38: tennis racket
  39: bottle
  40: wine glass
  41: cup
  42: fork
  43: knife
  44: spoon
  45: bowl
  46: banana
  47: apple
  48: sandwich
  49: orange
  50: broccoli
  51: carrot
  52: hot dog
  53: pizza
  54: donut
  55: cake
  56: chair
  57: couch
  58: potted plant
  59: bed
  60: dining table
  61: toilet
  62: tv
  63: laptop
  64: mouse
  65: remote
  66: keyboard
  67: cell phone
  68: microwave
  69: oven
  70: toaster
  71: sink
  72: refrigerator
  73: book
  74: clock
  75: vase
  76: scissors
  77: teddy bear
  78: hair drier
  79: toothbrush
  '''


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
        results = self.model([image], verbose=False)

        for item in results[0].boxes.cls.tolist():
            objects.append(results[0].names[item])
        prediction_time = results[0].speed['preprocess'] + results[0].speed['inference'] + results[0].speed['postprocess']
        xyxy = results[0].boxes.xyxy.tolist()
        
        self.person_remover(objects, xyxy)
        self.cls_pred.append(objects)

        if len(self.cls_pred) == 2:
            triggered = self.trigger_logic(self.cls_pred)
        else:
            triggered = False
        
        response_string = {
        "objects": {"EN_name": objects,
                    "IT_name": objects
                    },
        "origins": xyxy,
        "prediction_time": prediction_time,
        "triggered": triggered
        }
        return response_string

    def person_remover(self, pred_list, xyxy_list):
        
        for i, item in enumerate(pred_list):
            if item == "person":
                pred_list.pop(i)
                xyxy_list.pop(i)

    def trigger_logic(self, test_list):
        
        concatanation_1 = "".join(sorted("".join(test_list[0])))
        concatanation_2 = "".join(sorted("".join(test_list[1])))

        if concatanation_1 == concatanation_2 and len(concatanation_1) > 0:
            self.flush_images()
        else:
            self.shift_images()
        return (concatanation_1 == concatanation_2 and len(concatanation_1) > 0)

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
