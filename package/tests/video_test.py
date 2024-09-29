# import cv2
# import pytest

# from hands_to_text.text import (
#     LeverageLanguageModelStrategy,
#     RemoveRepetitionsStrategy,
#     TextProcessor,
# )
# from hands_to_text.video import draw_classbox, process_frame, read_hands_models


# @pytest.fixture()
# def mythings():
#     vtext_processor = TextProcessor(
#         strategies=[RemoveRepetitionsStrategy(), LeverageLanguageModelStrategy()]
#     )
#     model_path = "models/model.pickle"
#     vmodel, vhands = read_hands_models(model_path)
#     return vmodel, vhands, vtext_processor


# def process_video(video_path, vmodel, vhands, vtext_processor):
#     cap = cv2.VideoCapture(video_path)
#     recognized_text = ""
#     while True:
#         ret, frame = cap.read()
#         print(ret)
#         if not ret:
#             break
#         img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         chbox = process_frame(img, vmodel, vhands)
#         if chbox:
#             recognized_text += chbox.class_name
#         draw_classbox(img, chbox)
#     cap.release()
#     return vtext_processor.process(recognized_text)


# @pytest.mark.parametrize(
#     "video_path, expected_text",
#     [
#         ("examples/iloveyou.mp4", "i love you"),
#     ],
# )
# def test_video_processing(video_path, expected_text, mythings):
#     vmodel, vhands, vtext_processor = mythings
#     processed_text = process_video(video_path, vmodel, vhands, vtext_processor)
#     assert (
#         processed_text == expected_text
#     ), f"Expected '{expected_text}', but got '{processed_text}'"
