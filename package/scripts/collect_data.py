import os

import cv2
from mediapipe.python.solutions.hands import Hands

DATA_DIR = "../data/PERSON_NAME"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

number_of_classes = 26
dataset_size = 100
hands = Hands(static_image_mode=True, min_detection_confidence=0.3)

cap = cv2.VideoCapture(2)
for j in range(number_of_classes):
    parent_dir = os.path.join(DATA_DIR, str(j))
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)

    print("Collecting data for class {}".format(j))

    while True:
        ret, frame = cap.read()
        cv2.putText(
            frame,
            "press q t collect data class",
            (100, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            3,
            cv2.LINE_AA,
        )
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.imshow("frame", frame)
        if cv2.waitKey(25) == ord("q"):
            break

    while len(os.listdir(parent_dir)) < dataset_size:
        ret, frame = cap.read()
        cv2.imshow("frame", frame)
        cv2.waitKey(25)
        results = hands.process(frame_rgb)
        if results.multi_hand_landmarks is not None:
            cv2.imwrite(
                os.path.join(
                    DATA_DIR, str(j), "{}.jpg".format(len(os.listdir(parent_dir)) + 1)
                ),
                frame,
            )
        else:
            print("No hands landmarks detected, retaking image")

cap.release()
cv2.destroyAllWindows()
