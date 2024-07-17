from typing import NamedTuple

import cv2
import numpy as np
from mediapipe.python.solutions.drawing_styles import (
    get_default_hand_connections_style,
    get_default_hand_landmarks_style,
)
from mediapipe.python.solutions.drawing_utils import draw_landmarks
from mediapipe.python.solutions.hands import HAND_CONNECTIONS, Hands

margin = 10


class Point(NamedTuple):
    x: float
    y: float


class HandBox(NamedTuple):
    lt: Point
    rd: Point


class ClassedHandBox(NamedTuple):
    box: HandBox
    class_name: str


def _new_classed_hand_box(x1, y1, x2, y2, class_name) -> ClassedHandBox:
    return ClassedHandBox(
        box=HandBox(lt=Point(x=x1, y=y1), rd=Point(x=x2, y=y2)), class_name=class_name
    )


def get_alphabet_letter(position):
    if 0 <= position <= 25:
        return chr(position + 65)
    else:
        return None


def process_frame(frame, model, hands: Hands):
    data_aux = []
    x_ = []
    y_ = []
    H, W, _ = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            draw_landmarks(
                frame,  # image to draw
                hand_landmarks,  # model output
                HAND_CONNECTIONS,  # hand connections
                get_default_hand_landmarks_style(),
                get_default_hand_connections_style(),
            )

        for hand_landmarks in results.multi_hand_landmarks:
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y

                x_.append(x)
                y_.append(y)

            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x - min(x_))
                data_aux.append(y - min(y_))

        x1 = int(min(x_) * W) - margin
        y1 = int(min(y_) * H) - margin

        x2 = int(max(x_) * W) - margin
        y2 = int(max(y_) * H) - margin

        prediction = model.predict([np.asarray(data_aux)])

        class_name = get_alphabet_letter(int(prediction[0]))

        return _new_classed_hand_box(x1, y1, x2, y2, class_name)


def draw_classbox(frame, chbox: ClassedHandBox):
    cv2.rectangle(
        frame,
        (chbox.box.lt.x, chbox.box.lt.y),
        (chbox.box.rd.x, chbox.box.rd.y),
        (0, 0, 0),
        4,
    )
    cv2.putText(
        frame,
        chbox.class_name,
        (chbox.box.lt.x, chbox.box.lt.y - margin),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.3,
        (0, 0, 0),
        3,
        cv2.LINE_AA,
    )


# cap = cv2.VideoCapture(0)
# hands = Hands(max_num_hands=1, static_image_mode=True, min_detection_confidence=0.3)

# model_dict = pickle.load(open("./model.pickle", "rb"))
# model = model_dict["model"]

# while True:

#     _, frame = cap.read()

#     chbox = process_frame(frame, hands)
#     if chbox:
#         draw_classbox(chbox)

#     cv2.imshow("frame", frame)
#     cv2.waitKey(1)


# cap.release()
# cv2.destroyAllWindows()
