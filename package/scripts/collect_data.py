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
    if not os.path.exists(os.path.join(DATA_DIR, str(j))):
        os.makedirs(os.path.join(DATA_DIR, str(j)))

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
        results = hands.process(frame_rgb)
        print(results.multi_hand_landmarks is not None)
        cv2.imshow("frame", frame)
        if cv2.waitKey(25) == ord("q"):
            break

    counter = 0
    while counter < dataset_size:
        ret, frame = cap.read()
        cv2.imshow("frame", frame)
        cv2.waitKey(25)
        cv2.imwrite(os.path.join(DATA_DIR, str(j), "{}.jpg".format(counter)), frame)
        counter += 1

cap.release()
cv2.destroyAllWindows()
