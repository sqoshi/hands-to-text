<a id="readme-top"></a>
<div align="center">

[![Contributors](https://img.shields.io/github/contributors/sqoshi/hands-to-text.svg)](https://github.com/sqoshi/hands-to-text/graphs/contributors)
[![Forks](https://img.shields.io/github/forks/sqoshi/hands-to-text.svg)](https://github.com/sqoshi/hands-to-text/network/members)
[![Stargazers](https://img.shields.io/github/stars/sqoshi/hands-to-text.svg)](https://github.com/sqoshi/hands-to-text/stargazers)
[![Issues](https://img.shields.io/github/issues/sqoshi/hands-to-text.svg)](https://github.com/sqoshi/hands-to-text/issues)

</div>

<br />
<div align="center">
  <a href="https://github.com/sqoshi/hands-to-text/blob/master/docs/landscape.png">
   <img src="https://github.com/sqoshi/hands-to-text/raw/master/docs/landscape.png" alt="Logo" width="720" height="320">
 </a>

<h3 align="center">hands-to-text</h3>

  <p align="center">
    Python package designed to convert sign language frames from video into readable text.
    <br />
    <a href="https://github.com/sqoshi/hands-to-text"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/sqoshi/hands-to-text">View Demo</a>
    &middot;
    <a href="https://github.com/sqoshi/hands-to-text/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/sqoshi/hands-to-text/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#built-with">Built With</a></li>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
  </ol>
</details>

## About The Project

The Hands-to-Text application is a FastAPI-based web tool designed to assist hard-of-hearing individuals in communicating with ChatGPT using American Sign Language (ASL) letters. This web application enables users to ask questions to ChatGPT through a hand gesture recognition system, making AI-powered conversations more accessible.

Built with Python and FastAPI, the application ensures a lightweight and efficient backend for real-time interaction. To maintain error-free communication between the backend API and the frontend templates, Pydantic is used for data validation. Additionally, sensitive data, such as the ChatGPT API key, is managed securely using Pydantic models and environment variables to prevent unauthorized access.

For text processing, the application integrates the OpenAI API, which corrects and refines input text before sending it to ChatGPT. The Hands-to-Text package, specifically designed for this project, handles AI models that recognize and interpret hand gestures. To detect hands and extract ASL letters from video input, the system leverages MediaPipe, a powerful computer vision library for precise hand tracking.

To ensure high-performance and scalable deployment, the application runs on Uvicorn, a modern ASGI server optimized for fast execution. Additionally, the entire system is containerized using Docker, allowing users to run it seamlessly on their local machines with just a ChatGPT API key.

![img](https://github.com/sqoshi/hands-to-text/blob/master/docs/plant.png)

Ultimately, this project aims to bridge communication gaps by enabling ASL users to interact with ChatGPT effortlessly, making digital conversations more inclusive and accessible.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* Python
* OpenCV
* MediaPipe
* Hands-to-Text
* Pydantic
* Pydantic-Settings
* FastAPI
* OpenAI
* Uvicorn
* Python-Dotenv

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

To get started with hands-to-text web application, follow these steps:

### Prerequirements

It is required to generate openapikey from [page](https://platform.openai.com/).

### Installation

Install via pip artifactory:

```sh
    docker run --network host \
        --name htt --rm -it \
        -e CHATGPT_KEY=<KEY> \
        -e DISPLAY=${DISPLAY} \
        --device /dev/video0:/dev/video0 \
        -v /tmp/.X11-unix:/tmp/.X11-unix \
        ghcr.io/sqoshi/hands-to-text:0.1.1
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage

### Documentation

Interactive api documentation is available under `/docs` endpoint.

### Web

![img](https://github.com/sqoshi/hands-to-text/blob/master/docs/examplenew.png)

1. Open the Application - Navigate to localhost:8000 in your browser.
1. Start the Camera - Enable your camera to begin recognizing ASL gestures.
1. Use ASL to Write a Sentence - Sign letters in front of the camera to form a sentence.
1. Stop the Camera - Once you've completed your input, turn off the camera.
1. Correct the Text - Review and edit the detected text for accuracy.
1. Send the Chat - Submit your message to ChatGPT for a response.
1. Read the Response - View ChatGPT’s reply, with the entire conversation history saved for reference.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Roadmap

* [x] Phase 1: MVP
  * [x] Basic ASL Recognition - Implement hand tracking and ASL letter detection using MediaPipe.
  * [x] FastAPI Backend - Set up a lightweight backend with FastAPI for handling requests.
  * [x] Frontend UI - Create a simple web UI with JavaScript and HTML to capture ASL input.
  * [x] Text Correction - Integrate OpenAI API for autocorrection of recognized ASL sequences.
  * [x] ChatGPT Integration - Enable users to send corrected text to ChatGPT and receive responses.
  * [x] Basic Dockerization - Package the application in a Docker container for easy deployment.

* [x] Phase 2: Enhanced Features
  * [x] Improve ASL Recognition - Enhance gesture recognition with better AI models (e.g., custom CNNs or LSTMs).
  * [x] Real-Time Text Processing - Display live text suggestions while signing.
  * [x] User Profiles & History - Implement session-based chat history storage for users.
  * [x] Security Enhancements - Improve API key handling, user authentication, and request validation.

* [x] Phase 3: Advanced Capabilities
  * [x] Customizable AI Models - Train and fine-tune custom models for better ASL recognition accuracy.
  * [ ] Multi-Hand Gesture Support - Recognize complex gestures (e.g., words instead of just letters).
  * [ ] Speech Output - Convert ASL text responses into speech output for additional accessibility.
  * [ ] Mobile Support - Develop a PWA (Progressive Web App) or mobile app for on-the-go use.
  * [ ] Cloud Deployment - Deploy on AWS/GCP/Azure for global accessibility.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
