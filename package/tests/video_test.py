import datetime
import os

import pytest

from hands_to_text.text import TextProcessor
from hands_to_text.text.strategy import ChatGPTStrategy
from hands_to_text.video import LeeNetModelService, RandomForestModelService
from hands_to_text.video.processor import FramesProcessor
from hands_to_text.video.services.resnet import ResNetModelService

GLOBAL_TEST_CASES = [
    ("examples/howareyou.mp4", "HOW ARE YOU"),
    ("examples/hi.mp4", "hi"),
    ("examples/iloveyou2.mp4", "I LOVE YOU"),
    ("examples/whatup.mp4", "WHAT UP"),
    # ("examples/drawcat.mp4", "DRAW CAT"),
    # ("examples/drawcat2.mp4", "WHAT THE WEATHER"),
]


@pytest.fixture()
def text_processor():
    """Fixture to set up the RandomForest model service."""
    text_processor = TextProcessor(
        strategies=[ChatGPTStrategy(api_key=os.getenv("CHATGPT_KEY"))]
    )
    return text_processor


def process_video_with_frames_processor(video_path, frames_processor) -> str:
    """General function to process video using FramesProcessor."""
    video_path = os.path.join(os.path.dirname(__file__), video_path)
    assert os.path.exists(video_path) is True
    return frames_processor.process_video(video_path)


@pytest.fixture(
    params=[
        (
            RandomForestModelService,
            "/home/piotr/Workspaces/studies/htt-models/models/rf.pickle",
        ),
        (
            LeeNetModelService,
            "/home/piotr/Workspaces/studies/htt-models/models/cnn.pth",
        ),
        (
            ResNetModelService,
            "/home/piotr/Downloads/htt-models/resnet_asl_cnn_model.pth",
        ),  # 5 epoch
        (
            ResNetModelService,
            "/home/piotr/Workspaces/studies/htt-models/httmodels/resnet_asl_cnn_model.pth",
        ),  # 25 epoch
    ]
)
def model_service(request):
    model_class, model_path = request.param
    return model_class(path=model_path)


@pytest.mark.parametrize("video_path, expected_output", GLOBAL_TEST_CASES)
def test_video_processing_with_models(
    model_service, text_processor, vid_results, video_path: str, expected_output: str
):

    frames_processor = FramesProcessor(model_service=model_service)

    video_path_full = os.path.join(os.path.dirname(__file__), video_path)
    assert os.path.exists(video_path_full) is True
    start = datetime.datetime.now()
    recognized_text = frames_processor.process_video(video_path_full)
    delta = datetime.datetime.now() - start

    processed_text = text_processor.process(recognized_text)
    vid_results.append(
        {
            "video_path": video_path,
            "processing_time": delta,
            "strategies": f"`{', '.join([str(_) for _ in text_processor.strategies])}`",
            "model": model_service.__class__.__name__,
            "recognized_text": recognized_text,
            "output": processed_text,
            "expected": expected_output,
        }
    )

    # assert processed_text == expected_output
