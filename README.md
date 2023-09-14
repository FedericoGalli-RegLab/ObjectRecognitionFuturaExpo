﻿# FuturaExpo Object Recognition API Documentation

Welcome to our API documentation, where we provide comprehensive information about our APIs. These APIs are designed to predict objects (or just a single one) from an image and return a chat-gpt generated text telling the predicted objects emissions.

## Table of Contents
- [/api/get_object_predictions](#object-prediction-api)
  - [Overview](#overview)
  - [Usage](#usage)
  - [Request](#request)
  - [Response](#response)
  - [Example](#example)

- [/api/get_emissions_text](#emissions-text-api)
  - [Overview](#overview)
  - [Usage](#usage)
  - [Request](#request)
  - [Response](#response)
  - [Example](#example)

## Object Prediction API
### Overview
The `api/get_object_prediction` API allows you to perform advanced object prediction on images. It utilizes state-of-the-art machine learning models to identify and annotate objects within an image, providing you with valuable insights.

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
