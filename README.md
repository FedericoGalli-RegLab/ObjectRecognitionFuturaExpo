# FuturaExpo Object Recognition API Documentation

## WARNING!!!
## The following APIs are currently in a dummy development state wich means the APIs DO NOT return any meaningfull result. We are defining the architecture to let the DEVs build up the main code structure.

Welcome to our API documentation, where we provide comprehensive information about our APIs. These APIs are designed to predict objects (or just a single one) from an image and return a chat-gpt generated text telling the predicted objects emissions.

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
The `api/get_object_prediction` API allows you to perform advanced object prediction on images. It utilizes a YOLO machine learning model to identify and annotate objects within an image, providing you with valuable insights.

### Usage
To use the Object Prediction API, make a POST request to the following endpoint:
### Request
- **Input**: An image file or URL.
- **Output**: A JSON response containing object prediction results.

### Response
The response will include a list of objects detected in the image, each with the following information:
- Object label
- Confidence score
- Bounding box coordinates

### Example
```bash
# Sample request using cURL
curl -X POST -F "image=@/path/to/your/image.jpg" https://api.example.com/api/get_object_prediction
