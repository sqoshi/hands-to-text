# hands-to-text - package

Python package designed to convert sign language frames from video into readable text. The package processes video frames to detect hand landmarks, classifies them, and applies text processing strategies to refine the output.

## Table of Contents

- [hands-to-text - package](#hands-to-text---package)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Overview](#overview)
    - [Processing Video Frames](#processing-video-frames)
      - [Code Example](#code-example)
    - [Text Processor](#text-processor)
      - [Code Example TP](#code-example-tp)
    - [Text Processing Strategies](#text-processing-strategies)
      - [Remove Repetitions Strategy](#remove-repetitions-strategy)
      - [Filter Continuous Symbols Strategy](#filter-continuous-symbols-strategy)
      - [Leverage Language Model Strategy](#leverage-language-model-strategy)
  - [License](#license)
  - [Contributing](#contributing)
  - [Experiments summary](#experiments-summary)

## Introduction

Hands-to-text package has been created for experimenting. There are 2 main problems, that this repo is responsible for.

1. Letter classification from video frames with either RandomForest or LeNet CNN,
2. Text correction with many Strategies, including AI correction with ChatGPT, other are rather treated as preprocessing for Strategies.

So as stated, we selecting the model which we want to use and which strategy pipeliene we want to use, for example

```text
  video -split to frames-> Model(RandomForest) -classify each frame-> Recognized letters with noices -> Text Correction(Pipeline[RemoveRepetitionsStrategy, MajorityVoteStrategy, ChatGPTStartegy]) -> Corrected Text
```

## Overview

### Processing Video Frames

Frame Processing: Detect hand landmarks and classify them to draw bounding boxes with recognized letters.

Model Prediction: The hand landmarks are used to predict the corresponding sign language letter.

#### Code Example

Process a Video Frame
To process a video frame, you need to load your model and Mediapipe Hands instance. Then, use the process_frame function to analyze the frame and get the classified hand boxes.

```python
from hands_to_text import read_hands_models, process_frame, draw_classbox
import cv2

# Load the model and Mediapipe Hands
model, hands = read_hands_models(path="path/to/your/model.pickle")

# Capture a frame from video
cap = cv2.VideoCapture("path/to/your/video.mp4")
ret, frame = cap.read()

if ret:
    # Process the frame
    classed_hand_box = process_frame(frame, model, hands)

    # Draw the classified hand box on the frame
    if classed_hand_box:
        draw_classbox(frame, classed_hand_box)

    # Display the frame with drawn bounding box
    cv2.imshow("Hand Detection", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

cap.release()
```

### Text Processor

The TextProcessor class applies various strategies to clean and correct the text output from sign language frames.

#### Code Example TP

To refine the text output using TextProcessor, create an instance with the desired strategies and process the raw text sequence.

```python
from hands_to_text import TextProcessor
from hands_to_text.strategy import RemoveRepetitionsStrategy, FilterContiniousSymbolsStrategy, LeverageLanguageModelStrategy

# Initialize TextProcessor with strategies
text_processor = TextProcessor(strategies=[
    RemoveRepetitionsStrategy(),
    FilterContiniousSymbolsStrategy(),
    LeverageLanguageModelStrategy()
])

# Raw text output from sign language frames
raw_text = "HHHHHEEELLLLOOOO"

# Process the text to clean and correct it
processed_text = text_processor.process(raw_text)

print("Processed Text:", processed_text)
```

### Text Processing Strategies

#### Remove Repetitions Strategy

Removes consecutive repeated characters from the text. Example:

```python
"aaabbbbcc" -> "abc"
```

#### Filter Continuous Symbols Strategy

Filters out symbols that appear continuously for a number of repetitions greater than or equal to a given threshold. Example:

```python
"aaaabbbbcccc" with min_reps=4 -> "aaaabbbbcccc"
```

#### Leverage Language Model Strategy

Uses a language model to correct noisy sequences. Example:

```python
"HHHHHEEELLLLOOOO" -> "HELLO"
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome. Please open issues or submit pull requests if you have improvements or fixes.

## Experiments summary

![Tests Summary](./experiments.md)
