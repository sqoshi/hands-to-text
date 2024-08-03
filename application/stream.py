import pickle

import av
import streamlit as st
from mediapipe.python.solutions.hands import Hands

# from streamlit.runtime.scriptrunner import add_script_run_ctx, get_script_run_ctx
from streamlit_webrtc import VideoProcessorBase, webrtc_streamer

from hands_to_text.main import draw_classbox, process_frame

# from streamlit.report_thread import REPORT_CONTEXT_ATTR_NAME
from threading import current_thread
from contextlib import contextmanager
from io import StringIO
import sys
import logging
import time


# @contextmanager
# def st_redirect(src, dst):
#     placeholder = st.empty()
#     output_func = getattr(placeholder, dst)

#     with StringIO() as buffer:
#         old_write = src.write

#         def new_write(b):
#             if getattr(current_thread(), REPORT_CONTEXT_ATTR_NAME, None):
#                 buffer.write(b + '')
#                 output_func(buffer.getvalue() + '')
#             else:
#                 old_write(b)

#         try:
#             src.write = new_write
#             yield
#         finally:
#             src.write = old_write


# @contextmanager
# def st_stdout(dst):
#     with st_redirect(sys.stdout, dst):
#         yield


# @contextmanager
# def st_stderr(dst):
#     with st_redirect(sys.stderr, dst):
#         yield


# def demo_function():
#     for i in range(10):
#         logging.warning(f'Counting... {i}')
#         time.sleep(2)
#         print('Time out...')



class HandGestureProcessor(VideoProcessorBase):
    def __init__(self, model_path: str = "/app/hands_to_text/model.pickle"):
        self.hands = Hands(
            max_num_hands=1, static_image_mode=True, min_detection_confidence=0.3
        )
        model_dict = pickle.load(open(model_path, "rb"))
        self.model = model_dict["model"]
        self.recognized_text = ""

    def recv(self, frame: av.VideoFrame):
        img = frame.to_ndarray(format="bgr24")
        chbox = process_frame(img, self.model, self.hands)
        if chbox:
            draw_classbox(img, chbox)
            self.process_letter(chbox.class_name)
            # text_area.text_area("info", self.get_recognized_text())
            # st.chat_input(self.get_recognized_text())
        return av.VideoFrame.from_ndarray(img, format="bgr24")

    def process_letter(self, letter: str):
        self.recognized_text += letter

    def get_recognized_text(self) -> str:
        return self.recognized_text

## / full sentences with symbols

if __name__ == '__main__':
    st.title("Hand Gesture Recognition")
    hgp = HandGestureProcessor()


    webrtc_ctx = webrtc_streamer(
        key="VideoInput", video_processor_factory=HandGestureProcessor
    )
    
    # st.chat_input()
    # with st_stdout("success"), st_stderr("code"):
        # demo_function()

# if "dynamic_text" not in st.session_state:
#     st.session_state.dynamic_text = hgp.get_recognized_text()


# def target():
#     while True:
#         st.session_state.dynamic_text = hgp.get_recognized_text()


# if webrtc_ctx.video_processor:
#     st.text_area("Dynamic Text Area", st.session_state.dynamic_text)
#     ctx = get_script_run_ctx()
#     print(ctx)
#     st.session_state["thread"] = True
#     t = Thread(target=target)
#     add_script_run_ctx(t, ctx)
#     t.start()
# https://github.com/BugzTheBunny/streamlit_logging_output_example/blob/main/app.py
