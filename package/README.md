<a id="readme-top"></a>

[![Contributors][contributors-shield]](https://github.com/sqoshi/hands-to-text/graphs/contributors)
[![Forks][forks-shield]](https://github.com/sqoshi/hands-to-text/network/members)
[![Stargazers][stars-shield]](https://github.com/sqoshi/hands-to-text/stargazers)
[![Issues][issues-shield]](https://github.com/sqoshi/hands-to-text/issues)

<br />
<div align="center">
  <a href="https://github.com/sqoshi/hands-to-text/docs/landscape.png">
    <img src="docs/landscape.png" alt="Logo" width="160" height="80">
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

Hands-to-text package has been created for performing experiments and wrap operations required for transforming gestures to text. Contains video and text module for processing appropriate data. Mainly focueses on:

1. Letter classification from video frames with either RandomForest,LeNet or Resnet18.
2. Text correction with multiple strategies, including AI correction with ChatGPT, LLama; others are treated as preprocessing for strategies.


<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* Python
* OpenCV
* MediaPipe
* Scikit-Learn
* NumPy
* Transformers
* PyTorch
* TorchVision
* AutoCorrect
* WordNinja
* Fuzzy
* TextDistance
* g4f
* OpenAI GPT
* LLama

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

To get started with hands-to-text, follow these steps:

### Installation

Install via pip artifactory:

```sh
pipx install hands-to-text
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage

```python
from hands_to_text import read_hands_models, process_frame, draw_classbox
import cv2

# Load the model
model, hands = read_hands_models(path="path/to/your/model.pickle")

cap = cv2.VideoCapture("path/to/your/video.mp4")
ret, frame = cap.read()

if ret:
    classed_hand_box = process_frame(frame, model, hands)
    if classed_hand_box:
        draw_classbox(frame, classed_hand_box)
    cv2.imshow("Hand Detection", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

cap.release()
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Roadmap

* [x] Process image with model
* [x] Correct text with strategies
* [x] Allow usage of different models
* [x] Allow injection of custom implementations by adding abstract clases
* [x] Optimize real-time performance ( handle frames streams)
* [x] Add more text correction strategies

<p align="right">(<a href="#readme-top">back to top</a>)</p>
