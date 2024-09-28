import cv2
import pytest
from hands_to_text.text import (
    TextProcessor,
    RemoveRepetitionsStrategy,
    LeverageLanguageModelStrategy,
)
from hands_to_text.video import draw_classbox, process_frame, read_hands_models


@pytest.fixture(scope="module")
def setup():
    text_processor = TextProcessor(
        strategies=[RemoveRepetitionsStrategy(), LeverageLanguageModelStrategy()]
    )
    model_path = "../models/model.pickle"
    model, hands = read_hands_models(model_path)
    return model, hands, text_processor


def process_video(video_path, model, text_processor, hands_model):
    cap = cv2.VideoCapture(video_path)
    recognized_text = ""
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        chbox = process_frame(img, model, hands_model)
        if chbox:
            recognized_text += chbox.class_name
        draw_classbox(img, chbox)
    cap.release()
    return text_processor.process(recognized_text)


@pytest.mark.parametrize(
    "video_path, expected_text",
    [
        ("examples/iloveyou", "i love you"),
    ],
)
def test_video_processing(video_path, expected_text, setup):
    model, hands_model, text_proc = setup
    processed_text = process_video(video_path, model, text_proc, hands_model)
    assert (
        processed_text == expected_text
    ), f"Expected '{expected_text}', but got '{processed_text}'"
    print(f"Test passed for video {video_path}!")
