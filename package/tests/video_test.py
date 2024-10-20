import datetime
import os

import pytest

from hands_to_text.text import TextProcessor
from hands_to_text.text.strategy import ChatGPTStrategy
from hands_to_text.video import CNNModelService, RandomForestModelService
from hands_to_text.video.processor import FramesProcessor


@pytest.fixture()
def rf_setup():
    """Fixture to set up the RandomForest model service."""
    model_path = "/home/piotr/Workspaces/studies/htt-models/models/rf.pickle"
    rf_model_service = RandomForestModelService(path=model_path)
    vtext_processor = TextProcessor(
        strategies=[ChatGPTStrategy(api_key=os.getenv("CHATGPT_KEY"))]
    )
    return rf_model_service, vtext_processor


def process_video_with_frames_processor(video_path, frames_processor) -> str:
    """General function to process video using FramesProcessor."""
    video_path = os.path.join(os.path.dirname(__file__), video_path)
    assert os.path.exists(video_path) is True
    return frames_processor.process_video(video_path)


@pytest.mark.parametrize(
    "video_path, expected_text",
    [
        # ("examples/iloveyou.mp4", "I LOVE YOU"),
        ("examples/drawcat.mp4", "DRAW CAT"),
        ("examples/howareyou.mp4", "How ARE YOU"),
        ("examples/whattheweather.mp4", "WHAT THE WEATHER"),
    ],
)
def test_random_forest_video_processing(
    video_path, expected_text, rf_setup, vid_results
):
    """Test case for RandomForestModelService using FramesProcessor."""
    rf_model_service, vtext_processor = rf_setup
    frames_processor = FramesProcessor(model_service=rf_model_service)
    start = datetime.datetime.now()
    recognized_text = process_video_with_frames_processor(video_path, frames_processor)
    delta = datetime.datetime.now() - start
    processed_text = vtext_processor.process(recognized_text)
    vid_results.append(
        {
            "video_path": video_path,
            "processing_time": delta,
            "strategies": f"`{', '.join([str(_) for _ in vtext_processor.strategies])}`",
            "model": rf_model_service.__class__.__name__,
            "recognized_text": recognized_text,
            "output": processed_text,
            "expected": expected_text,
        }
    )
    assert processed_text == expected_text
