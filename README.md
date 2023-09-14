# FuturaExpo Object Recognition API Documentation

## PLEASE NOTE 
**The following APIs are currently in a dummy development state wich means the APIs DO NOT return any meaningfull result. We are defining the architecture to let the DEVs build up the main code structure.**

## APIs Documentation
Welcome to our API documentation, where we provide comprehensive information about our APIs. These APIs are designed to predict objects (lets suppose for now there could be a multiple object detedction, TBD if in future this is still possible) from an image and return a chat-gpt generated text telling the predicted objects emissions.

## Table of Contents
- [Objects prediction](#object-prediction-api)
  - [Overview](#overview)
  - [Usage](#usage)
  - [Request](#request)
  - [Response](#response)
  - [Example](#example)

- [Emissions prediction](#emissions-text-api)
  - [Overview](#overview)
  - [Usage](#usage)
  - [Request](#request)
  - [Response](#response)
  - [Example](#example)

## Object Prediction API
### Overview
The `apis/get_object_prediction` API allows you to perform advanced object prediction on images. It utilizes a YOLO machine learning model to identify and annotate objects within an image, providing you with valuable insights such as prediction probability for each object and boundig box.

### Usage
To use the Object Prediction API, make a POST request to the following endpoint: http://10.88.2.76:8000/apis/get_object_predictions

**Please note, in order to access the APIs you need to be connected to the Regesta VPN**

### Request
- **Input**: The current request consist of a json file wich takes a simple string as input, **we need to discuss how to pass the image and the kind of format to use.**
```json
{
  "image": "string"
}
```
- **Output**: A JSON response containing object prediction results.
  - objects: List of string rapresenting the text of predicted object in the image.
  - probabilities: List 
  - origins: 
  - widths: 
  - heights: 
  - prediction_time: 
  - triggered: 
```json
{
  "objects": "list(string)",
  "probabilities": "list(float)",
  "origins": "list(list(int))",
  "widths": "list(int)",
  "heights": "list(int)",
  "prediction_time": "int",
  "triggered": "bool"
}
```

### Response
Here an example response:
```json
{
  "objects": ["sofa", "pen", "pencil"],
  "probabilities": [0.932, 0.23, 0.53],
  "origins": [[256, 452],[112, 143], [622, 342]],
  "widths": [112, 100, 92],
  "heights": [221, 64, 99],
  "prediction_time": 1.912452,
  "triggered": false
}
```

### Example
```bash
# Sample request using cURL
curl -X POST -F "image=@/path/to/your/image.jpg" https://api.example.com/api/get_object_prediction
