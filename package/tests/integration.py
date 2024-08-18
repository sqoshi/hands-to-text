import cv2
import pytest
from hands_to_text import TextProcessor, draw_classbox, process_frame, read_hands_models

VIDEO_PATH = "path_to_test_video.mp4"
EXPECTED_TEXT = "expected sentence based on test video"


@pytest.fixture(scope="module")
def setup():
    text_processor = TextProcessor()
    model_path = "../models/model.pickle"
    hands_model = read_hands_models(model_path)
    return text_processor, hands_model


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
        ("path_to_test_video1.mp4", "expected sentence 1"),
        ("path_to_test_video2.mp4", "expected sentence 2"),
        ("path_to_test_video3.mp4", "expected sentence 3"),
    ],
)
def test_video_processing(video_path, expected_text, setup):
    model, text_processor, hands_model = setup
    processed_text = process_video(video_path, model, text_processor, hands_model)
    assert (
        processed_text == expected_text
    ), f"Expected '{expected_text}', but got '{processed_text}'"
    print(f"Test passed for video {video_path}!")
