# FuturaExpo Object Recognition API Documentation

Welcome to our API documentation, where we provide comprehensive information about our APIs. These APIs are designed to predict objects (or just a single one) from an image and return a chat-gpt generated text telling the predicted object emissions.

## Table of Contents
- [Object Prediction API](#object-prediction-api)
  - [Overview](#overview)
  - [Usage](#usage)
  - [Request](#request)
  - [Response](#response)
  - [Example](#example)

- [Emissions Text API](#emissions-text-api)
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
