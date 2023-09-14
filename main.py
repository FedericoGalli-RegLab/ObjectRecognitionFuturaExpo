from ultralytics import YOLO
from PIL import Image
import cv2
import time

# Load a model
model = YOLO('yolov8m.pt')  # pretrained YOLOv8m model best performance/inference_time tradeoff

def api_dev():
    cap = cv2.VideoCapture(0)
    i = 0
    for i in range(1, 5):
        time.sleep(0.5)
        ret, frame = cap.read()
        #cropped_img = frame[195: 395, 340: 940]
        #results = model([cropped_img])
        results = model([frame])

        for r in results:
            im_array = r.plot()  # plot a BGR numpy array of predictions
            im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
            im.show() # show image
            im.save("Results/" + 'result' + str(i) + '.jpg')  # save image

def image_inference(image_name):

    #Cropping the image to get just the center of the image
    img = cv2.imread(image_name)
    
    cropped_img = img[195: 395, 340: 940] # y, x

    results = model([cropped_img])
    # Show the results
    for r in results:
        im_array = r.plot()  # plot a BGR numpy array of predictions
        im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
        im.show() # show image
        im.save("Results/" + 'result.jpg')  # save image

def video_inference(video_path="Videos/walking_osaka.mp4"):
    if len(video_path) == 0:
        cap = cv2.VideoCapture(0)
    else:
        cap = cv2.VideoCapture(video_path)
    
    # Loop through the video frames
    while cap.isOpened():

        # Read a frame from the video
        success, frame = cap.read()
        if success:
            # Run YOLOv8 inference on the frame
            results = model(frame)
            print(results[0])
            # Visualize the results on the frame
            annotated_frame = results[0].plot()
            # Display the annotated frame
            cv2.imshow("Inference", annotated_frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            break 

    # Release the video capture object and close the display window
    cap.release()
    cv2.destroyAllWindows()

image_inference("Images/img3.jpg")

#video_inference("") #inference on webcam

#api_dev()