from http.client import TOO_MANY_REQUESTS
from ultralytics import YOLO
from PIL import Image
import cv2

classes = {
    "person": "persona",
    "bicycle": "bicicletta",
    "car": "automobile",
    "motorcycle": "motocicletta",
    "airplane": "aereo di linea",
    "bus": "autobus", 
    "train": "treno", 
    "truck": "camion",
    "boat": "barca",
    "traffic light": "semaforo",
    "fire hydrant": "idrante",
    "stop sign": "cartello stradale",
    "parking meter": "parcometro",
    "bench": "panchina",
    "bird": "uccello",
    "cat": "gatto",
    "dog": "cane",
    "horse": "cavallo",
    "sheep": "pecora",
    "cow": "mucca",
    "elephant": "elefante",
    "bear": "orso", 
    "zebra": "zebra",
    "giraffe": "giraffa", 
    "backpack": "zaino", 
    "umbrella": "ombrello",
    "handbag": "borsetta",
    "tie": "cravatta", 
    "suitcase": "borsa", 
    "frisbee": "frisbee", 
    "skis": "sci", 
    "snowboard": "snowboard", 
    "sports ball": "pallone da calcio",
    "kite": "kite", 
    "baseball bat": "mazza da baseball", 
    "baseball glove": "guanti da baseball", 
    "skateboard": "skateboard",
    "surfboard": "tavola da surf", 
    "tennis racket": "racchetta da tennis", 
    "bottle": "bottiglia", 
    "wine glass": "bicchiera da vino", 
    "cup": "tazza",
    "fork": "forchetta", 
    "knife": "coltello", 
    "spoon": "cucchiaio", 
    "bowl": "ciotola", 
    "banana": "banana", 
    "apple": "mela", 
    "sandwich": "panino",
    "orange": "arancia",
    "broccoli": "broccoli",
    "carrot": "carota", 
    "hot dog": "hot dog", 
    "pizza": "pizza",
    "donut": "ciambella",
    "cake": "torta",
    "chair": "sedia",
    "couch": "poltrona",
    "potted plant": "pianta", 
    "bed": "letto",
    "dining table": "tavolo da pranzo",
    "toilet": "bagno",
    "tv": "televisore",
    "laptop": "laptop",
    "mouse": "mouse",
    "remote": "remote",
    "keyboard": "tastiera",
    "cell phone": "smartphone",
    "microwave": "microonde",
    "oven": "forno",
    "toaster": "toaster",
    "sink": "lavandino",
    "refrigerator": "frigorifero",
    "book": "libro",
    "clock": "orologio",
    "vase": "vaso",
    "scissors": "forbici",
    "teddy bear": "peluches",
    "hair drier": "asciuga capelli",
    "toothbrush": "spazzolino da denti"

}


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
        
        it_objects = []

        for obj in objects:
            it_objects.append(classes[obj])

        response_string = {
        "objects": {"EN_name": objects,
                    "IT_name": it_objects
                    },
        "origins": xyxy,
        "prediction_time": prediction_time,
        "triggered": triggered
        }
        return response_string

    def person_remover(self, pred_list, xyxy_list):
        n_person = pred_list.count("person")
        for _ in range(n_person):
            index = pred_list.index("person")
            pred_list.pop(index)
            xyxy_list.pop(index)

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