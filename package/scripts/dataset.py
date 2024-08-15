import os
import pickle
from typing import List

import cv2
import matplotlib.pyplot as plt
import numpy as np
from mediapipe.python.solutions.hands import Hands

DATA_DIR = "./data"


def _draw_class_bar_plot(
    labels: List[str], counts: List[int], threshold_scale: float = 0.5
) -> None:
    max_count = np.max(counts)
    threshold = threshold_scale * max_count
    plt.figure(figsize=(12, 6))
    bars = plt.bar(labels, counts, color="b")
    for bar, count in zip(bars, counts):
        if count < threshold:
            bar.set_color("r")
    plt.xlabel("Class Labels")
    plt.ylabel("Number of Elements")
    plt.title("Class Distribution")
    plt.axhline(
        y=threshold, color="gray", linestyle="--", label=f"Threshold: {threshold}"
    )
    plt.legend()

    for bar, count in zip(bars, counts):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            str(count),
            ha="center",
            va="bottom",
        )
    plt.show()
    plt.savefig("class_distribution.png")


def _print_class_stats(
    labels: List[str],
    counts: List[int],
):
    print(f"missing classes for {set(labels).difference([str(i) for i in range(26)])}")
    for label, count in zip(labels, counts):
        msg = f"Class {label}: {count} elements"
        if count < 35:
            msg += " - should be retaken"
        print(msg)


def main():
    hands = Hands(max_num_hands=1, static_image_mode=True, min_detection_confidence=0.3)

    data = []
    labels = []

    for dir_ in sorted(os.listdir(DATA_DIR), key=lambda x: int(x)):
        for img_path in os.listdir(os.path.join(DATA_DIR, dir_)):
            data_aux = []
            x_ = []
            y_ = []
            img = cv2.imread(os.path.join(DATA_DIR, dir_, img_path))
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(img_rgb)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    for i in range(len(hand_landmarks.landmark)):
                        x_.append(hand_landmarks.landmark[i].x)
                        y_.append(hand_landmarks.landmark[i].y)

                    for i in range(len(hand_landmarks.landmark)):
                        data_aux.append(hand_landmarks.landmark[i].x - min(x_))
                        data_aux.append(hand_landmarks.landmark[i].y - min(y_))
                data.append(data_aux)
                labels.append(dir_)
            else:
                print(
                    "warning hand landmakrs unrecognized in image {}/{}".format(
                        dir_, img_path
                    )
                )
    unique_labels, counts = np.unique(labels, return_counts=True)
    _print_class_stats(unique_labels, counts)
    _draw_class_bar_plot(unique_labels, counts)

    with open("data.pickle", "wb") as f:
        pickle.dump({"data": data, "labels": labels}, f)


main()
