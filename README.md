# 🗒️FuturaExpo Object Recognition API Documentation

## PLEASE NOTE 
**The following APIs are currently in a dummy development state wich means the APIs DO NOT return any meaningfull result. We are defining basic architecture to let the DEVs build up the main code structure. In addition remember that the developement is still ongoing by our side, so you may encounter APIs mulfunctions/bugs. If so, you are strongly encouraged to notify me on the issue**

## APIs Documentation
Welcome to our API documentation, where we provide comprehensive information about our APIs. These APIs are designed to predict objects (lets suppose for now there could be a multiple object detedction, TBD if in future this is still possible) from an image and return a chat-gpt generated text telling the predicted objects emissions.

## Table of Contents
- [Objects prediction](#object-prediction-api)
  - [Overview](#overview)
  - [Usage](#usage)
  - [Request](#request)
  - [Response](#response)
  - [JS Example](#js-example)

- [Emissions prediction](#emissions-prediction-api)
  - [Overview](#eoverview)
  - [Usage](#eusage)
  - [Request](#erequest)
  - [Response](#eresponse)
  - [JS Example](#ejs-example)

- [Contacts](#contacs)

## Object Prediction API
### Overview
The `/apis/get_object_prediction` API allows you to perform advanced object prediction on images. It utilizes a YOLO machine learning model to identify and annotate objects within an image, providing you with valuable insights such as prediction probability for each object and boundig box.

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
  - objects: List of string, rapresenting the text of predicted object in the image.
  - probabilities: List of floats, rapresenting the prediction probability of each recognized object in the image.
  - origins: List of list of integers, boxes are represented via corners, x1, y1 being top left and x2, y2 being bottom right.
  - prediction_time: Integer, rapresenting the time to produce a prediction (not considering the internet latency)
  - triggered: Boolean, rapresenting if objects are being detected for the sufficent amount of time to be considered valid for the emissions prediction
    
```json
{
  "objects": "list(string)",
  "probabilities": "list(float)",
  "origins": "list(list(int))",
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
  "origins": [[256, 452, 356, 492],[112, 143, 224, 200], [622, 342, 740, 400]],
  "prediction_time": 1.912452,
  "triggered": true
}
```

### JS Example
Sample example in JavaScript, where the function paramenter **data** is your input JSON: 

```javascript
# Sample request using fetch
function postData(data) {

  fetch('http://10.88.2.76:8000/apis/get_object_prediction', {
    method: 'POST',
    headers: {
      "Content-type": "application/json; charset=UTF-8"
    },
    body: JSON.stringify({
      query: data,
      description: '',
    })
  }).then((response) => response.json())
    .then((json) => showResponse(json));
  return;
}
```

## Emissions Prediction API
### Overview
The `/apis/get_emissions_text` API allows you to call ChatGPT APIs and predict the carbon footprint of the specified objects.

### Usage
To use the Emissions Prediction API, make a POST request to the following endpoint: http://10.88.2.76:8000/apis/get_emissions_text

**Please note, in order to access the APIs you need to be connected to the Regesta VPN**

### Request
- **Input**: The current request consist of a json file wich takes a simple string as input.
```json
{
  "object": "string"
}
```
- **Output**: A JSON response containing carbon emissions results.
  - response: String, rapresenting the ChatGPT generated text.

```json
{
  "response": "string"
}
```

### Response
Here an example response:

```json
{
  "response": "The emission for a bottle is 10 Kg of CO2"
}
```

### JS Example
Sample example in JavaScript, where the function paramenter **data** is your input JSON: 

```javascript
# Sample request using fetch
function postData(data) {

  fetch('http://10.88.2.76:8000/apis/get_emissions_text', {
    method: 'POST',
    headers: {
      "Content-type": "application/json; charset=UTF-8"
    },
    body: JSON.stringify({
      query: data,
      description: '',
    })
  }).then((response) => response.json())
    .then((json) => showResponse(json));
  return;
}
```

## Contacts
If you need clarifications, having questions or problems of any kind just contact me on the Google Chat or via email **federico.galli@regestaitalia.it**

Have fun 😉
